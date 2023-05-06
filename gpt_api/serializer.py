"""
Serializer for YoutubeSummary model
"""
from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from .models import YoutubeSummary


class YoutubeSummarySerializer(serializers.ModelSerializer):
    """
    Serializer for YoutubeSummary model
    """
    class Meta:
        """
        Metaclass for YoutubeSummarySerializer
        """
        model = YoutubeSummary

        # jsonに含めるフィールドを指定
        fields = ('video_id', 'title', 'summary')