from django.contrib.auth.models import User
from django.test import TestCase

from store.models import Product
from store.serializers import ProductSerializer


class ProductSerializerTestCase(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(username='test_user')

    def test_ok(self):
        product_1 = Product.objects.create(name='book_1', price=26, owner=self.user)
        product_2 = Product.objects.create(name='book_2', price=27, owner=self.user)
        data = ProductSerializer([product_1, product_2], many=True).data
        expected_data = [
            {
                'id': product_1.id,
                'name': 'book_1',
                'price': '26.00',
                'owner': self.user.id
            },
            {
                'id': product_2.id,
                'name': 'book_2',
                'price': '27.00',
                'owner': self.user.id
            }
        ]
        self.assertEqual(expected_data, data)