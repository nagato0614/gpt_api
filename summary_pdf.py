import PyPDF2
import os
from summarizer import GptSummarizer
import codecs


class PDFToTextConverter:
    # pdfファイルが保存されているディレクトリ
    dir_name: str

    # pdfファイル名
    file_name: str

    # テキスト化したpdfファイルの保存先ディレクトリ
    output_dir: str

    def __init__(self,
                 file_name,
                 input_dir_name="pdf",
                 output_dir_name="pdf_text"):
        """
        コンストラクタ
        :param file_name: pdfファイル名
        :param input_dir_name: pdfファイルが保存されているディレクトリ名
        :param output_dir_name: テキスト化したpdfファイルの保存先ディレクトリ名
        """
        self.file_name = file_name
        self.input_file_path = input_dir_name + "/" + file_name
        self.output_dir_name = output_dir_name
        self.output_file_name = file_name.replace(".pdf", ".txt")
        self.output_file_path = self.output_dir_name + "/" + self.output_file_name
        self.text = ""
        self.convert_to_text()
        self.save()

    def convert_to_text(self):
        """
        pdfファイルをテキスト化する
        :return:
        """
        read_text = ''

        with open(self.input_file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for i in range(len(reader.pages)):
                page = reader.pages[i]
                read_text += page.extract_text()
        self.text = read_text
        return read_text

    def save(self):
        """
        テキストを保存する
        :param text: 保存するテキスト
        :return: なし
        """

        # ディレクトリが存在するか確認してなければディレクトリ作成
        if not os.path.exists(self.output_dir_name):
            os.mkdir(self.output_dir_name)

        text = self.text
        with codecs.open(f"{self.output_file_path}", "w", 'utf-8', 'ignore') as f:
            f.write(text)


class PdfSummarizer:
    """
    PDFの要約を行うクラス
    """

    def __init__(self, file_name):
        """
        コンストラクタ
        :param file_name: 要約するPDFファイル名
        """
        self.file_name = file_name
        self.converter = PDFToTextConverter(file_name)
        self.summarizer = GptSummarizer(self.converter.text)
        self.summarizer.save_summary(file_name)

    def summarize(self):
        pass
