import os

from common.helpers import relative_path
from parsing.models import RunningTask
from product.forms import UrlForm
from config.settings import GOODS_IMAGE_PATH, DEFAULT_IMG_NAME
from product.models import Product


def get_photo_path(photo_name=None):
    """Возвращает путь от корня проекта до картинки, если задано корректное
    название файла и файл существует. Иначе выдаст путь до картинки по умолчанию
    :param photo_name: Название файла картинки
    :return: Путь от корня проекта до картинки
    """
    if photo_name:
        full_path = os.path.join(GOODS_IMAGE_PATH, photo_name)
    if not photo_name or not os.path.exists(full_path):
        full_path = os.path.join(GOODS_IMAGE_PATH, DEFAULT_IMG_NAME)
    return relative_path(full_path)


def get_sites_and_url_form():
    """Получение данных для страницы со всеми товарами"""
    products = Product.objects.all()
    for product in products:
        last_price = product.last_price
        product.is_running = RunningTask.has_active_task(product)
        product.price_in_rub = f'{last_price.price} руб.' if last_price else '-'
        product.photo_path = get_photo_path(product.photo_path)
    data = {'products': products, 'form': UrlForm()}
    return data


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
