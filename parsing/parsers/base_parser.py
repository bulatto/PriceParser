from abc import ABCMeta, abstractmethod
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

        if not isinstance(elem_src, list):
            return self.get_element_on_page(elem_src)
        else:
            for el_src in elem_src:
                elem = self.try_get_element_on_page(el_src)
                if elem:
                    return elem
            raise ElementNotFoundedOnPage()

    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def get_element_on_page(self, elem_src):
        pass

    def reset_where_to_find(self):
        pass

    def close(self):
        pass