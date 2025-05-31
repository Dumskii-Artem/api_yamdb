import django_filters

from reviews.models import Title


class TitleFilter(django_filters.FilterSet):
    """Фильтрация по полям для Title."""

    category = django_filters.CharFilter(
        field_name='category__slug',
        lookup_expr='icontains'
    )
    genre = django_filters.CharFilter(
        field_name='genre__slug',
        lookup_expr='icontains'
    )
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )
    year = django_filters.NumberFilter(
        field_name='year'
    )

    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year')
