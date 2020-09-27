import os

from config.settings.base import DEFAULT_IMG_NAME
from config.settings.base import GOODS_IMAGE_PATH
from product.models import Product


GOODS_ON_PAGE = 30


def is_photo_exists(photo_name=None):
    """Проверяет, существует ли изображение товара с таким названием
    :param photo_name: Название файла картинки
    :return: Существует ли фото
    """
    return photo_name and os.path.exists(
        os.path.join(GOODS_IMAGE_PATH, photo_name))


def remove_product_photo(photo_name):
    """Удаляет существующее изображение товара с указанным названием
    :param photo_name: Название файла картинки
    :return: Произошло ли удаление
    """
    if not photo_name:
        return False

    path = os.path.join(GOODS_IMAGE_PATH, photo_name)
    if os.path.exists(path):
        os.remove(path)
        return True
    return False


def get_photo_path(photo_name=None):
    """Возвращает путь из папки со статикой до картинки, если задано корректное
    название файла и файл существует. Иначе выдаст путь до картинки по умолчанию
    :param photo_name: Название файла картинки
    :return: Путь от папки со статикой до картинки
    """
    prefix = os.path.split(GOODS_IMAGE_PATH)[-1]
    not_exists = photo_name and not is_photo_exists(photo_name)
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


def remove_unused_products_photo():
    """Удаление неиспользуемых файлов из папки с фото товаров для удаления"""

    products_query = Product.objects.filter(
        photo_path__isnull=False).exclude(photo_path='')
    images_names = list(products_query.values_list('photo_path', flat=True))

    # Удаление неиспользуемых файлов из папки с фото товаров для удаления
    images_for_deleting = [
        file_name for file_name in os.listdir(GOODS_IMAGE_PATH)
        if file_name not in images_names
           and file_name != DEFAULT_IMG_NAME]

    # TODO: Добавить запись в лог
    if images_for_deleting:
        print(f'\nФайлы для удаления (кол-во = {len(images_for_deleting)}):')
        print(images_for_deleting)

    for image in images_for_deleting:
        remove_product_photo(image)


def fix_photo_paths_in_products():
    """Исправление заполненных полей у продуктов, которые указывают на
    несуществующий файл (для этих продуктов поле photo_path становится None)
    """

    products_query = Product.objects.filter(
        photo_path__isnull=False).exclude(photo_path='')

    existed_files = os.listdir(GOODS_IMAGE_PATH)
    for product in products_query:
        if product.photo_path not in existed_files:
            product.photo_path = None
            product.save()
            # TODO: Добавить запись в лог
            print(f'Для товара с id={product.id} было очищено '
                  'поле с изображением')
