from django.contrib import admin

from . import models


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'created', 'modificated', 'url', 'photo_path']


@admin.register(models.Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ['id', 'created', 'product', 'price']
