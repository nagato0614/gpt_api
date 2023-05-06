"""
モデルを定義するファイル
"""
from django.db import models


class GptAPI(models.Model):
    """
    Youtubeの動画の要約を保存するモデル
    """
    video_id = models.CharField(verbose_name='動画ID',
                                max_length=100,
                                primary_key=True)
    url = models.CharField(verbose_name='URL',
                           max_length=200,
                           default="")
    title = models.CharField(verbose_name='タイトル',
                             max_length=100,
                             default="")
    summary = models.JSONField(verbose_name='要約',
                               blank=True,
                               null=True,
                               default=list)

    def __str__(self):
        """
        オブジェクトの文字列表現を返す関数
        :return:
        """
        return self.video_id
