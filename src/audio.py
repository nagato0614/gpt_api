import pyaudio
import os
import pvporcupine
import struct
import numpy as np


class Audio:
    """
    マイクから音声を読み取り, 人が喋っている部分だけを取得できるクラス.
    """

    # オーディオストリーム
    audio: pyaudio.PyAudio

    # ウェイクワード
    keyword: str

    # PICOVOICEのAPIキー
    picovoice_api_key: str

    porcupine: pvporcupine.Porcupine

    def __init__(self, keyword="hey pico"):
        """
        コンストラクタ
        """
        self.picovoice_api_key = os.environ["PICOVOICE_API_KEY"]
        self.keyword = keyword
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.close_audio()

    def __del__(self):
        self.close_audio()

    def open_audio(self):
        """
        オーディオストリームを取得する関数
        """
        # オーディオストリームを取得
        self.stream = self.audio.open(format=pyaudio.paInt16,
                                      rate=44100,
                                      channels=1,
                                      input_device_index=1,
                                      input=True,
                                      frames_per_buffer=self.porcupine.frame_length)
        return self.stream

    def create_pvporcupine(self):
        """
        PICOVOICEのインスタンスを作成する関数
        """
        self.porcupine = pvporcupine.create(access_key=self.picovoice_api_key,
                                            keywords=[self.keyword],
                                            sensitivities=[0.5])

    def close_audio(self):
        """
        オーディオストリームを閉じる関数
        """
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

    def read_audio(self, size=1024):
        """
        オーディオストリームから音声を読み取る関数
        :return: 音声データ
        """
        # 音声データを読み取る
        audio_data = self.stream.read(size)
        return audio_data
