from django.contrib.auth.models import User
from django.db.models import Count, Case, When, Avg
from django.test import TestCase

from store.models import Product, UserProductRelation
from store.serializers import ProductSerializer


class ProductSerializerTestCase(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(username='test_user')
        self.user_2 = User.objects.create(username='test_user_2')
        self.user_3 = User.objects.create(username='test_user_3')

    def test_ok(self):
        product_1 = Product.objects.create(name='book_1', price=26, owner=self.user)
        product_2 = Product.objects.create(name='book_2', price=27, owner=self.user)

        UserProductRelation.objects.create(user=self.user, product=product_1, like=True, rate=5)
        UserProductRelation.objects.create(user=self.user_2, product=product_1, like=True, rate=5)
        UserProductRelation.objects.create(user=self.user_3, product=product_1, like=True, rate=4)

        UserProductRelation.objects.create(user=self.user, product=product_2, like=True, rate=3)
        UserProductRelation.objects.create(user=self.user_2, product=product_2, like=True, rate=4)
        UserProductRelation.objects.create(user=self.user_3, product=product_2, like=False)
        products = Product.objects.all().annotate(
            annoteted_likes=Count(Case(When(userproductrelation__like=True, then=1))),
            rating=Avg('userproductrelation__rate')
            ).order_by('id')
        data = ProductSerializer(products, many=True).data
        expected_data = [
            {
                'id': product_1.id,
                'name': 'book_1',
                'price': '26.00',
                'owner': self.user.id,
                'annoteted_likes': 3,
                'rating': '4.67'
            },
            {
                'id': product_2.id,
                'name': 'book_2',
                'price': '27.00',
                'owner': self.user.id,
                'annoteted_likes': 2,
                'rating': '3.50'
            }
        ]
        self.assertEqual(expected_data, data)
