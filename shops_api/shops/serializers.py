from rest_framework import serializers

from shops_api.shops.models import City, Shop, Street


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'name')


class StreetSerializer(serializers.ModelSerializer):
    city = serializers.SlugRelatedField(slug_field='name', queryset=City.objects.all())

    class Meta:
        model = Street
        fields = ('id', 'name', 'city')


class ShopSerializer(serializers.ModelSerializer):

    city = serializers.SlugRelatedField(slug_field='name', queryset=City.objects.all())
    street = serializers.SlugRelatedField(slug_field='name', queryset=Street.objects.all())

    def create(self, validated_data):
        shop = super().create(validated_data)
        return shop.id

    class Meta:
        model = Shop
        fields = ('id', 'name', 'city', 'street', 'building', 'opening_time', 'closing_time')
