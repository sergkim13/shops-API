from http import HTTPStatus

from django.urls import reverse
from freezegun import freeze_time
from rest_framework.test import APITestCase

from shops_api.shops.models import City, Shop, Street
from shops_api.shops.serializers import CitySerializer, ShopSerializer, StreetSerializer


class ShopAPITestCase(APITestCase):
    fixtures = ['cities.json', 'streets.json', 'shops.json']

    def setUp(self):
        self.fixture_city_1 = City.objects.get(id=1)
        self.fixture_city_2 = City.objects.get(id=2)
        self.fixture_street_1 = Street.objects.get(id=1)
        self.fixture_street_2 = Street.objects.get(id=2)
        self.fixture_street_3 = Street.objects.get(id=3)
        self.fixture_street_4 = Street.objects.get(id=4)
        self.fixture_shop_1 = Shop.objects.get(id=1)
        self.fixture_shop_2 = Shop.objects.get(id=2)
        self.fixture_shop_3 = Shop.objects.get(id=3)
        self.fixture_shop_4 = Shop.objects.get(id=4)

    def test_get_cities(self):
        expected_data = CitySerializer([self.fixture_city_1, self.fixture_city_2], many=True).data

        url = reverse('cities')
        response = self.client.get(url)

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual(expected_data, response.data)

    def test_get_cities_empty(self):
        Shop.objects.all().delete()
        Street.objects.all().delete()
        City.objects.all().delete()
        url = reverse('cities')
        response = self.client.get(url)

        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual([], response.data)

    def test_get_streets(self):
        url_1 = reverse('streets', kwargs={'city_id': self.fixture_city_1.id})
        url_2 = reverse('streets', kwargs={'city_id': self.fixture_city_2.id})
        url_3 = reverse('streets', kwargs={'city_id': 3})  # not existing city
        response_1 = self.client.get(url_1)
        response_2 = self.client.get(url_2)
        response_3 = self.client.get(url_3)
        expected_data_1 = StreetSerializer([self.fixture_street_1, self.fixture_street_2], many=True).data
        expected_data_2 = StreetSerializer([self.fixture_street_3, self.fixture_street_4], many=True).data

        self.assertEqual(HTTPStatus.OK, response_1.status_code)
        self.assertEqual(HTTPStatus.OK, response_2.status_code)
        self.assertEqual(HTTPStatus.OK, response_3.status_code)
        self.assertEqual(expected_data_1, response_1.data)
        self.assertEqual(expected_data_2, response_2.data)
        self.assertEqual([], response_3.data)

    @freeze_time('2023-04-18 19:30')
    def test_get_shops(self):
        url = reverse('shops')
        response_1 = self.client.get(url)
        response_2 = self.client.get(url, data={'city': 1})
        response_3 = self.client.get(url, data={'city': 'City 2'})
        response_4 = self.client.get(url, data={'street': 3})
        response_5 = self.client.get(url, data={'street': 'Street 4'})
        response_6 = self.client.get(url, data={'open': 0})
        response_7 = self.client.get(url, data={'open': 1})
        response_8 = self.client.get(url, data={'city': 1, 'street': 2, 'open': 1})
        expected_data_1 = ShopSerializer([self.fixture_shop_1, self.fixture_shop_2,
                                          self.fixture_shop_3, self.fixture_shop_4], many=True).data
        expected_data_2 = ShopSerializer([self.fixture_shop_1, self.fixture_shop_2], many=True).data
        expected_data_3 = ShopSerializer([self.fixture_shop_3, self.fixture_shop_4], many=True).data
        expected_data_4 = ShopSerializer([self.fixture_shop_3], many=True).data
        expected_data_5 = ShopSerializer([self.fixture_shop_4], many=True).data
        expected_data_6 = ShopSerializer([self.fixture_shop_1, self.fixture_shop_4], many=True).data
        expected_data_7 = ShopSerializer([self.fixture_shop_2, self.fixture_shop_3], many=True).data
        expected_data_8 = ShopSerializer([self.fixture_shop_2], many=True).data
        self.assertEqual(HTTPStatus.OK, response_1.status_code)
        self.assertEqual(HTTPStatus.OK, response_2.status_code)
        self.assertEqual(HTTPStatus.OK, response_3.status_code)
        self.assertEqual(HTTPStatus.OK, response_4.status_code)
        self.assertEqual(HTTPStatus.OK, response_5.status_code)
        self.assertEqual(HTTPStatus.OK, response_6.status_code)
        self.assertEqual(HTTPStatus.OK, response_7.status_code)
        self.assertEqual(HTTPStatus.OK, response_8.status_code)
        self.assertEqual(expected_data_1, response_1.data)
        self.assertEqual(expected_data_2, response_2.data)
        self.assertEqual(expected_data_3, response_3.data)
        self.assertEqual(expected_data_4, response_4.data)
        self.assertEqual(expected_data_5, response_5.data)
        self.assertEqual(expected_data_6, response_6.data)
        self.assertEqual(expected_data_7, response_7.data)
        self.assertEqual(expected_data_8, response_8.data)
