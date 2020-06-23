import os

from django.db.models import Prefetch

from common.helpers import relative_path
from config.settings.base import DEFAULT_IMG_NAME
from config.settings.base import GOODS_IMAGE_PATH
from parsing.models import RunningTask
from product.forms import UrlForm
from product.models import Product, Price


GOODS_ON_PAGE = 30


def get_photo_path(photo_name=None):
    """Возвращает путь от корня проекта до картинки, если задано корректное
    название файла и файл существует. Иначе выдаст путь до картинки по умолчанию
    :param photo_name: Название файла картинки
    :return: Путь от корня проекта до картинки
    """
    full_path = None
    if photo_name:
        full_path = os.path.join(GOODS_IMAGE_PATH, photo_name)
    if not full_path or not os.path.exists(full_path):
        full_path = os.path.join(GOODS_IMAGE_PATH, DEFAULT_IMG_NAME)
    return relative_path(full_path)


def get_sites_and_url_form(page=1):
    """Получение данных для страницы со всеми товарами"""
    assert page > 0, 'Номер страницы должен быть больше нуля'

    products = Product.objects.all().prefetch_related(
        Prefetch('prices', queryset=Price.objects.order_by('-created')))
    products_list = list(products[:page*GOODS_ON_PAGE])

    # Определение продуктов с запущенными задачами
    product_ids = [product.id for product in products_list]
    products_with_running_task = frozenset(RunningTask.objects.filter(
        product__in=product_ids, is_active=True).values_list(
        'product_id', flat=True))

    for product in products_list:
        product.has_running_task = product.id in products_with_running_task
        last_price_obj = product.prices.first()
        product.price_in_rub = (f'{last_price_obj.price} руб.'
                                if last_price_obj else '-')
        product.photo_path = get_photo_path(product.photo_path)

    return {'products': products_list, 'form': UrlForm()}


def add_url(url):
    site = Product.create_product(url)
    if site:
        message = 'Ссылка успешно добавлена!'
    else:
        message = 'Ссылка не была добавлена из-за ошибки!'
    return bool(site), message


def delete_site(id):
    site = Product.delete_by_id(id)
    if site:
        message = 'Ссылка успешно удалена!'
    else:
        message = 'Ссылка не была удалена из-за ошибки!'
    return message
