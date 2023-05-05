"""
モデルを定義するファイル
"""
from django.db import models


class YoutubeSummary(models.Model):
    """
    Youtubeの動画の要約を保存するモデル
    """
    video_id = models.CharField(max_length=100, primary_key=True)
    title = models.CharField(max_length=100, default="")
    summary = models.JSONField(default=list)

    def __str__(self):
        """
        オブジェクトの文字列表現を返す関数
        :return:
        """
        return self.video_id
