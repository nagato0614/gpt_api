"""
URL configuration for nagato_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the included() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from drf_test_app.views import UserInfoViewSet
from gpt_api.views import GptAPIViewSet

# userInfoのURLを設定する
userInfo = routers.DefaultRouter()
userInfo.register('userinfo', UserInfoViewSet)

# youtubeSummaryのURLを設定する
youtubeSummary = routers.DefaultRouter()
youtubeSummary.register('youtubeSummary', GptAPIViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),

    # defaultRouterのURLをincludeする
    path('dft_api/', include(userInfo.urls)),

    # defaultRouterのURLをincludeする
    path('gpt_api/', include(youtubeSummary.urls)),

    path('', include('gpt_tools.urls')),
]
