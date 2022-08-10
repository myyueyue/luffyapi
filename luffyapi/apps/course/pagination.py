'''
 @Description:见字如面 
 @Author: MING
 @Title: 
 @Date: 2022/8/7 10:01
'''
from rest_framework.pagination import PageNumberPagination as DRFPageNumberPagination
class PageNumberPagination(DRFPageNumberPagination):
    page_size = 1
    page_query_param = 'page'
    max_page_size = 10
    page_size_query_param = 'size'