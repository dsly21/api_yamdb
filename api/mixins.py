from rest_framework.pagination import PageNumberPagination


class PaginationMixin:
    pagination_class = PageNumberPagination
    pagination_class.page_size = 10
