import os
import tiktoken
import openai
from tiktoken.core import *
from pytube import YouTube

from summarizer import GptSummarizer
from youtube_downloader import YoutubeDownloader
import json
from decimal import Decimal


class YoutubeSummarizer:
    """
    Youtubeの字幕を要約するクラス
    字幕をベクトル化して、要約する
    """

    # YoutubeDownloaderクラスのインスタンス
    youtube_downloader: YoutubeDownloader

    # YouTubeの動画タイトル
    title: str

    # YouTubeの動画ID
    id: str

    # Youtubeの字幕を纏めた文字列
    text: str

    summarizer: GptSummarizer

    def __init__(self, url: str):
        """
        Summaryクラスのコンストラクタ
        :param url: YouTubeの動画URL
        """
        self.response_list = []
        self.youtube_downloader = YoutubeDownloader(url)
        self.id = self.youtube_downloader.id
        self.transcript_list = self.youtube_downloader.transcript_list

        # 字幕を1つの文字列にまとめる
        self.text = ""
        for transcript in self.transcript_list:
            self.text += transcript["text"]

        self.summarizer = GptSummarizer(self.text)

        self.save_text()
        self.summarizer.save_summary(self.youtube_downloader.id)

    def save_text(self):
        """
        textディレクトリに字幕を保存する関数
        :return: 保存したファイル名
        """

        # ディレクトリがなければ作成する
        if not os.path.exists("text"):
            os.mkdir("text")

        # ファイル名を指定
        file_name = f"{self.id}.txt"

        # ファイルを開く
        with open(f"text/{file_name}", "w") as f:
            # 字幕をファイルに書き込む
            for transcript in self.transcript_list:
                f.write(transcript["text"] + "\n")

        return file_name

    def remove_newlines(self, series):
        """
        文字列の改行を削除する関数
        :param serie: 文字列のSeries
        :return: 改行を削除した文字列のSeries
        """
        series = series.str.replace('\n', ' ')
        series = series.str.replace('\\n', ' ')
        series = series.str.replace('  ', ' ')
        series = series.str.replace('  ', ' ')
        return series
