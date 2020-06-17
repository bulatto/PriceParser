# Generated by Django 3.0.3 on 2020-03-22 13:16

from django.conf import settings
from django.db import migrations
from django.db import models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('parsing', '0007_auto_20200321_2148'),
    ]

    operations = [
        migrations.RenameField(
            model_name='price',
            old_name='site',
            new_name='product',
        ),
        migrations.RenameField(
            model_name='runningtask',
            old_name='site',
            new_name='product',
        ),
        migrations.AlterField(
            model_name='product',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='price',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                    related_name='prices',
                                    to='parsing.Product'),
        ),
        migrations.RenameField(
            model_name='price',
            old_name='date',
            new_name='created',
        ),
        migrations.AlterField(
            model_name='price',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='price',
            name='price',
            field=models.FloatField(),
        ),
    ]
