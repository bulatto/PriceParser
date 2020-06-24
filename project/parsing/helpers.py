import time

from django.db import transaction

from parsing.parsers import Parsing
from product.models import Product

from .models import RunningTask


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
        self.task = None

    def __enter__(self):
        print('---------------------------------------------')
        print(f'Задача обновления данных сайта '
              f'(id={self.product.id}) была запущена!')
        self.task = RunningTask.objects.create(product=self.product)

    def __exit__(self, exc_type, exc_val, exc_tb):
        RunningTask.close_task_by_id(self.task.id)
        print('---------------------------------------------')


@transaction.atomic
def run_price_task(product_id):
    """Запускает задачу по обновлению цены и фото для сайта"""

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        print(f'Товар с id = {product_id} не существует!')
        return

    if RunningTask.has_active_task(product):
        print(f'Задача для обновления цены товара '
              'с id = {product_id} уже запущена!')
        return

    with SiteTaskContextManager(product=product):
        price, photo_name = Parsing(
            product.url, product.photo_is_needed).parse()
        print(f'Price - {price}; Photo - {photo_name}')
        product.add_price_and_photo(price, photo_name)
