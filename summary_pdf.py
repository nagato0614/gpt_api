import PyPDF2


class PDFToTextConverter:
    # pdfファイルが保存されているディレクトリ
    dir_name: str

    # pdfファイル名
    file_name: str

    # テキスト化したpdfファイルの保存先ディレクトリ
    output_dir: str

    def __init__(self,
                 file_name,
                 dir_name="pdf",
                 output_dir="pdf_text"):
        self.file_name = file_name
        self.file_path = dir_name + "/" + file_name
        self.output_dir = output_dir

    def convert_to_text(self):
        with open(self.file_name, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ''
            for i in range(len(reader.pages)):
                print(f'page {i}')
                print(reader.pages[i].extract_text())
                page = reader.pages[i]
                text += page.extract_text()
        return text

    def save(self, text):
        with open(f"text/{self.file_path}.txt", "w") as f:
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
        self.text = self.converter.convert_to_text()
        self.converter.save(self.text)

    def summarize(self):
        pass
