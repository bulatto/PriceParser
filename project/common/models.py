from django.db import models
from django.db.models import DateTimeField


class CreatedDateMixin(models.Model):
    """Добавление даты создания в модель"""

    created = DateTimeField(
        auto_now_add=True, verbose_name='Дата создания записи')

    class Meta:
        abstract = True


class ModificatedDateMixin(models.Model):
    """Добавление даты последнего изменения в модель"""

    modificated = DateTimeField(
        auto_now=True, verbose_name='Дата последнего изменения')

    class Meta:
        abstract = True


class DateAwareMixin(CreatedDateMixin, ModificatedDateMixin):
    """Добавление даты создания записи и последнего изменения в модель"""

    class Meta:
        abstract = True
