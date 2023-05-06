"""
YoutubeSummaryのテストモジュール
"""
from django.test import TestCase
from .models import GptAPI
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APIRequestFactory
from .views import *


class YoutubeSummaryTestCase(TestCase):
    """
    YoutubeSummaryのテストクラス
    """

    def setUp(self):
        """
        テスト実行前に実行される関数
        """
        obj = GptAPI(
            video_id="test_video_id",
            title="test_title",
            summary={
                "summary": ["test_summary1", "test_summary2"]
            }
        )
        obj.save()

        self.factory = APIRequestFactory()
        self.view = GptAPIViewSet.as_view({'get': 'list'})
        self.item_url = "youtube_summary/"
        self.host_url = "https://127.0.0.1:8000/"

    def test_youtube_summary(self):
        """
        YoutubeSummaryのテスト
        """
        qs_count = GptAPI.objects.count()
        print("qs_count : ", qs_count)
        self.assertEqual(qs_count, 1)

    def test_api_get(self):
        """
        APIのGETメソッドのテスト
        :return:
        """
        url = self.host_url + self.item_url
        request = self.factory.get(url)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
