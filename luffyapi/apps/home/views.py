from django.core.cache import cache
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
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
    queryset = models.Banner.objects.filter(is_delete=False, is_show=True).order_by('orders')[
               :settings.BANNER_COUNTER]
    serializer_class = serializer.BannerModelSerializer
    print(queryset.all())

    def list(self, request, *args, **kwargs):
        banner_list = cache.get('banner_list')
        if not banner_list:
            # 数据库取值
            response = super().list(request, *args, **kwargs)

            # 加入缓存
            cache.set(banner_list, response.data, 60 * 60)
            return response
        return Response(data=banner_list)
