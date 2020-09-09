import os

from config.settings.base import DEFAULT_IMG_NAME
from config.settings.base import GOODS_IMAGE_PATH
from product.models import Product


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
