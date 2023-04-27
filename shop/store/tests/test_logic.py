from django.contrib.auth.models import User
from django.test import TestCase

from store.logic import set_rating
from store.models import Product, UserProductRelation


class SetRatingTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username='test_user')
        self.user_2 = User.objects.create(username='test_user_2')
        self.user_3 = User.objects.create(username='test_user_3')
        self.product_1 = Product.objects.create(name='book_1', price=26, owner=self.user)

        UserProductRelation.objects.create(user=self.user, product=self.product_1, like=True, rate=5)
        UserProductRelation.objects.create(user=self.user_2, product=self.product_1, like=True, rate=5)
        UserProductRelation.objects.create(user=self.user_3, product=self.product_1, like=True, rate=4)

    def test_ok(self):
        set_rating(self.product_1)
        self.product_1.refresh_from_db()
        self.assertEqual('4.67', str(self.product_1.rating))
