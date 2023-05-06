"""
gpt_toolsの view を設定する
"""
from django.shortcuts import render
from .forms import SummaryForm

def index(request):
    form = SummaryForm()
    context = {'form': form}
    return render(request, 'hello_world/index.html', context=context)


def youtube_summary(request):
    return render(request, 'youtube_summary/youtube_summary.html')
