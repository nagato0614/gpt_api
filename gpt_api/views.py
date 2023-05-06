"""
APIのエンドポイントを定義するクラス
"""

from rest_framework import viewsets
from .models import GptAPI
from .serializer import GptAPISerializer


class GptAPIViewSet(viewsets.ModelViewSet):
    """
    APIのエンドポイントを定義するクラス
    """

    # クエリセットを指定
    queryset = GptAPI.objects.all()

    # シリアライザーを指定
    serializer_class = GptAPISerializer
