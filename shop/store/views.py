from django.db.models import Count, Case, When, Avg
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from store.models import Product, UserProductRelation
from store.permissions import IsOwnerOrIsStaffOrReadOnly
from store.serializers import ProductSerializer, UserProductRelationSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all().annotate(
            annoteted_likes=Count(Case(When(userproductrelation__like=True, then=1))),
            rating=Avg('userproductrelation__rate')
            ).order_by('id')
    serializer_class = ProductSerializer
    permission_classes = [IsOwnerOrIsStaffOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['price']
    search_fields = ['name', 'price']
    ordering_field = ['name', 'price']

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        serializer.save()


def auth(request):
    return render(request, 'OAuth.html')


class UserProductRelationViewSet(mixins.UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserProductRelation.objects.all()
    serializer_class = UserProductRelationSerializer
    lookup_field = 'product'

    def get_object(self):
        obj, _ = UserProductRelation.objects.get_or_create(user=self.request.user,
                                                                  product_id=self.kwargs['product'])
        return obj