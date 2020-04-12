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
    def has_active_task(cls, product):
        return cls.objects.filter(product=product, is_active=True).exists()

    @classmethod
    def close_task_by_id(cls, id):
        try:
            cls.objects.filter(id=id).update(
                is_active=False, end_time=timezone.now())
        except cls.DoesNotExist:
            pass
