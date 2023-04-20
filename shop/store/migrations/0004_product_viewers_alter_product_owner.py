# Generated by Django 4.2 on 2023-04-19 11:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0003_userproductrelation'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='viewers',
            field=models.ManyToManyField(related_name='products', through='store.UserProductRelation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='product',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='my_product', to=settings.AUTH_USER_MODEL),
        ),
    ]
