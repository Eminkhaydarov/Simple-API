from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from store.models import Product
from store.serializers import ProductSerializer


class ProductApiTestCase(APITestCase):
    def setUp(self) -> None:
        self.product_1 = Product.objects.create(name='book_1', price=26)
        self.product_2 = Product.objects.create(name='book_2', price=27)
        self.product_3 = Product.objects.create(name='book 27.00', price=26)

    def test_get(self):
        url = reverse('product-list')
        serializer_data = ProductSerializer([self.product_1, self.product_2, self.product_3], many=True).data
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_filter(self):
        url = reverse('product-list')
        serializer_data = ProductSerializer([self.product_1, self.product_3], many=True).data
        response = self.client.get(url, data={'price': '26.00'})
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_search(self):
        url = reverse('product-list')
        serializer_data = ProductSerializer([self.product_2, self.product_3], many=True).data
        response = self.client.get(url, data={'search': '27.00'})
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_order(self):
        url = reverse('product-list')
        serializer_data = ProductSerializer([self.product_1, self.product_3, self.product_2,], many=True).data
        response = self.client.get(url, data={'ordering': 'price'})
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
        response = self.client.get(url, data={'ordering': '-price'})
        serializer_data = ProductSerializer([self.product_2, self.product_1, self.product_3,], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)