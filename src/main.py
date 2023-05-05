from summary_youtube import *
from summary_pdf import *
from audio import *
import matplotlib.pyplot as plt
import numpy as np
from scraping import *


def summary_youtube():
    url = "https://www.youtube.com/watch?v=YyhfK-aBo-Y&ab_channel=GOTOConferences"
    # url = "https://www.youtube.com/watch?v=5sIg-wNEj_U&ab_channel=%E3%82%AE%E3%82%BA%E3%83%A2%E3%83%BC%E3%83%89%E3%83%BB%E3%82%B8%E3%83%A3%E3%83%91%E3%83%B3"
    # url = "https://www.youtube.com/watch?v=H7Ytt07yyhM&ab_channel=FORMULA1"
    # url = "https://www.youtube.com/watch?v=0WwJOVwluRQ&ab_channel=%E3%82%AB%E3%83%BC%E3%83%95%E3%82%A3%E3%83%BC%E3%83%AA%E3%83%B3%E3%82%B0"
    summary = YoutubeSummarizer(url)
    print(summary.text)
    if summary.text is not None:
        print(summary.summarizer.summary_text_list)

def summary_pdf():
    path = "tdk_en.pdf"
    pdf_summarizer = PdfSummarizer(path)

if __name__ == '__main__':
    summary_youtube()
    # base_url = "https://www.sony.jp/"
    # scraper = WebScraper(
    #     base_url=base_url,
    #     download_folder="sony",
    #     backoff_factor=3,
    # )
    # scraper.scrape()