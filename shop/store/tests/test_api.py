import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase

from store.models import Product
from store.serializers import ProductSerializer


class ProductApiTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username='test_user')
        self.product_1 = Product.objects.create(name='book_1', price=26, owner=self.user)
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
        self.assertEqual(self.user, Product.objects.last().owner)

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

    def test_update_not_owner(self):
        self.user_2 = User.objects.create(username='test_user_2')
        self.client.force_login(self.user_2)
        url = reverse('product-detail', args=(self.product_1.id,))
        data = {"name": "book_1",
                "price": 375}
        json_data = json.dumps(data)
        response = self.client.put(url,
                                   data=json_data,
                                   content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.product_1.refresh_from_db()
        self.assertEqual(26, self.product_1.price)
        self.assertEqual({'detail': ErrorDetail(string='You do not have permission to perform this action.', code='permission_denied')}, response.data)

    def test_update_not_owner_but_staff(self):
        self.user_2 = User.objects.create(username='test_user_2',
                                          is_staff=True)
        self.client.force_login(self.user_2)
        url = reverse('product-detail', args=(self.product_1.id,))
        data = {"name": "book_1",
                "price": 375}
        json_data = json.dumps(data)
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

    def test_delete_not_owner(self):
        self.assertEqual(3, Product.objects.all().count())
        url = reverse('product-detail', args=(self.product_1.id,))
        self.user_2 = User.objects.create(username='test_user_2')
        self.client.force_login(self.user_2)
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(3, Product.objects.all().count())
        self.assertEqual({'detail': ErrorDetail(string='You do not have permission to perform this action.',
                                                code='permission_denied')}, response.data)

    def test_delete_not_owner_but_staff(self):
        self.assertEqual(3, Product.objects.all().count())
        url = reverse('product-detail', args=(self.product_1.id,))
        self.user_2 = User.objects.create(username='test_user_2', is_staff=True)
        self.client.force_login(self.user_2)
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


class ProductRelationApiTestCase(APITestCase):
    def setUp(self) -> None:
        self.user_1 = User.objects.create(username='test_user_1')
        self.user_2 = User.objects.create(username='test_user_2')
        self.product_1 = Product.objects.create(name='book_1', price=26, owner=self.user)
        self.product_2 = Product.objects.create(name='book_2', price=27)
        self.product_3 = Product.objects.create(name='book 27.00', price=26)

    def test_get(self):
        url = reverse('userproductrelation-detail', args=(self.product_1.id,))
        self.client.force_login(self.user_1)
        data = {"like": True}
        json_data = json.dumps(data)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.product_1.refresh_from_db()

        self.assertTrue(self.product_1.like)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

