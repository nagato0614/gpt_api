"""
APIのエンドポイントを定義するクラス
"""

from rest_framework import viewsets
from .models import YoutubeSummary
from .serializer import YoutubeSummarySerializer


class YoutubeSummaryViewSet(viewsets.ModelViewSet):
    """
    APIのエンドポイントを定義するクラス
    """

    # クエリセットを指定
    queryset = YoutubeSummary.objects.all()

    # シリアライザーを指定
    serializer_class = YoutubeSummarySerializer
