from youtube_transcript_api import YouTubeTranscriptApi
import openai
from janome.charfilter import *
import tiktoken
from tiktoken.core import Encoding
from pytube import YouTube


# YouTubeのURLから動画IDを抽出する関数
def extract_youtube_id(url):
    """
    YouTubeの動画IDをURLから抽出する関数

    Args:
        url (str): YouTubeの動画URL

    Returns:
        str: YouTubeの動画ID
    """
    # YouTubeの動画IDの正規表現パターン
    regex_pattern = r"(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|[^\/]+\?.*v=))([a-zA-Z0-9_-]{11})"

    # 正規表現パターンでIDを検索する
    match = re.search(regex_pattern, url)

    # マッチオブジェクトからIDを抽出する
    if match:
        return match.group(1)
    else:
        return None


# 字幕のテキスト情報を抽出する関数
def get_subtitles_texts(transcript_list):
    """
    字幕リストから、各字幕のテキスト情報を抽出して一つの文字列に連結する関数。

    Args:
        transcript_list (list): YouTubeTranscriptApi.list_transcripts() で取得した字幕リスト。

    Returns:
        str: 各字幕のテキスト情報を連結した文字列。
    """
    str = ""
    for transcript in transcript_list:
        for tr in transcript.fetch():
            str += tr['text']  # {'text': '字幕のテキスト情報', 'start': 字幕の開始時間, 'duration': 字幕が表示されている時間}
    return str


def split_string(text, length):
    """
    文字列を指定した長さで分割する関数

    Args:
        text (str): 分割する文字列
        length (int): 分割する文字数

    Returns:
        list: 分割された文字列のリスト
    """
    # 空のリストを作成
    result = []

    # 指定された長さで文字列を分割してリストに追加する
    for i in range(0, len(text), length):
        result.append(text[i:i + length])

    return result


def get_token_number(text):
    '''
    文章のトークン数を取得する関数
    :param text: 文章
    :return: トークン数
    '''
    encoding: Encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    tokens = encoding.encode(text)
    tokens_count = len(tokens)
    return tokens_count


def summarize_transcript(text):
    '''
    字幕の要約を行う関数
    :param text: 字幕のテキスト情報
    :return: 要約された字幕のテキスト情報
    '''
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "あなたは説明上手な講師です."},
            {"role": "user", "content": f"これから渡す文章はyoutubeの字幕を抽出したものです.\n"
                                        f"以下の用に箇条書きで要約してください.\n"
                                        f"- 要約文1\n"
                                        f"- 要約文2M"
                                        f"\n\n"
                                        f" {text}"},
        ],
        temperature=0.5
    )
    return res["choices"][0]["message"]["content"]


def summarize(text):
    '''
    要約する関数
    :param text: 要約する文章
    :return: 要約された文章
    '''
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "あなたは説明上手な講師です."},  # 役割設定（省略可）
            {"role": "user", "content": f"これから渡す文章を日本語要約してください.\n\n{text}"},  # 最初の質問
        ],
        temperature=0.5
    )
    return res["choices"][0]["message"]["content"]


def get_video_title(video_url):
    '''
    動画のタイトルを取得する関数
    :param video_url: 動画のURL
    :return: 動画のタイトル
    '''
    try:
        yt = YouTube(video_url)
        title = yt.title
        return title

    except:
        print("An error occurred")
        return None


def summary_youtube_video(url):
    '''
    YouTubeの動画の要約を行う関数
    :param url: YouTubeの動画URL
    :return: 要約された字幕のテキスト情報
    '''
    # 動画IDを抽出する
    youtube_id = extract_youtube_id(url)
    print(youtube_id)

    # 字幕情報を取得する
    transcript_list = YouTubeTranscriptApi.list_transcripts(youtube_id)
    text = get_subtitles_texts(transcript_list)
    print(text)
    print("char count : ", len(text))
    print("token : ", get_token_number(text))

    # 字幕を指定した長さで分割する
    text_list = split_string(text, 1500)
    summarized_text = []
    for t in text_list:
        for line in summarize_transcript(t).splitlines():
            summarized_text.append(line)
            print(line)
    return summarized_text
