from django.db import models
from unicodedata import category, name


class UserInfo(models.Model):
    user_name = models.CharField(verbose_name='ユーザー名', max_length=32)
    birth_day = models.DateField(verbose_name='生年月日')
    age = models.PositiveSmallIntegerField(verbose_name='年齢',
                                           null=True,
                                           unique=False)
    create_at = models.DateTimeField(verbose_name='作成日時',
                                     auto_now_add=True)
