from django.contrib.auth.models import User
from django.db import models, transaction


class Product(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='product')
    url = models.URLField()
    photo_path = models.CharField(max_length=200, null=True, blank=True)

    def get_prices(self):
        return self.prices.order_by('date')

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
    def add_ref_link(cls, link):
        try:
            site = Product.objects.create(
                user=User.objects.get(username='admin'), url=link)
            return site.id
        except Exception as e:
            print('Добавление ссылки не удалось.' + str(e))
            return None

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
        Product, on_delete=models.CASCADE, related_name='prices')
    price = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)
