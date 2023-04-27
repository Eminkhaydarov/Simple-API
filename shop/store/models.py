from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='my_product')
    viewers = models.ManyToManyField(User, through='UserProductRelation', related_name='products')
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, default=None)

    def __str__(self):
        return f'ID {self.id}: {self.name}'


class UserProductRelation(models.Model):
    RATE_CHOICES = (
        (1, 'Ok'),
        (2, 'Fine'),
        (3, 'Good'),
        (4, 'Amazing'),
        (5, 'Incredible'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    in_bookmarks = models.BooleanField(default=False)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES, null=True)

    def __str__(self):
        return f'{self.user.username}: {self.product.name}, RATE {self.rate}'

    def __init__(self, *args, **kwargs):
        super(UserProductRelation, self).__init__(*args, **kwargs)
        self.old_rate = self.rate

    def save(self, *args, **kwargs):
        creating = not self.pk
        super().save(*args, **kwargs)

        if self.old_rate != self.rate or creating:
            from store.logic import set_rating
            set_rating(self.product)
