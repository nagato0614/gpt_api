import youtube_transcript_api
from youtube_transcript_api import *
from janome.charfilter import *


class YoutubeDownloader:
    """
    YouTubeの動画をダウンロードしたり字幕などを取得するクラス
    """
    url: str
    id: str
    transcript_list: youtube_transcript_api.TranscriptList
    title: str

    def __init__(self, url: str):
        """

        :param url: YouTubeの動画URL
        """
        self.url = url
        self.id = self.extract_youtube_id(self.url)
        self.transcript_list = self.fetch()

    def extract_youtube_id(self, url: str):
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

    def find_ja_or_en_transcript(self):
        """
        指定された動画IDに対して、まず日本語の字幕を検索し、見つからない場合は英語の字幕を検索します。
        どちらの言語の字幕も見つからない場合は、何も返さずに終了します。

        Returns:
            Transcript: 見つかった字幕のTranscriptオブジェクト。どちらの言語の字幕も見つからない場合はNone。
        """

        # YouTubeの動画IDから字幕のリストを取得する
        try:
            print(self.id)
            transcript_list = YouTubeTranscriptApi.list_transcripts(self.id)

            # 字幕がない場合はNoneを返す
        except NoTranscriptFound:
            print("字幕が見つかりませんでした。")
            return None
        except youtube_transcript_api._errors.TranscriptsDisabled:
            print("字幕が無効になっています。")
            return None
        except AttributeError:
            print("YoutubeDownloader :  AttributeError")
            return None

        try:
            # 日本語の字幕を探す
            ja_transcript = transcript_list.find_transcript(['ja'])
            return ja_transcript
        except NoTranscriptFound:
            try:
                # 日本語が見つからない場合は英語の字幕を探す
                en_transcript = transcript_list.find_transcript(['en'])
                return en_transcript
            except NoTranscriptFound:
                # 日本語と英語のどちらの字幕も見つからない場合はNoneを返す
                return None

    def fetch(self):
        """
        字幕のテキスト情報を抽出しアトリビュートに保存する
        :return: youtube_transcript_api.TranscriptList
        """
        transcript = self.find_ja_or_en_transcript()
        if transcript is None:
            return None
        self.transcript_list = transcript.fetch()
        return self.transcript_list


if __name__ == '__main__':
    url = "https://www.youtube.com/watch?v=YyhfK-aBo-Y&ab_channel=GOTOConferences"
    youtube_downloader = YoutubeDownloader(url)
    print(youtube_downloader.title)
    for text in youtube_downloader.transcript_list:
        print(text['text'])
