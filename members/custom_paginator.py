from rest_framework import pagination


class CustomPageNumberPagination(pagination.PageNumberPagination):
    page_size = 100
    page_size_query_param = 'pageSize'
    page_query_param = "current"
    max_page_size = 1000
