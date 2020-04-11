import pytz

from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models, transaction

from parsing.constants import TASK_TIMEOUT


class Site(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='site')
    url = models.URLField()
    photo_path = models.CharField(max_length=200, null=True, blank=True)

    def get_prices(self):
        return Price.objects.filter(site=self).order_by('-date')

    @property
    def last_price(self):
        prices = self.get_prices()
        return prices.first()

    @transaction.atomic
    def add_price_and_photo(self, price, photoname):
        if price:
            Price.add(site=self, price=price)
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
            site = Site.objects.create(
                user=User.objects.get(username='admin'), url=link)
            return site.id
        except Exception as e:
            print('Добавление ссылки не удалось.' + str(e))
            return None

    @classmethod
    def delete_by_id(cls, id):
        try:
            Site.objects.get(id=id).delete()
            return True
        except cls.DoesNotExist as e:
            print('Сайт с таким id не был найден. Удаление не выполнено.')
            return None

    @property
    def task_is_running(self):
        return RunningTask.objects.filter(site=self).exists()

    @property
    def is_task_out_of_date(self):
        if self.task_is_running:
            start_time = RunningTask.objects.get(site=self).start_time
            delta_time = timezone.now() - start_time
            return delta_time > TASK_TIMEOUT
        else:
            return False

    def run_task_for_price(self):
        pass


class Price(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    price = models.IntegerField()
    date = models.DateTimeField()

    @classmethod
    def add(cls, site, price):
        cls.objects.create(site=site, price=price, date=timezone.now())


class RunningTask(models.Model):
    """Задача обновления данных сайта"""
    site = models.OneToOneField(Site, on_delete=models.CASCADE)
    start_time = models.DateTimeField(verbose_name='Время начала задачи')

    @classmethod
    def create_task_for_site(cls, site):
        cls.objects.create(site=site, start_time=timezone.now())

    @classmethod
    def delete_task_for_site(cls, site):
        task = None
        try:
            task = cls.objects.get(site=site)
        except cls.DoesNotExist:
            print(f'Задача для сайта с id={site.id} не была найдена!')
            return
        task.delete()
