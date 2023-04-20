from django.contrib import admin
# Register your models here.
from django.contrib.admin import ModelAdmin

from store.models import Product, UserProductRelation


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    pass


@admin.register(UserProductRelation)
class UserProductRelationAdmin(ModelAdmin):
    pass
