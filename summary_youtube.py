import os
import tiktoken
import openai
from tiktoken.core import *
from pytube import YouTube
from youtube_downloader import YoutubeDownloader
import json
from decimal import Decimal


class Summary:
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

    # コンテキスト
    embedding: openai.Embedding

    # 分割されたテキスト
    split_text: list[str]

    # 要約されたテキストのリスト
    summary_text_list: list[str]

    # 受け取ったレスポンスのリスト
    response_list: list

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

        self.save()

    def save(self):
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

    def get_token_number(self):
        '''
        文章のトークン数を取得する関数
        :param text: 文章
        :return: トークン数
        '''
        encoding: Encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
        tokens = encoding.encode(self.text)
        tokens_count = len(tokens)
        return tokens_count

    def split_into_many(self, max_tokens=8191):
        """
        テキストを最大トークン数を超えないように分割する関数

        Args:
            text (str): 分割するテキスト
            max_tokens (int, optional): 分割後の各チャンクの最大トークン数。デフォルトはmax_tokens。

        Returns:
            list: 分割されたテキストのリスト
        """

        # テキストを単語に分割する
        words = self.text.split(' ')

        # 各単語のトークン数を1として処理する
        n_tokens = [1 for _ in words]

        chunks = []
        tokens_so_far = 0
        chunk = []

        # 単語とトークンがタプルで結合されたものをループで処理する
        for word, token in zip(words, n_tokens):

            # これまでのトークン数と現在の単語のトークン数の合計が最大トークン数を超える場合、
            # チャンクをチャンクのリストに追加し、チャンクとこれまでのトークン数をリセットする
            if tokens_so_far + token > max_tokens:
                chunks.append(" ".join(chunk))
                chunk = []
                tokens_so_far = 0

            # 現在の単語のトークン数が最大トークン数を超える場合、次の単語に移動する
            if token > max_tokens:
                continue

            # それ以外の場合、単語をチャンクに追加し、トークン数を合計に追加する
            chunk.append(word)
            tokens_so_far += token + 1

        # 最後のチャンクを追加
        if chunk:
            chunks.append(" ".join(chunk))

        self.split_text = chunks
        return chunks

    def summarize_split_text(self):
        """
        分割されたテキストを要約する関数
        :return: 要約されたテキストのリスト
        """
        self.summary_text_list = []
        for split_t in self.split_text:
            self.summary_text_list.append(self.summarize_turbo(split_t))
        return self.summary_text_list

    def summarize_davinci(self, text):
        '''
        GPT-3のDavinciエンジンを使って文章を要約する関数
        :param text: 字幕のテキスト情報
        :return: 要約された字幕のテキスト情報
        '''

        def decimal_to_int(obj):
            if isinstance(obj, Decimal):
                return int(obj)

        input_text = f"これから渡す文章はyoutubeの字幕を抽出したものです.\n" \
                     f"文章を要約してください, その時言語は日本語で表示してください.\n" \
                     f"\n\n" \
                     f" {text}" \

        res = openai.Completion.create(
            engine="text-davinci-003",
            prompt=input_text,
            max_tokens=3000,
        )
        json.dumps(res, default=decimal_to_int, ensure_ascii=False)
        self.response_list.append(res)
        return res.choices[0].text

    def summarize_turbo(self, text):
        '''
        GPT-3のTurboエンジンを使って文章を要約する関数
        :param text: 要約する文章
        :return: 要約された文章
        '''
        def decimal_to_int(obj):
            if isinstance(obj, Decimal):
                return int(obj)

        res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "あなたは説明上手な講師です."},  # 役割設定（省略可）
                {"role": "user", "content": f"これから渡す文章はyoutubeの字幕を抽出したものです.\n"
                                            f"文章を要約してください, その時言語は日本語で表示してください.\n"
                                            f"\n\n"
                                            f"{text}"},
            ],
            temperature=0.5
        )
        json.dumps(res, default=decimal_to_int, ensure_ascii=False)
        self.response_list.append(res)
        return res["choices"][0]["message"]["content"]



