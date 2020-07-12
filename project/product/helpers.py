import os

from config.settings.base import DEFAULT_IMG_NAME
from config.settings.base import GOODS_IMAGE_PATH
from parsing.models import RunningTask
from product.forms import UrlForm
from product.models import Product, Price


GOODS_ON_PAGE = 30


def get_photo_path(photo_name=None):
    """Возвращает путь из папки со статикой до картинки, если задано корректное
    название файла и файл существует. Иначе выдаст путь до картинки по умолчанию
    :param photo_name: Название файла картинки
    :return: Путь от папки со статикой до картинки
    """
    prefix = os.path.split(GOODS_IMAGE_PATH)[-1]
    not_exists = photo_name and not os.path.exists(
        os.path.join(GOODS_IMAGE_PATH, photo_name))
    if not photo_name or not_exists:
        photo_name = DEFAULT_IMG_NAME
    return f'{prefix}/{photo_name}'


def convert_price_to_string(price):
    """Преобразует вещественную цену в строку (при возможности). Если число
    целое, то дробная часть откидывается, иначе идёт округление до 2 знаков,
    после запятой. Если на вход подаётся None, возвращается пустая строка

    :param price: Цена в вещественном виде
    :return: Строка для вывода
    """
    assert price is None or isinstance(price, float)

    if not price:
        return ''
    elif price % 1 == 0:
        return "{:.0f}".format(price)
    else:
        return "{:.2f}".format(price)


def get_sites_and_url_form(products):
    """Получение данных для страницы со всеми товарами"""

    # Определение продуктов с запущенными задачами
    product_ids = [product.id for product in products]
    products_with_running_task = frozenset(RunningTask.objects.filter(
        product__in=product_ids, is_active=True).values_list(
        'product_id', flat=True))

    for product in products:
        product.has_running_task = product.id in products_with_running_task
        product.price_str = convert_price_to_string(product.current_price)
        product.photo_path = get_photo_path(product.photo_path)

    return {'products': products, 'form': UrlForm()}


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
