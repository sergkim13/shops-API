from django.forms import ModelChoiceField
from django_filters import FilterSet, CharFilter
from shops_api.shops.models import City, Shop


class ShopFilter(FilterSet):
    city = CharFilter(method='filter_by_city', label='City')
    street = CharFilter(method='filter_by_street', label='Street')

    def filter_by_city(self, queryset, name, value):
        try:
            city_id = int(value)
            return queryset.filter(city_id=city_id)
        except ValueError:
            city_name = value.strip().capitalize()
            return queryset.filter(city__name__iexact=city_name)

    street = CharFilter(field_name='street', method='filter_by_street')

    def filter_by_street(self, queryset, name, value):
        try:
            street_id = int(value)
            return queryset.filter(street_id=street_id)
        except ValueError:
            street_name = value.strip().capitalize()
            return queryset.filter(street__name__iexact=street_name)

    class Meta:
        model = Shop
        fields = ('city', 'street')
