# Generated by Django 3.0.3 on 2020-04-11 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parsing', '0008_auto_20200322_1616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='price',
            name='product',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='runningtask',
            name='product',
            field=models.IntegerField(),
        ),
    ]
