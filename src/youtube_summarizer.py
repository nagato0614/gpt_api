"""
GptSummarizerを継承してyoutube動画の要約に特化させたクラス
"""
from summarizer import *


class YoutubeSummarizer(GptSummarizer):
    """
    Youtubeの字幕を要約するクラス
    """

    # Youtubeの動画タイトル
    title: str

    def __init__(self,
                 text,
                 title="",
                 split_text_size=1000,
                 model=GptSummarizer.GPT4):
        """
        コンストラクタ
        """
        self.title = title
        super().__init__(text, split_text_size, model)

    def generate_input_text(self, input_context, point=5):
        """
        生成するテキストを youtube 動画要約用に最適化する
        :param point:
        :param input_context:
        :return:
        """
        example = ""
        for i in range(point):
            example += "- テキスト" + str(i + 1) + "\n"
        self.input_text = """
# 指示

今から渡す文章は \"{title}\" という youtube 動画字幕の一部です.
日本語を使用して {point} 個の文章で纏めてください.
さらに, 以下の成約を必ず守ってください.

# 文章の成約

- 日本語を使う
- 最大{point}個の文章
- 5W1Hを明確にする
- 句読点 (',', '.', '、', '。') は使用禁止

# 対象とする文章

{text}

# 出力形式

{example}

        """.format(title=self.title,
                   text=input_context,
                   point=point,
                   example=example)
        return self.input_text
