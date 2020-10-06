import django_filters

from .models import Title


class TitleFilter(django_filters.rest_framework.FilterSet):
    genre = django_filters.CharFilter(
        field_name='genre__slug', lookup_expr='iexact'
    )
    category = django_filters.CharFilter(
        field_name='category__slug', lookup_expr='iexact'
    )
    name = django_filters.CharFilter(
        field_name='name', lookup_expr='contains'
    )

    class Meta:
        model = Title
        fields = ('year', )
