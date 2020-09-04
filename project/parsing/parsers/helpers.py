from time import sleep
from typing import Optional
import re

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


def price_processing(string: str) -> Optional[float]:
    """Функция нахождения цены в строке и перевода её в вещественный тип.
    При отсутствии цены или невозможности её преобразовать возвращается None

    :param string: Исходная строка
    :return: По возможности возвращается найденная цена в строке либо None
    """
    rub_strings = ['руб.', '₽', 'р.', 'руб']
    positions = [string.find(st) for st in rub_strings]
    pos = next((pos for pos in positions if pos >= 0), None)
    if pos:
        string = string[:pos]
    result = re.search(r'\d{1,3}\s*\d{2,3}([\.,]\s?(?:\d{1,2}))?', string)
    if result:
        # Убираем посторонние символы
        price_string = result.string.replace(',', '.')
        price_string = ''.join(
            [ch for ch in price_string if ch.isdigit() or ch == '.'])

        try:
            price = float(price_string)
        except ValueError:
            price = None

        return price
