import os

from django.contrib.auth.models import User
from django.db import models
from django.db import transaction

from common.helpers import get_datetime_string
from common.models import CreatedDateMixin
from common.models import DateAwareMixin
from config.settings.base import GOODS_IMAGE_PATH
from product.model_managers import ProductPriceManager


class Product(DateAwareMixin):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='product',
        verbose_name='Пользователь')
    url = models.URLField(verbose_name='Ссылка на товар')
    photo_path = models.CharField(
        max_length=200, null=True, blank=True,
        verbose_name='Изображение товара')
    objects = models.Manager()
    products_with_prices = ProductPriceManager()

    def __str__(self):
        return f'(id={self.id}) {self.url}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def get_prices(self):
        return self.prices.order_by('created')

    @property
    def last_price(self):
        return self.get_prices().last()

    @transaction.atomic
    def add_price_and_photo(self, price, photoname=None):
        if self.photo_is_needed and photoname:
            self.photo_path = photoname
            self.save()
            print(f'Фото {photoname} добавлено для продукта (id={self.id})')
        if price:
            self.prices.create(price=price)
            return True
        else:
            print(f'Цена {price} не была добавлена для продукта (id={self.id})')
            return False

    @classmethod
    def create_product(cls, url):
        return Product.objects.create(
            user=User.objects.get(username='admin'), url=url)

    @classmethod
    def delete_by_id(cls, id):
        try:
            Product.objects.get(id=id).delete()
            return True
        except cls.DoesNotExist as e:
            print('Сайт с таким id не был найден. Удаление не выполнено.')

    @property
    def photo_is_needed(self):
        """Нужно ли фото для данного продукта, зависит от заполненности поля
        photo_path и корректности указанного пути"""
        return not self.photo_path or not os.path.exists(
            os.path.join(GOODS_IMAGE_PATH, self.photo_path))


class Price(CreatedDateMixin):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='prices',
        verbose_name='Ссылка на товар')
    price = models.FloatField(verbose_name='Цена')

    def __str__(self):
        return (f'Цена на товар(id={str(self.product.id)}, '
                f'дата={get_datetime_string(self.created)}) = '
                f'{self.price} руб.')

    class Meta:
        verbose_name = 'Цена'
        verbose_name_plural = 'Цены'
