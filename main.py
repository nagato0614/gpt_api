from summary_youtube import *
from summary_pdf import *
from audio import *
import matplotlib.pyplot as plt
import numpy as np


def summary_youtube():
    # url = "https://www.youtube.com/watch?v=YyhfK-aBo-Y&ab_channel=GOTOConferences"
    url = "https://www.youtube.com/watch?v=Jq1zyNk7b4w&ab_channel=FormulaCentric"
    summary = YoutubeSummarizer(url)
    print(summary.text)
    print(summary.summarizer.summary_text_list)

def summary_pdf():
    path = "tdk_en.pdf"
    pdf_summarizer = PdfSummarizer(path)

if __name__ == '__main__':
    summary_pdf()
    # print("hello world")
    # audio = Audio()
    # audio.open_audio()
    #
    # while True:
    #     try:
    #         audiodata = np.frombuffer(audio.read_audio(), dtype="int16")
    #         plt.plot(audiodata)
    #         plt.draw()
    #         plt.pause(0.001)
    #         plt.cla()
    #     except KeyboardInterrupt:
    #         break
