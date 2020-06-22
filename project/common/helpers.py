import datetime
import os

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
