from time import sleep

from django.core.exceptions import ImproperlyConfigured

from parsing.parsers.constants import IdentifierEnum


def open_parser(function):
    """Декоратор для открытия парсера с возможностью повторной попытки"""
    def fun(self):
        for i in range(2):
            try:
                function(self)
                break
            except:
                print('Произошла ошибка при открытии сайта!')
            sleep(1)
    return fun


def get_identifier(string):
    """Находит идентификатор в начале строки или генерирует ошибку
    :param string: Строка с идентификатором и параметром функции
    :type string: str
    :raise: ImproperlyConfigured
    """
    assert string, "Строка пуста!"

    for key, value in IdentifierEnum.str_to_identifier.items():
        if string.startswith(key):
            return key, value
    raise ImproperlyConfigured(
        f'Идентификатор не был найден в начале строки "{string}"')