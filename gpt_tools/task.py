from celery import shared_task
from src.youtube_summary import YoutubeSummary


@shared_task
def task_summarizer(summarizer, obj):
    """
    youtube_summarizerを実行する
    :param summarizer:  YoutubeSummary
    :param obj: GptAPI
    :return:
    """

    # youtube_summarizerを実行
    for summary in summarizer.summarizer.summary_text_list:
        obj.summary.append(summary)

    # video_idを保存
    video_id = summarizer.id

    # summaryを保存
    obj.video_id = video_id

    # titleを保存
    obj.title = summarizer.downloader.title

    obj.save()
