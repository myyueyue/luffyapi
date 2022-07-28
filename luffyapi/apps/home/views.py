from django.shortcuts import render

from rest_framework.views import APIView
from luffyapi.utils.response import APIResponse
from luffyapi.utils.logger import log

from rest_framework.mixins import ListModelMixin
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import GenericViewSet
from . import models
from . import serializer

# class BannerView(GenericAPIView,ListModelMixin):  # 这个路由配置  path('banner/', views.BannerView.as_view()),

# 路由位置
'''
from rest_framework.routers import  SimpleRouter
router=SimpleRouter()
router.register('banner',views.BannerView,'banner')
path('', include(router.urls)),
'''
from django.conf import settings


class BannerView(GenericViewSet, ListModelMixin):
    # 无论有多少条待展示的数据，最多就展示3条
    queryset = models.Banner.objects.filter(is_delete=False, is_show=True).order_by('display_order')[
               :settings.BANNER_COUNTER]
    serializer_class = serializer.BannerModelSerilaizer
