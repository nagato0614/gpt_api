from youtube_summary import *
from summary_pdf import *
from youtube_downloader import *


def summary_youtube():
    # url = "https://www.youtube.com/watch?v=YyhfK-aBo-Y&ab_channel=GOTOConferences"
    # url = "https://www.youtube.com/watch?v=5sIg-wNEj_U&ab_channel=%E3%82%AE%E3%82%BA%E3%83%A2%E3%83%BC%E3%83%89%E3%83%BB%E3%82%B8%E3%83%A3%E3%83%91%E3%83%B3"
    # url = "https://www.youtube.com/watch?v=H7Ytt07yyhM&ab_channel=FORMULA1"
    url = "https://www.youtube.com/watch?v=0WwJOVwluRQ&ab_channel=%E3%82%AB" \
          "%E3%83%BC%E3%83%95%E3%82%A3%E3%83%BC%E3%83%AA%E3%83%B3%E3%82%B0 "
    summary = YoutubeSummary(url)
    print(summary.text)
    count = 0
    if summary.text is not None:
        for line in summary.summarizer.summary_text_list:
            print(str(count) + " : " + line)


def summary_pdf():
    path = "tdk_en.pdf"
    pdf_summarizer = PdfSummarizer(path)


def youtube_viede_download():
    url = "https://www.youtube.com/watch?v=H7Ytt07yyhM&ab_channel=FORMULA1"
    youtube_downloader = YoutubeDownloader(url)
    print(youtube_downloader.title)
    youtube_downloader.download_audio()


if __name__ == '__main__':
    summary_youtube()
