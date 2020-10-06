from rest_framework import mixins, viewsets, filters
from rest_framework.pagination import PageNumberPagination
from .permissions import IsAdminOrReadOnly


class PaginationMixin:
    pagination_class = PageNumberPagination
    pagination_class.page_size = 10


class BasicCategoryGenreMixin(
    PaginationMixin, mixins.DestroyModelMixin, mixins.ListModelMixin,
    mixins.CreateModelMixin, viewsets.GenericViewSet
):
    filter_backends = (filters.SearchFilter, )
    search_fields = ('slug', 'name')
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly, )
