from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from store.models import Product
from store.serializers import ProductSerializer


class ProductApiTestCase(APITestCase):
    def test_get(self):
        product_1 = Product.objects.create(name='book_1', price=26)
        product_2 = Product.objects.create(name='book_2', price=27)
        url = reverse('product-list')
        serializer_data = ProductSerializer([product_1, product_2], many=True).data
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
