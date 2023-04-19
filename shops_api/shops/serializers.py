from rest_framework import serializers

from shops_api.shops.models import City, Shop, Street


class CitySerializer(serializers.ModelSerializer):
    '''Serializer class for `City` ojects.'''
    class Meta:
        model = City
        fields = ('id', 'name')


class StreetSerializer(serializers.ModelSerializer):
    '''Serializer class for `Street` ojects.'''
    city = serializers.SlugRelatedField(slug_field='name', queryset=City.objects.all())

    class Meta:
        model = Street
        fields = ('id', 'name', 'city')


class ShopSerializer(serializers.ModelSerializer):
    '''Serializer class for `Shop` ojects.'''

    city = serializers.SlugRelatedField(slug_field='name', queryset=City.objects.all())
    street = serializers.SlugRelatedField(slug_field='name', queryset=Street.objects.all())

    def create(self, validated_data):
        '''
        Overridden `create` method which is calling `Shop` model's `clean' method for
        activating compatibility checking of `city` and `street`.
        '''
        shop = Shop(**validated_data)
        shop.clean()
        shop.save()
        return shop.id

    class Meta:
        model = Shop
        fields = ('id', 'name', 'city', 'street', 'building', 'opening_time', 'closing_time')
