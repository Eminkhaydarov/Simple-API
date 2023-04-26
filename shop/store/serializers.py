from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from store.models import Product, UserProductRelation


class ProductSerializer(ModelSerializer):
    annoteted_likes = serializers.IntegerField(read_only=True)
    rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)
    owner_name = serializers.CharField(source='owner.username', default='', read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'owner', 'annoteted_likes', 'owner_name', 'rating')



class UserProductRelationSerializer(ModelSerializer):
    class Meta:
        model = UserProductRelation
        fields = ('product', 'like', 'in_bookmarks', 'rate')
