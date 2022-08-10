'''
 @Description:见字如面 
 @Author: MING
 @Title: 
 @Date: 2022/8/8 13:59
'''
from rest_framework.filters import BaseFilterBackend

from course import models


class MyFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset[:1]


from django_filters.filterset import FilterSet
from django_filters import filters


class CourseFilter(FilterSet):
    # 区间过滤
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')  # gte大于等于
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')  # 小于等于

    class Meta:
        model = models.Course
        fields = ['course_category']
