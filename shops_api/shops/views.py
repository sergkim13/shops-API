from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.response import Response

from shops_api.shops.filters import ShopFilter
from shops_api.shops.models import City, Shop, Street
from shops_api.shops.serializers import CitySerializer, ShopSerializer, StreetSerializer


class CityAPIListView(generics.ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class StreetAPIListView(generics.ListAPIView):
    queryset = Street.objects.all()
    serializer_class = StreetSerializer

    def get_queryset(self):
        city_id = self.kwargs['city_id']
        queryset = Street.objects.filter(city_id=city_id)
        return queryset


class ShopAPIView(generics.ListCreateAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ShopFilter

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_id = serializer.save()
        return Response({'id': product_id}, status=status.HTTP_201_CREATED)
