import pytz
from django.utils import timezone
from django.db import models, transaction

from parsing.constants import TASK_TIMEOUT
from product.models import Product


class RunningTask(models.Model):
    """Задача обновления данных сайта"""
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='running_tasks')
    is_active = models.BooleanField(
        default=True, verbose_name='Активность задачи')
    start_time = models.DateTimeField(
        auto_now_add=True, verbose_name='Время начала задачи')
    end_time = models.DateTimeField(
        null=True, blank=True, default=None,
        verbose_name='Время завершения задачи')

    @classmethod
    def create_task_for_product(cls, product):
        cls.objects.create(product=product, start_time=timezone.now())

    @classmethod
    def delete_task_for_site(cls, product):
        task = None
        try:
            task = cls.objects.get(product=product)
        except cls.DoesNotExist:
            print(f'Задача для сайта с id={product.id} не была найдена!')
            return
        task.delete()
