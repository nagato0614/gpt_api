"""
YoutubeSummaryのテストモジュール
"""
from django.test import TestCase
from .models import YoutubeSummary


class YoutubeSummaryTestCase(TestCase):
    """
    YoutubeSummaryのテストクラス
    """

    def setUp(self):
        """
        テスト実行前に実行される関数
        """
        obj = YoutubeSummary(
            video_id="test_video_id",
            title="test_title",
            summary={
                ["test_summary1", "test_summary2"]
            }
        )
        obj.save()

    def test_youtube_summary(self):
        """
        YoutubeSummaryのテスト
        """
        qs_count = YoutubeSummary.objects.count()
        self.assertEqual(qs_count, 1)
