from abc import ABCMeta
from abc import abstractmethod

from parsing.enum import IdentifierEnum

from .exceptions import *


class PageParser(metaclass=ABCMeta):
    url = None
    # Элемент, с которого начинается поиск
    where = None

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
        pass

    def parse_sequence(self, parsing_sequence):
        """Обработка последовательности элементов и получение информации со
        страницы. В случае если для элемента определено несколько
        последовательностей, будет выбран первый ненулевой результат.
        Не требует переопределения
        :param parsing_sequence: Последовательность элементов на странице для
            получения определённой информации
        :type parsing_sequence: List[List[ParsingElement]]
        :raise: ElementNotFoundedOnPage
        """
        self.reset_where_to_find()
        for sequence_num, sequence in enumerate(parsing_sequence):
            try:
                element = None
                for parsing_element in sequence:
                    element = self.get_element_on_page(parsing_element)
                return element
            except ElementNotFoundedOnPage as e:
                if sequence_num == len(parsing_sequence) - 1:
                    print(e.message)
                    raise e
                else:
                    continue

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

    def get_identifier_function(self, parsing_element):
        """Возвращает функцию для парсинга конкретного элемента
        :param parsing_element: Тип идентификатора и сам идентификатор
        :return: Фунция для парсинга элемента
        :raise: ElementNotFoundedOnPage
        """
        identifier_functions = self.get_supported_identifier_functions()
        function_tuple = identifier_functions.get(parsing_element.type)
        if not function_tuple:
            print('Подходящая функция не была найдена.')
            raise ElementNotFoundedOnPage(parsing_element)
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
    def get_param_for_identifier_function(self, function, parsing_element):
        """Возвращает словарь параметров для передачи в функцию
        получения идентификатора
        :param function: Функция для получения идентификатора
        :param parsing_element: Тип идентификатора и сам идентификатор
        :type parsing_element: ParsingElement
        :return args, kwargs: Неименованные/именованные аргументы для функции
        :raise BaseParsingException
        """
        pass

    def get_element_on_page(self, parsing_element):
        """ Получение элемента на странице согласно идентификатору
        :param parsing_element: Тип идентификатора и сам идентификатор
        :type parsing_element: ParsingElement

        :return: Искомый элемент страницы
        :rtype: Any

        :raise: WrongIdentifier, ElementNotFoundedOnPage
        """
        print(f'Type={IdentifierEnum.values[parsing_element.type]},'
              f'id={parsing_element.identifier}')
        function = self.get_identifier_function(parsing_element)
        args, kwargs = self.get_param_for_identifier_function(
            function, parsing_element)
        result = function(*args, **kwargs)
        print(f'Результат парсинга={result}')
        if not result:
            raise ElementNotFoundedOnPage(parsing_element)

        self.where = result
        return result
