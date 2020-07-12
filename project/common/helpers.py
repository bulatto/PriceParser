import datetime
import os
import urllib.parse as urlparse

from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.paginator import Paginator

from config.settings.base import BASE_DIR


# Символы скобок, которые используются в конфигурации
open_brackets, close_brackets = '([', ')]'


def relative_path(path):
    """Возвращает относительный путь от корневой директории проекта
    :param path: абсолютный путь к файлу или папке
    :return: относительный путь к файлу или папке
    """
    return os.path.relpath(os.path.abspath(path), BASE_DIR)


def check_or_create_dir(directory):
    """Если директория не существует, то она создаётся"""
    if not os.path.exists(directory):
        os.mkdir(directory)


def get_datetime_string(datetime_object):
    """Возвращает строковое представление даты и времени"""
    if isinstance(datetime_object, datetime.datetime):
        return datetime_object.strftime("%d.%m.%Y %H:%M:%S")
    elif isinstance(datetime_object, datetime.date):
        return datetime_object.strftime("%d.%m.%Y")


def check_parentheses_in_string(string):
    """Проверяет закрытость и порядок скобок в строке.
    Возвращает True, если все хорошо, иначе False

    :param string: Строка, которую необходимо проверить
    :return: Корректность расстановки скобок (True/False)
    """
    parentheses = []
    for ch in (c for c in string if c in open_brackets + close_brackets):
        if ch in open_brackets:
            parentheses.append(ch)
        else:
            if not parentheses or (parentheses.pop() != open_brackets[
                    close_brackets.index(ch)]):
                return False
    return not parentheses


def pagination_page(objects, page, objects_on_page, page_dif=3):
    """Получение объекта страницы с объектами

    :param objects: Запрос к модели
    :param page: Номер страницы
    :param objects_on_page: Количество объектов на странице
    :param page_dif: Количество страниц, которое будет отображено на сайте,
        слева и справа от текущей страницы

    :return: Объект пагинации
    """

    paginator = Paginator(objects, objects_on_page)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        # Если страница не является целым числом, поставим первую страницу
        page_obj = paginator.page(1)
    except EmptyPage:
        # Если страница больше максимальной,
        # возврат последнюю страницу результатов
        page_obj = paginator.page(paginator.num_pages)

    page_obj.page_nums_for_html = (
        p for p in paginator.page_range if abs(page_obj.number - p) <= page_dif)
    return page_obj


def add_get_param_to_url(url, param_dict):
    """Добавляется к запросу необходимые GET параметры

    :param url: URL запроса
    :param param_dict: Словарь с параметрами для добавления

    :return: Новый получившийся URL адрес
    """
    url_parts = list(urlparse.urlparse(url))
    query_params_dict = dict(urlparse.parse_qsl(url_parts[4]))
    # Добавление параметра к другими параметрам
    query_params_dict.update(param_dict)
    url_parts[4] = urlparse.urlencode(query_params_dict)
    # Готовый URL
    new_url = urlparse.urlunparse(url_parts)
    return new_url
