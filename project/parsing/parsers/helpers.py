from time import sleep

from django.core.exceptions import ImproperlyConfigured

from parsing.enum import IdentifierEnum


def open_parser(function):
    """Декоратор для открытия парсера с возможностью повторной попытки"""
    def fun(self):
        for i in range(2):
            try:
                function(self)
                break
            except Exception as e:
                print(f'Произошла ошибка при открытии сайта! {e}')
            sleep(1)
    return fun


def get_identifier(string):
    """Находит идентификатор в начале строки или генерирует ошибку
    :param string: Строка с идентификатором и параметром функции
    :type string: str
    :raise: ImproperlyConfigured
    """
    assert string, "Строка пуста!"
    # TODO: можно улучшить функцию

    for key, value in IdentifierEnum.str_to_identifier.items():
        if string.startswith(key):
            return key, value
    raise ImproperlyConfigured(
        f'Идентификатор не был найден в начале строки "{string}"')


def get_num_of_list(elem_list, num):
    """Возвращается num-ый по счёту элемент массива"""
    assert isinstance(elem_list, list)

    if 0 <= num <= len(elem_list):
        try:
            return elem_list[num]
        except IndexError as e:
            print('Индекс вышел за границы массива!')

    return None
