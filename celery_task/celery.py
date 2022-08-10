'''
 @Description:见字如面 
 @Author: MING
 @Title: 
 @Date: 2022/8/2 15:59
'''
from celery import Celery

# 加载django环境
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'luffyapi.setting.dev')

broker = 'redis://127.0.0.1:6379/2'  # 执行任务
backend = 'redis://127.0.0.1:6379/1'  # 结果存储

app = Celery(__name__, backend=backend, broker=broker,include=['celery_task.home_task',])


#执行定时任务