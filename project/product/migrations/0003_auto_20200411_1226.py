# Generated by Django 3.0.3 on 2020-04-11 09:26

from django.db import migrations
from django.db import models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='price',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prices', to='product.Product'),
        ),
    ]
