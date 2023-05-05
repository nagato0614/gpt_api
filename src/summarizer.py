import tiktoken
import openai
from tiktoken.core import *
import json
from decimal import Decimal
import os
import re
from src.split_sentences import TextSplitter


class GptSummarizer:
    """
    GPTを使って要約するクラス
    """

    # 分割されたテキスト
    split_text: list[str]

    # 要約されたテキストのリスト
    summary_text_list: list[str]

    # 受け取ったレスポンスのリスト
    response_list: list

    # 入力するテキスト
    input_text: str

    # GPT-3のモデル
    model: str

    # GPT-3のエンジン
    GPT3_TURBO = "gpt-3.5-turbo"

    # GPT-3のエンジン
    GPT3_DAVINCI = "text-davinci-003"

    # GPT-4のエンジン
    GPT4 = "gpt-4"

    # テキストを分割するときのトークン数
    split_text_size: int

    def __init__(self, text, split_text_size=1000, model=GPT4):
        """
        コンストラクタ
        :param text: 要約する文字列
        """
        self.text = text
        self.response_list = []
        self.model = model
        self.split_text_size = split_text_size

        if text is not None:
            self.split_into_many(split_text_size)
            self.summarize()

    def save_summary(self, file_name: str):
        """
        要約したテキストリストを保存する
        :param file_name: 保存先のファイルパス
        :return:
        """

        # 要約がなければ何もしない
        if self.summary_text_list is None:
            return None

        # ディレクトリがなければ作成
        if not os.path.exists("../summary"):
            os.mkdir("../summary")

        # 時々箇条書きが数字になってしまうので '-' に置換する
        output_text_list = []
        for s in self.summary_text_list:
            # 改行文字で分割してリストにする.
            line_list = s.split("\n")

            for line in line_list:
                # 戦闘が数字で始まる箇条書きを '-' に置換する
                pattern1 = r"^(\d+\.)|(\d+\)) "
                replaced_text1 = re.sub(pattern1, "- ", line)

                # - で始まる行だけ取り出す.
                pattern2 = r"^- "
                if re.match(pattern2, replaced_text1):
                    output_text_list.append(replaced_text1)

        self.summary_text_list = output_text_list

        # ファイルに保存 utf-8で保存する
        save_file_path = "../summary/" + file_name + ".txt"
        with open(save_file_path, mode='w', encoding='utf-8') as f:
            for line in self.summary_text_list:
                f.write(line + "\n")

    def get_token_number(self, text: str):
        """
        文章のトークン数を取得する関数
        :return: トークン数
        """

        encoding: Encoding = tiktoken.encoding_for_model(self.model)
        tokens = encoding.encode(text)
        tokens_count = len(tokens)
        return tokens_count

    def split_into_many(self, max_tokens=8191):
        """
        テキストを最大トークン数を超えないように分割する関数

        Args:
            max_tokens (int, optional): 分割後の各チャンクの最大トークン数。
            デフォルトはmax_tokens。

        Returns:
            list: 分割されたテキストのリスト
        """
        # テキストを単語に分割する
        splitter = TextSplitter(self.text, self.model)
        words = splitter.split_text
        n_tokens = splitter.token_list

        chunks = []
        tokens_so_far = 0
        chunk = []

        # 単語とトークンがタプルで結合されたものをループで処理する
        for word, token in zip(words, n_tokens):

            # これまでのトークン数と現在の単語のトークン数の合計が最大トークン数を超える場合、
            # チャンクをチャンクのリストに追加し、チャンクとこれまでのトークン数をリセットする
            if tokens_so_far + token > max_tokens:
                chunks.append("".join(chunk))
                chunk = []
                tokens_so_far = 0

            # それ以外の場合、単語をチャンクに追加し、トークン数を合計に追加する
            chunk.append(word)
            tokens_so_far += token

        # 最後のチャンクを追加
        if chunk:
            chunks.append("".join(chunk))

        self.split_text = chunks
        return chunks

    def summarize(self):
        """
        分割されたテキストを要約する関数
        :return: 要約されたテキストのリスト
        """

        self.summary_text_list = []
        for split_t in self.split_text:
            if self.model == self.GPT3_TURBO:
                summary = self.summarize_chat_completion(split_t)
            elif self.model == self.GPT3_DAVINCI:
                summary = self.summarize_davinci(split_t)
            elif self.model == self.GPT4:
                summary = self.summarize_chat_completion(split_t)
            else:
                raise Exception("モデル名が不正です : " + self.model)

            print("------ 分割されたテキスト ------")
            print(self.input_text)
            print("------------ 要約 ------------")
            print(summary)

            self.summary_text_list.append(summary)
        return self.summary_text_list

    def generate_input_text(self, input_context, point=8):
        """
        GPT-3の入力テキストを生成する関数
        参考 : https://qiita.com/m-morohashi/items/391b350075ff91f4a694
        :param point: 生成する箇条書きの数
        :param input_context: 入力コンテキスト
        :return: GPT-3の入力テキスト
        """
        example = ""
        for i in range(point):
            # example += "- 文章" + str(i + 1) + "\n"
            example += "- \n"
        self.input_text = """
# 指示

今から渡す文章を, 日本語を使用して{point}個の文章で纏めてください.
さらに, 以下の成約を必ず守ってください.

# 文章の成約

- 最大{point}個
- 5w1Hを明確にする
- ',', '.', '、', '。'は使用禁止

# 対象とする文章

{text}

# 出力形式 

{example}
        """.format(text=input_context, point=point, example=example)
        return self.input_text

    def summarize_davinci(self, text):
        """
        GPT-3のDavinciエンジンを使って文章を要約する関数
        :param text: 字幕のテキスト情報
        :return: 要約された字幕のテキスト情報
        """

        def decimal_to_int(obj):
            if isinstance(obj, Decimal):
                return int(obj)

        input_text = self.generate_input_text(text)

        res = openai.Completion.create(
            engine="text-davinci-003",
            prompt=input_text,
            max_tokens=3000,
        )
        json.dumps(res, default=decimal_to_int, ensure_ascii=False)
        self.response_list.append(res)
        return res.choices[0].text

    def summarize_chat_completion(self, text):
        """
        GPT-3のTurboエンジンを使って文章を要約する関数
        :param text: 要約する文章
        :return: 要約された文章
        """

        input_text = self.generate_input_text(text)

        def decimal_to_int(obj):
            if isinstance(obj, Decimal):
                return int(obj)

        res = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "あなたは優秀な新聞記者です"},
                {"role": "user", "content": input_text},
            ],
            temperature=0.5
        )
        json.dumps(res, default=decimal_to_int, ensure_ascii=False)
        self.response_list.append(res)
        return res["choices"][0]["message"]["content"]
