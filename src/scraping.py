import os
import re
import time
import requests
from bs4 import BeautifulSoup
from collections import deque
from urllib.parse import urljoin, urlparse
from io import BytesIO
import PyPDF2
from fake_useragent import UserAgent
import codecs


class WebScraper:
    """
    指定したurlのページをスクレイピングする
    """

    # HTTP URLの正規表現パターン
    HTTP_URL_PATTERN = r'^http[s]{0,1}://.+$'

    def __init__(self, base_url, download_folder, max_retries=10,
                 backoff_factor=0.5):
        """
        コンストラクタ
        :type base_url: str
        :type download_folder: str
        :type max_retries: int
        :type backoff_factor: float

        :param base_url:
        :param download_folder:
        :param max_retries:
        :param backoff_factor:
        """

        self.base_url = base_url
        self.local_domain = urlparse(base_url).netloc
        self.download_folder = "scraper/" + download_folder
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.user_agent = UserAgent()
        self.session = requests.Session()

        # visited ファイルを読み込む
        self.visited = self.load_visited()

        # queue ファイルを読み込む
        self.queue = self.load_queue()

    def load_queue(self):
        """
        queueファイルを読み込み、dequeにして返す
        :return:
        """

        if os.path.exists(self.download_folder + "_queue.txt"):
            queue = deque()
            with open(self.download_folder + "_queue.txt", "r") as f:
                for line in f:
                    queue.append(line.strip())
            return queue
        else:
            return deque([self.base_url])

    def load_visited(self):
        """
        visitedファイルを読み込み、setにして返す
        :return:
        """
        visited = set()
        if os.path.exists(self.download_folder + "_visited.txt"):
            with open(self.download_folder + "_visited.txt", "r") as f:
                for line in f:
                    visited.add(line.strip())

        return visited

    def download_page(self, url):
        """
        指定したurlのページをダウンロードする
        :param url:
        :return:
        """

        # リトライとタイムアウトの設定を行う
        for i in range(self.max_retries):
            try:
                # ダウンロード
                headers = {
                    "User-Agent": self.user_agent.random}
                response = self.session.get(url, headers=headers, timeout=5)
                response.raise_for_status()
                return response
            except requests.exceptions.RequestException as e:

                # リトライ回数を超えたらエラーを返す
                sleep_time = self.backoff_factor ** float(i)
                if i < self.max_retries - 1:
                    print(f"Error downloading {url}: {e}")
                    print(
                        f"Retrying in {sleep_time} seconds... (retries left: {self.max_retries - i - 1})")
                    time.sleep(sleep_time)
                else:
                    print(
                        f"Failed to download {url} after {self.max_retries} retries.")
                    exit()

    def sanitize_filename(self, filename):
        """
        ファイル名として使えない文字を置き換える
        :param filename:
        :return:
        """
        return re.sub(r'[\\/:"*?<>|\n]', '', filename)

    def save_page(self, url, response):
        """
        ページを保存する
        :param url:
        :param response:
        :return:
        """

        # ディレクトリがなければ作成
        if not os.path.exists(self.download_folder):
            os.makedirs(self.download_folder)

        # ファイル名を作成
        file_path = self.download_folder + '/' + self.sanitize_filename(
            url[8:]) + ".txt"

        # PDFの場合はテキストに変換して保存
        if response.headers.get("Content-Type") == "application/pdf":
            pdf_content = BytesIO(response.content)
            text_content = self.pdf_to_text(pdf_content)
            path = file_path.replace(".pdf", ".txt")
            with codecs.open(path, "w", 'utf-8',
                             'ignore') as f:
                f.write(text_content)

        # それ以外の場合はそのまま保存
        else:
            with codecs.open(file_path, "w", 'utf-8',
                             'ignore') as f:
                soup = BeautifulSoup(response.text, "html.parser")
                f.write(self.clean_text(soup.get_text()))

    def clean_text(self, text: str):
        """
        無駄な改行を減らして保存する
        :param text: 修正するテキスト
        :return: 修正されたテキスト
        """
        clean_text = text.encode('utf-8', 'ignore').decode('utf-8')
        clean_text = re.sub(r'\n+', '\n', clean_text)
        clean_text = re.sub(r'\t+', '\n', clean_text)
        return clean_text

    def extract_links(self, url, content):
        """
        ページからリンクを抽出する
        :param url:
        :param content:
        :return:
        """
        # ページの内容を解析
        soup = BeautifulSoup(content, "html.parser")

        # Extract all the anchor tags
        anchor_tags = soup.find_all("a")

        # Get the href attributes of the anchor tags and store them in a list
        hyperlinks = [a.get("href") for a in anchor_tags]
        # リンクを抽出
        clean_links = []
        for link in set(hyperlinks):
            if link is None:
                continue

            clean_link = None


            # リンクに特定の文字が含まれていればスキップする.
            skip_exts = [
                "javascript:void"
                "javascript:ssfl.login"
            ]
            if any(ext in link for ext in skip_exts):
                print(link)
                continue

            # リンクが相対パスの場合は絶対パスに変換
            if re.search(self.HTTP_URL_PATTERN, link):
                url_obj = urlparse(clean_link)

                # ローカルドメインの場合はそのまま
                if url_obj.netloc == self.local_domain:
                    clean_link = link

            else:
                if link.startswith("/"):
                    link = link[1:]
                elif (
                        link.startswith("#")
                        or link.startswith("mailto:")
                        or link.startswith("tel:")
                ):
                    continue
                clean_link = "https://" + self.local_domain + "/" + link


            if clean_link is not None:
                if clean_link.endswith("/"):
                    clean_link = clean_link[:-1]
                clean_links.append(clean_link)

        return clean_links

    def pdf_to_text(self, pdf_content):
        pdf_content.seek(0)
        pdf_reader = PyPDF2.PdfReader(pdf_content)
        text = []

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text.append(page.extract_text())

        return "\n".join(text)

    def scrape(self):

        # キューが空になるまで繰り返す
        try:
            while self.queue:
                print(f"Queue size: {len(self.queue)}"
                      f" | Visited URLs: {len(self.visited)}")

                # キューからURLを取り出す
                current_url = self.queue.popleft()
                if current_url in self.visited:
                    continue
                print(f"Scraping {current_url}")
                self.visited.add(current_url)

                # ページをダウンロードする
                response = self.download_page(current_url)
                if not response:
                    continue

                self.save_page(current_url, response)

                # リンクを抽出する
                for link in self.extract_links(current_url, response.text):
                    if link not in self.visited:
                        self.queue.append(link)

        except KeyboardInterrupt:
            print("Interrupted by the user")

            # キーボードからの割り込みがあった場合visitedの内容を
            # ファイルに保存しておく
            with open(self.download_folder + "_visited.txt", "w") as f:
                f.write("\n".join(self.visited))

            # queueの内容を保存する
            with open(self.download_folder + "_queue.txt", "w") as f:
                f.write("\n".join(self.queue))
