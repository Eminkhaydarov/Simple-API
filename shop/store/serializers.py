from rest_framework.serializers import ModelSerializer

from store.models import Product, UserProductRelation


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class UserProductRelationSerializer(ModelSerializer):
    class Meta:
        model = UserProductRelation
        fields = ('product', 'like', 'in_bookmarks', 'rate')
