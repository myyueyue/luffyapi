'''
 @Description:见字如面 
 @Author: MING
 @Title: 
 @Date: 2022/8/3 11:34
'''
from django.urls import path, re_path, include
from . import views

from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('categories',views.CourseCategoryView,'categories')
router.register('free',views.CourseViews,'free')
router.register('chapters',views.CourseViews,'chapters')
router.register('search',views.CourseSearch,'search')
urlpatterns = [
    path('', include(router.urls)),
]


