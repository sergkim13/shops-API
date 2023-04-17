from django.urls import path

from shops_api.shops.views import CityAPIListView, StreetAPIListView, ShopAPIView

urlpatterns = [
    path('cities/', CityAPIListView.as_view()),
    path('cities/<int:city_id>/streets/', StreetAPIListView.as_view()),
    path('shops/', ShopAPIView.as_view()),
]