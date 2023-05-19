"""
gpt_toolsの view を設定する
"""
from django.shortcuts import render
from .forms import SummaryForm
from gpt_api.models import GptAPI
from src.youtube_summary import YoutubeSummary
from .task import task_summarizer


def index(request):
    """
    indexページを表示する
    youtubeのurlを入力すると、その動画の要約を表示する
    :param request:
    :return:
    """
    # formの定義
    form = SummaryForm(request.POST or None)
    context = {'form': form}

    if form.is_valid():

        print("form is valid")
        # urlを取得
        url = form.cleaned_data['url']
        obj = GptAPI(url=url)
        print("url : ", url)

        # youtube_summarizerを作成
        youtube_summarizer = YoutubeSummary(url)

        # youtube_summarizerが作成できなかった場合
        if youtube_summarizer.can_summarize is False:
            return render(request, 'hello_world/index.html', context=context)

        # youtube_summarizerを実行
        task_summarizer.delay(youtube_summarizer, obj)

    return render(request, 'hello_world/index.html', context=context)


def youtube_summary(request):
    return render(request, 'youtube_summary/youtube_summary.html')
