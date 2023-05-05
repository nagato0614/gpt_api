from rest_framework import viewsets
from .models import UserInfo
from .serializer import UserInfoSerializer


class UserInfoViewSet(viewsets.ModelViewSet):
    # モデルのオブジェクトを取得
    queryset = UserInfo.objects.all()
    # シリアライザーを取得
    serializer_class = UserInfoSerializer
