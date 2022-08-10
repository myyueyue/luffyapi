# Create your views here.
from rest_framework.filters import OrderingFilter
from rest_framework.mixins import ListModelMixin,RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from . import models
from . import serializer
from rest_framework.filters import SearchFilter


# 课程分类
class CourseCategoryView(GenericViewSet, ListModelMixin):
    queryset = models.CourseCategory.objects.filter(is_delete=False, is_show=True).order_by('-orders')
    serializer_class = serializer.CourseCategorySerializer


# 课程群查
from .filter import CourseFilter
from .pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend


class CourseViews(GenericViewSet, ListModelMixin,RetrieveModelMixin):
    queryset = models.Course.objects.filter(is_delete=False, is_show=True).order_by('-orders')
    serializer_class = serializer.CourseModelSerializer
    pagination_class = PageNumberPagination

    # 过滤
    filter_backends =[DjangoFilterBackend,OrderingFilter]
    ordering_fields=['id','student','price']
    filter_fields=['course_category']
    # 区间过滤
    # filter_backends = [DjangoFilterBackend]
    # filter_class = [CourseFilter]


class CourseChapter(GenericViewSet,ListModelMixin):
    queryset = models.CourseChapter.objects.filter(is_delete=False,is_show=True)
    serializer_class = serializer.CourseChapterSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields=['course']


class CourseSearch(GenericViewSet,ListModelMixin):
    queryset = models.Course.objects.filter(is_delete=False,is_show=True)
    serializer_class = serializer.CourseModelSerializer
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter]
    search_fields=['name']