import os
import time
from datetime import datetime

from django.db import transaction

from config.settings import BASE_DIR
from parsing.parsers import Parsing
from .settings import DEFAULT_IMG_PATH, GOODS_IMAGE_PATH
from .forms import LinkForm
from .models import RunningTask


def relative_path(path):
    """Вовзращает относительный путь от корневой директории проекта
    :param path: абсолютный путь к файлу или папке
    :return: относительный путь к файлу или папке
    """
    return os.path.relpath(os.path.abspath(path), BASE_DIR)


def get_sites_and_url_form():
    products = Product.objects.all()
    for product in products:
        last_price = product.last_price
        product.is_running = product.task_is_running
        product.price_rub = f'{last_price.price} руб.' if last_price else '-'
        product.photo_path = (
            relative_path(os.path.join(GOODS_IMAGE_PATH, product.photo_path))
            if product.photo_path else DEFAULT_IMG_PATH)
    data = {'products': products, 'form': LinkForm()}
    return data

def add_message_to_context(context, message=None):
    context['has_message'] = False if message is None else True
    if message:
        context['message'] = message
    return context


def add_link(url):
    site = Product.add_ref_link(url)
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


def calculate_time(fun):
    def calculate(url_param):
        t = time.time()
        result = fun(url_param)
        print(f'Время на обработку запроса - {time.time() - t} секунд')
        return result
    return calculate


class SiteTaskContextManager:
    """Менеджер контекста для создания задач обновления данных сайтов
     и для вывода информации при запуске и завершении задач"""
    def __init__(self, product):
        self.product = product

    def __enter__(self):
        print('---------------------------------------------')
        print(f'Задача обновления данных сайта '
              f'(id={self.product.id}) была запущена!')
        RunningTask.create_task_for_product(self.product)

    def __exit__(self, exc_type, exc_val, exc_tb):
        RunningTask.delete_task_for_site(self.product)
        print('---------------------------------------------')


@transaction.atomic
def run_price_task(product_id):
    """Запускает задачу по обновлению цены и фото для сайта"""

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        print(f'Товар с id = {product_id} не существует!')
        return

    if product.task_is_running:
        print(f'Задача для обновления цены товара '
              'с id = {product_id} уже запущена!')
        return

    with SiteTaskContextManager(product=product):
        price, photo_name = Parsing(product.url).parse_data()
        print(f'Price - {price}; Photo - {photo_name}')
        product.add_price_and_photo(price, photo_name)
