from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from .models import UserInfo

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ('id', 'user_name', 'birth_day', 'age', 'create_at')