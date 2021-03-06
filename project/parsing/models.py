from django.db import models
from django.db import transaction
from django.utils import timezone
import pytz

from common.helpers import get_datetime_string
from parsing.constants import TASK_TIMEOUT
from product.models import Product


class RunningTask(models.Model):
    """Задача обновления данных сайта"""
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='running_tasks',
        verbose_name='Ссылка на товар')
    is_active = models.BooleanField(
        default=True, verbose_name='Активность задачи')
    start_time = models.DateTimeField(
        auto_now_add=True, verbose_name='Время начала задачи')
    end_time = models.DateTimeField(
        null=True, blank=True, default=None,
        verbose_name='Время завершения задачи')

    def __str__(self):
        end_time = (
            '...' if self.is_active else get_datetime_string(self.end_time))
        return (f'id={self.id}, id_продукта={str(self.product.id)}'
                f'({get_datetime_string(self.start_time)}-{end_time})')

    class Meta:
        verbose_name = 'Задача для обновления данных о товаре'
        verbose_name_plural = 'Задачи для обновления данных о товаре'

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
