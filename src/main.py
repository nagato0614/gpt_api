from summary_youtube import *
from summary_pdf import *
from audio import *
import matplotlib.pyplot as plt
import numpy as np
from scraping import *


def summary_youtube():
    # url = "https://www.youtube.com/watch?v=YyhfK-aBo-Y&ab_channel=GOTOConferences"
    url = "https://www.youtube.com/watch?v=Jq1zyNk7b4w&ab_channel=FormulaCentric"
    summary = YoutubeSummarizer(url)
    print(summary.text)
    print(summary.summarizer.summary_text_list)

def summary_pdf():
    path = "tdk_en.pdf"
    pdf_summarizer = PdfSummarizer(path)

if __name__ == '__main__':
    base_url = "https://www.sony.jp/"
    scraper = WebScraper(
        base_url=base_url,
        download_folder="sony",
        backoff_factor=3,
    )
    scraper.scrape()