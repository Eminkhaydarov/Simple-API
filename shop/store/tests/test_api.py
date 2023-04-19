import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from store.models import Product
from store.serializers import ProductSerializer


class ProductApiTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username='test_user')
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
        serializer_data = ProductSerializer([self.product_1, self.product_3, self.product_2, ], many=True).data
        response = self.client.get(url, data={'ordering': 'price'})
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
        response = self.client.get(url, data={'ordering': '-price'})
        serializer_data = ProductSerializer([self.product_2, self.product_1, self.product_3, ], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        self.assertEqual(3, Product.objects.all().count())
        url = reverse('product-list')
        data = {"name": "mouse",
                "price": 150}
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(url,
                                    data=json_data,
                                    content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, Product.objects.all().count())

    def test_update(self):
        url = reverse('product-detail', args=(self.product_1.id,))
        data = {"name": "book_1",
                "price": 375}
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.put(url,
                                    data=json_data,
                                    content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.product_1.refresh_from_db()
        self.assertEqual(375, self.product_1.price)

    def test_delete(self):
        self.assertEqual(3, Product.objects.all().count())
        url = reverse('product-detail', args=(self.product_1.id,))
        self.client.force_login(self.user)
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(2, Product.objects.all().count())

    def test_detail_read(self):
        serializer_data = ProductSerializer(self.product_1).data
        url = reverse('product-detail', args=(self.product_1.id,))
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        self.assertEqual(serializer_data, response.data)
