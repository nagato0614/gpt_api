import os
from src.summarizer import GptSummarizer
from src.youtube_downloader import YoutubeDownloader
from src.youtube_summarizer import *


class YoutubeSummary:
    """
    Youtubeの字幕を要約するクラス
    字幕をベクトル化して、要約する
    """

    # YoutubeDownloaderクラスのインスタンス
    downloader: YoutubeDownloader

    # YouTubeの動画タイトル
    title: str

    # YouTubeの動画ID
    id: str

    # Youtubeの字幕を纏めた文字列
    text: str

    # 要約した文字列
    summarizer: YoutubeSummarizer

    # noinspection PyTypeChecker
    def __init__(self, url: str):
        """
        Summaryクラスのコンストラクタ
        :param url: YouTubeの動画URL
        """
        self.response_list = []
        self.downloader = YoutubeDownloader(url)
        self.summarizer = None

        # YouTubeの動画IDが取得できた場合
        if self.downloader.transcript_list is not None:

            # YouTubeの動画タイトルを取得する
            self.id = self.downloader.id
            self.transcript_list = self.downloader.transcript_list

            self.text = ""
            if self.transcript_list is not None:
                # 字幕を1つの文字列にまとめる
                for transcript in self.transcript_list:
                    self.text += transcript["text"] + " "

            self.summarizer = YoutubeSummarizer(self.text,
                                                title=self.downloader.title,
                                                split_text_size=2000,
                                                model=GptSummarizer.GPT3_TURBO)

            # self.summarizer = GptSummarizer(self.text,
            #                                 split_text_size=2000,
            #                                 model=GptSummarizer.GPT3_TURBO)
        # self.save_text()
        # self.summarizer.save_summary(self.youtube_downloader.id)

    def save_text(self):
        """
        textディレクトリに字幕を保存する関数
        :return: 保存したファイル名
        """

        # transcript_listがNoneの場合は何もしない
        if self.transcript_list is None:
            return None

        # ディレクトリがなければ作成する
        if not os.path.exists("../text"):
            os.mkdir("../text")

        # ファイル名を指定
        file_name = f"{self.id}.txt"

        # ファイルを開く, ファイルが無い場合は作成する
        with open(f"../text/{file_name}", "w", encoding='utf-8') as f:
            # 字幕をファイルに書き込む
            for transcript in self.transcript_list:
                f.write(transcript["text"] + "\n")

        return file_name

    @staticmethod
    def remove_newlines(series):
        """
        文字列の改行を削除する関数
        :param series: 文字列のSeries
        :return: 改行を削除した文字列のSeries
        """
        series = series.str.replace('\n', ' ')
        series = series.str.replace('\\n', ' ')
        series = series.str.replace('  ', ' ')
        series = series.str.replace('  ', ' ')
        return series
