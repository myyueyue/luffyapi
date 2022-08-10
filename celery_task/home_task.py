'''
 @Description:见字如面 
 @Author: MING
 @Title: 
 @Date: 2022/8/2 16:00
'''
# 任务添加
from django.core.cache import cache
from .celery import app
from home import models
from django.conf import settings
from home import serializer


@app.task
def banner_update():
    # 无论有多少条待展示的数据，最多就展示3条
    queryset_banner = models.Banner.objects.filter(is_delete=False, is_show=True).order_by('orders')[
               :settings.BANNER_COUNTER]
    serializer_banner = serializer.BannerModelSerilaizer(instance=queryset_banner,many=True)
    for banner in serializer_banner:
        banner['img']='http://127.0.0.1:8080'+banner['img']
    cache.set("banner_list",serializer_banner)
    import time
    time.sleep(3)