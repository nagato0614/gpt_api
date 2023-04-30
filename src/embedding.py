import requests
import re
import urllib.request
from bs4 import BeautifulSoup
from collections import deque
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote
import os
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import sys
import codecs
from fake_useragent import UserAgent

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer)

# Regex pattern to match a URL
HTTP_URL_PATTERN = r'^http[s]{0,1}://.+$'

# Define root domain to crawl
full_url = "https://www.sony.jp/"
domain = "sony.jp"

ua = UserAgent()


# リトライとタイムアウトの設定を行う
def create_retry_session():
    session = requests.Session()
    retry = Retry(
        total=5,  # 最大リトライ回数
        backoff_factor=1,  # スリープ時間の係数
        status_forcelist=[429, 500, 502, 503, 504],  # リトライするHTTPステータスコード
        allowed_methods=["GET"],  # リトライするHTTPメソッド
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


session = create_retry_session()


# Create a class to parse the HTML and get the hyperlinks
class HyperlinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        # Create a list to store the hyperlinks
        self.hyperlinks = []

    # Override the HTMLParser's handle_starttag method to get the hyperlinks
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)

        # If the tag is an anchor tag, and it has a href attribute, add the href attribute to the list of hyperlinks
        if tag == "a" and "href" in attrs:
            print("handle_starttag : " + attrs["href"])
            self.hyperlinks.append(attrs["href"])


def remove_invalid_characters(text: str, encoding="utf-8"):
    return text.encode(encoding, errors="ignore").decode(encoding)


def get_text_from_html(html):
    try:
        soup = BeautifulSoup(html, "lxml", from_encoding="utf-8")
        text = soup.get_text()
    except Exception as e:
        print("Error in get_text_from_html: " + str(e))
        text = ""
    return text


# Function to get the hyperlinks from a URL
def get_hyperlinks(url):
    try:
        # Get the text from the URL using BeautifulSoup
        headers = {
            "User-Agent": ua.random
        }
        response = session.get(url, headers=headers, timeout=1)  # タイムアウトを10秒に設定

        # If the response is not HTML, return an empty list
        if not response.headers['Content-Type'].startswith("text/html"):
            return []

        # Get the HTML content
        html = response.content

        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")

        # Extract all the anchor tags
        anchor_tags = soup.find_all("a")

        # Get the href attributes of the anchor tags and store them in a list
        hyperlinks = [a.get("href") for a in anchor_tags]

        return hyperlinks
    except Exception as e:
        print("Get Hyperlinks Error: " + str(e))
        return []


################################################################################
### Step 3
################################################################################

# Function to get the hyperlinks from a URL that are within the same domain
def get_domain_hyperlinks(local_domain, url):
    clean_links = []
    for link in set(get_hyperlinks(url)):
        if link is None:
            continue

        clean_link = None

        # If the link is a URL, check if it is within the same domain
        if re.search(HTTP_URL_PATTERN, link):
            # Parse the URL and check if the domain is the same
            url_obj = urlparse(link)
            if url_obj.netloc == local_domain:
                clean_link = link

        # If the link is not a URL, check if it is a relative link
        else:
            if link.startswith("/"):
                link = link[1:]
            elif (
                    link.startswith("#")
                    or link.startswith("mailto:")
                    or link.startswith("tel:")
            ):
                continue
            clean_link = "https://" + local_domain + "/" + link

        if clean_link is not None:
            if clean_link.endswith("/"):
                clean_link = clean_link[:-1]
            clean_links.append(clean_link)

    # Return the list of hyperlinks that are within the same domain
    return list(set(clean_links))


def clean_text(text: str):
    """
    Clean the text by removing extra newlines
    :param text: text to clean
    :return: clean text
    """
    clean_text = text.encode('utf-8', 'ignore').decode('utf-8')
    clean_text = re.sub(r'\n+', '\n', clean_text)
    clean_text = re.sub(r'\t+', '\n', clean_text)
    return clean_text


def sanitize_filename(filename):
    # Replace invalid characters with an empty string
    return re.sub(r'[\\/:"*?<>|\n]', '', filename)


def crawl(url: str):
    # Parse the URL and get the domain
    local_domain = urlparse(url).netloc

    # Create a queue to store the URLs to crawl
    queue = deque([url])

    # Create a set to store the URLs that have already been seen (no duplicates)
    seen = {url}

    # count of read pages
    count = 0

    # Create a directory to store the text files
    if not os.path.exists("../text/"):
        os.mkdir("../text/")

    if not os.path.exists("text/" + local_domain + "/"):
        os.mkdir("text/" + local_domain + "/")

    # Create a directory to store the csv files
    if not os.path.exists("processed"):
        os.mkdir("processed")

    # While the queue is not empty, continue crawling
    while queue:
        print("------------------------------------------------------------------------------"
              "------------------------------------------------------------------------------")
        print("queue size: " + str(len(queue)) +
              " | seen size: " + str(len(seen)) +
              " | count: " + str(count))
        # Get the next URL from the queue
        url = queue.pop()

        file_path = 'text/' + local_domain + '/' + sanitize_filename(url[8:]) + ".txt"
        decoded_file_path = unquote(file_path)
        print(decoded_file_path)
        # Save text from the url to a <url>.txt file
        with open(file_path, "w", encoding="UTF-8") as f:

            try:
                # Get the text from the URL using BeautifulSoup
                headers = {
                    "User-Agent": ua.random}
                response = session.get(url, headers=headers, timeout=10)  # タイムアウトを10秒に設定

                # Correct encoding detection
                response.encoding = response.apparent_encoding

                soup = BeautifulSoup(response.text, "html.parser")

                # Get the text but remove the tags
                text = soup.get_text()

            except Exception as e:
                print("Error in get_text_from_html: " + str(e))
                continue

            # If the crawler gets to a page that requires JavaScript, it will stop the crawl
            if ("You need to enable JavaScript to run this app." in text):
                print("Unable to parse page " + url + " due to JavaScript being required")

            clean_text_data = clean_text(text)
            # Otherwise, write the text to the file in the text directory
            f.write(clean_text_data)

        print("finish write text file")

        # Get the hyperlinks from the URL and add them to the queue
        for link in get_domain_hyperlinks(local_domain, url):
            if link not in seen:
                queue.append(link)
                seen.add(link)

        count += 1


if __name__ == '__main__':
    crawl(full_url)
