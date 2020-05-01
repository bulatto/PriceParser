import os
import datetime

from config.settings.base import BASE_DIR


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
