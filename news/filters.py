import django_filters

from .models import News


class NewsFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='categories__slug', lookup_expr='iexact')
    author = django_filters.CharFilter(field_name='author__username', lookup_expr='iexact')
    status = django_filters.CharFilter(field_name='status', lookup_expr='iexact')
    published_after = django_filters.IsoDateTimeFilter(field_name='published_date', lookup_expr='gte')
    published_before = django_filters.IsoDateTimeFilter(field_name='published_date', lookup_expr='lte')

    class Meta:
        model = News
        fields = ['category', 'author', 'status']
