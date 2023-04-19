from django.utils import timezone
from django_filters import CharFilter, ChoiceFilter, FilterSet

from shops_api.shops.models import Shop

STATUS_CHOICES = (
    (0, 'Shop is closed'),
    (1, 'Shop is open'),
)


class ShopFilter(FilterSet):
    '''Filter class for handling filtering query parameters.'''
    city = CharFilter(method='filter_by_city', label='City')
    street = CharFilter(method='filter_by_street', label='Street')
    open = ChoiceFilter(method='filter_by_open', label='Open now', choices=STATUS_CHOICES)

    def filter_by_city(self, queryset, name, value):
        '''
        Filtering method for handling `city` query parameter.
        Allows to filter by `City` id or `City` name.
        '''
        try:
            city_id = int(value)
            return queryset.filter(city_id=city_id)
        except ValueError:
            city_name = ' '.join([word.capitalize() for word in value.strip().split()])
            return queryset.filter(city__name__iexact=city_name)

    street = CharFilter(field_name='street', method='filter_by_street')

    def filter_by_street(self, queryset, name, value):
        '''
        Filtering method for handling `stret` query parameter.
        Allows to filter by `Street` id or `Street` name.
        '''
        try:
            street_id = int(value)
            return queryset.filter(street_id=street_id)
        except ValueError:
            street_name = ' '.join([word.capitalize() for word in value.strip().split()])
            return queryset.filter(street__name__iexact=street_name)

    def filter_by_open(self, queryset, name, value):
        '''
        Filtering method for handling `open` query parameter.
        Allows to filter shops which open or closed in current time - depends on
        `opening_time` and `closing_time` of `Shop` object.
        '''
        now = timezone.now().time()
        value = int(value)
        if value:
            return queryset.filter(opening_time__lte=now, closing_time__gte=now)
        else:
            return queryset.exclude(opening_time__lte=now, closing_time__gte=now)

    class Meta:
        model = Shop
        fields = ('city', 'street', 'open')
