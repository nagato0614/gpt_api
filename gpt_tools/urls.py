"""
gpt_toolsのURLを設定する
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from . import views


app_name = 'gpt_tools'

# gpt_toolsのURLを設定する
urlpatterns = [

    # gpt_toolsのURLをincludeする
    path('', views.index, name='index'),
]
