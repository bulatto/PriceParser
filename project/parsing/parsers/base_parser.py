from abc import ABCMeta
from abc import abstractmethod

from parsing.enum import IdentifierEnum

from .exceptions import *


class PageParser(metaclass=ABCMeta):
    url = None
    # Элемент, с которого начинается поиск
    where = None

    def try_get_element_on_page(self, elem_src):
        """Безопасное получение элемента на странице
        Не требует переопределения"""

        try:
            elem = self.get_element_on_page(elem_src)
            return elem
        except ElementNotFoundedOnPage(elem_src) as e:
            print(e.message)
            return None

    def get_page_elem(self, elem_src):
        """Расширенная обработка элемента. Позволяет задавать несколько типов
        идентификаторов, будет выбран первый ненулевой результат.
        Не требует переопределения
        :param elem_src: Тип и сам идентификатор
        :type elem_src: TypeAndId
        :raise: ElementNotFoundedOnPage
        """
        if isinstance(elem_src, list):
            for el_src in elem_src:
                elem = self.try_get_element_on_page(el_src)
                if elem:
                    return elem
            raise ElementNotFoundedOnPage()
        else:
            return self.get_element_on_page(elem_src)

    @abstractmethod
    def open(self):
        """Метод, выполняющийся при открытии сайта"""
        print(f'Открытие сайта {self.url}')

    def reset_where_to_find(self):
        """Обновляет место поиска для парсера"""
        pass

    def close(self):
        """Метод, выполняющийся при закрытии сайта"""
        print(f'Закрытие сайта {self.url}')

    @abstractmethod
    def get_identifier_functions(self):
        """Получение словаря с функциями для парсинга идентификаторов.
        Ключом словаря является id идентификатора,
        значением - кортеж, первый элемент которого - элемент, для которого
        вызывается функция, второй - сама функция или её название.
        Данные кортежи затем будут преобразованы в нормальные функции.
        Их преобразование см. в функции convert_function_from_tuple
        """
        pass

    @abstractmethod
    def get_supported_identifiers_list(self):
        """Получение списка идентификаторов, поддерживаемых для текущего
        элемента self.where
        """

    def convert_function_from_tuple(self, function_tuple):
        """Преобразование определённого кортежа в функцию"""
        if not isinstance(function_tuple, tuple):
            raise ValueError(
                'Неверный тип элемента для преобразования в функцию')
        element, func = function_tuple
        if element is None and callable(func):
            return func
        elif element:
            if element == 'where' and isinstance(func, str):
                return getattr(self.where, func)

        raise ValueError('Не удалось преобразовать элемент в функцию')

    def get_identifier_function(self, elem_src):
        """Возвращает функцию для парсинга конкретного элемента
        :param elem_src: Тип идентификатора и сам идентификатор
        :return: Фунция для парсинга элемента
        :raise: ElementNotFoundedOnPage
        """
        identifier_functions = self.get_supported_identifier_functions()
        function_tuple = identifier_functions.get(elem_src.type)
        if not function_tuple:
            print('Подходящая функция не была найдена.')
            raise ElementNotFoundedOnPage(elem_src)
        return self.convert_function_from_tuple(function_tuple)

    def get_supported_identifier_functions(self):
        """Получение словаря только с функциями, поддерживаемыми для текущего
        элемента self.where. В данной функции можно переопределить ограничения
        на функции и идентификаторы
        """
        supported_identifiers = self.get_supported_identifiers_list()
        result_dict = {}
        identifier_functions = self.get_identifier_functions()
        for identificator in supported_identifiers:
            if identificator in identifier_functions:
                result_dict[identificator] = identifier_functions[
                    identificator]
        return result_dict

    @abstractmethod
    def get_param_for_identifier_function(self, function, elem_src):
        """Возвращает словарь параметров для передачи в функцию
        получения идентификатора
        :param elem_src: Тип идентификатора и сам идентификатор
        :type elem_src: TypeAndId
        :param elem_src: Функция для получения идентификатора
        :return args, kwargs: Неименованные/именованные аргументы для функции
        :raise BaseParsingException
        """
        pass

    def get_element_on_page(self, elem_src):
        """ Получение элемента на странице согласно идентификатору
        :param elem_src: Тип идентификатора и сам идентификатор
        :type elem_src: TypeAndId

        :return: Искомый элемент страницы
        :rtype: Any

        :raise: WrongIdentifier, ElementNotFoundedOnPage
        """
        print(f'Type={IdentifierEnum.values[elem_src.type]}, id={elem_src.id}')
        function = self.get_identifier_function(elem_src)
        args, kwargs = self.get_param_for_identifier_function(
            function, elem_src)
        result = function(*args, **kwargs)
        print(f'Результат парсинга={result}')
        if not result:
            raise ElementNotFoundedOnPage()

        self.where = result
        return result
