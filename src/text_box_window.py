from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout, QPushButton, QLabel, QProgressBar, \
    QGridLayout
from PyQt5.QtGui import QFont

class TextboxWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Text Boxes')
        self.setFixedSize(500, 700)
        self.setup_ui()

    def setup_ui(self):
        """
        テキストボックスとボタンを作成し、ウィンドウに追加するメソッド
        """
        self.setup_text_boxes()
        self.setup_labels()
        self.setup_button()
        self.setup_progress_bar()
        self.setup_layout()

    def setup_text_boxes(self):
        # QLineEditオブジェクトを作成する
        self.text_box1 = QLineEdit()
        self.text_box1.setFixedHeight(50)
        self.text_box1.setFont(QFont("MyricaM", 12))  # フォントを設定する
        self.text_box2 = QLineEdit()
        self.text_box2.setFixedHeight(400)
        self.text_box2.setReadOnly(True)  # 書き込み不可能にする
        self.text_box2.setFont(QFont("MyricaM", 12))  # フォントを設定する

    def setup_labels(self):
        # QLabelオブジェクトを作成する
        self.label1 = QLabel('URL')
        self.label1.setFont(QFont("MyricaM", 12))
        self.label2 = QLabel('../summary')
        self.label2.setFont(QFont("MyricaM", 12))

    def setup_button(self):
        # QPushButtonオブジェクトを作成する
        self.button = QPushButton('Get Text')
        self.button.setFixedHeight(50)
        self.button.setFont(QFont("MyricaM", 12))

        # QPushButtonに関数を関連付ける
        self.button.clicked.connect(self.on_button_click)

    def setup_progress_bar(self):
        # QProgressBarオブジェクトを作成する
        self.progress_bar = QProgressBar()
        self.progress_bar.setBaseSize(400, 20)
        self.progress_bar.setFont(QFont("MyricaM", 12))

    def setup_layout(self):
        # QGridLayoutオブジェクトを作成する
        layout = QGridLayout()
        layout.addWidget(self.label1, 0, 0)
        layout.addWidget(self.text_box1, 1, 0)
        layout.addWidget(self.label2, 2, 0)
        layout.addWidget(self.text_box2, 3, 0)
        layout.addWidget(self.button, 4, 0)
        layout.addWidget(self.progress_bar, 5, 0)

        # QWidgetにレイアウトを設定する
        self.setLayout(layout)

    def on_button_click(self):
        """
        ボタンがクリックされたら呼び出される関数
        """
        # text1 = self.text_box1.text()
        # max_progress = 100
        #
        # youtube_id = extract_youtube_id(text1)
        # transcript_list = YouTubeTranscriptApi.list_transcripts(youtube_id)
        # subtitles_text = get_subtitles_texts(transcript_list)
        # text_list = split_string(subtitles_text, 1500)
        # for t in text_list:
        #     for line in summarize_transcript(t).splitlines():
        #         self.text_box2.append(line)
        #         print(line)
        #     self.progress_bar.setValue(max_progress / len(text_list))
