from django.contrib.auth.models import User
from django.db import models
from django.db import transaction

from common.helpers import get_datetime_string


class Product(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='product',
        verbose_name='Пользователь')
    url = models.URLField(verbose_name='Ссылка на товар')
    photo_path = models.CharField(
        max_length=200, null=True, blank=True,
        verbose_name='Изображение товара')

    def __str__(self):
        return self.url

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def get_prices(self):
        return self.prices.order_by('created')

    @property
    def last_price(self):
        return self.get_prices().last()

    @transaction.atomic
    def add_price_and_photo(self, price, photoname):
        if price:
            self.prices.create(price=price)
            if photoname:
                self.photo_path = photoname
                self.save()
            return True
        else:
            print(f'Цена - {price}  и фото - {photoname} '
                  f'не были добавлены для сайта (id={self.id})')
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
            return None


class Price(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='prices',
        verbose_name='Ссылка на товар')
    price = models.FloatField(verbose_name='Цена')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    def __str__(self):
        return (f'Цена на товар(id={str(self.product.id)}, '
                f'дата={get_datetime_string(self.created)}) = '
                f'{self.price} руб.')

    class Meta:
        verbose_name = 'Цена'
        verbose_name_plural = 'Цены'
