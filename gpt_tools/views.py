from django.shortcuts import render


def index(request):
    return render(request, 'hello_world/index.html')


def youtube_summary(request):
    return render(request, 'youtube_summary/youtube_summary.html')
