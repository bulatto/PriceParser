from bs4 import BeautifulSoup
from bs4 import element
import requests

from parsing.enum import IdentifierEnum
from parsing.parsers import BaseParsingException
from parsing.parsers import ElementNotFoundedOnPage
from parsing.parsers.base_parser import PageParser
from parsing.parsers.helpers import get_num_of_list
from parsing.parsers.helpers import open_parser


# Типы идентификаторов элементов на html странице. Необходимо для изменения
# нескольких элементов в словаре values
RequestsIdentifierEnum = IdentifierEnum()
RequestsIdentifierEnum.values.update({
    IdentifierEnum.class_: 'class_',
    IdentifierEnum.tag: 'name',
})


class RequestsPageParser(PageParser):
    """Парсер на основе requests"""

    def __init__(self, url):
        self.url = url

    def return_soup_from_url(self,):
        response = requests.get(self.url)
        return BeautifulSoup(response.text, "html.parser")

    @open_parser
    def open(self):
        self.bs = self.return_soup_from_url()

    def reset_where_to_find(self):
        self.where = self.bs

    @staticmethod
    def get_element_attribute(where, attribute):
        """Функция для обработки получения атрибута
        :param where: Место, в котором будет происходить поиск
        :param attribute: Название атрибута
        :return: Возвращает атрибут, если он есть, иначе None
        """
        attrs = getattr(where, 'attrs', None)
        if attrs:
            return attrs.get(attribute, None)

    def get_identifier_functions(self):
        return {
            RequestsIdentifierEnum.id: ('where', 'find'),
            RequestsIdentifierEnum.class_: ('where', 'find_all'),
            RequestsIdentifierEnum.xpath: ('where', 'find'),
            RequestsIdentifierEnum.tag: ('where', 'find'),
            RequestsIdentifierEnum.attr: (None, self.get_element_attribute),
            RequestsIdentifierEnum.text: (None, getattr),
            RequestsIdentifierEnum.num: (None, get_num_of_list),
        }

    def get_supported_identifiers_list(self):
        """Получение списка идентификаторов, поддерживаемых для текущего
        элемента self.where
        """
        supported_identifiers = []
        IdEnum = RequestsIdentifierEnum
        is_tag_element = isinstance(self.where, element.Tag)

        if is_tag_element:
            supported_identifiers.extend(
                [IdEnum.id, IdEnum.class_, IdEnum.xpath, IdEnum.tag,
                 IdEnum.attr, IdEnum.text])

        if isinstance(self.where, list):
            supported_identifiers.append(IdEnum.num)

        return supported_identifiers

    def get_param_for_identifier_function(self, function, elem_src):
        args, kwargs = [], {}

        if isinstance(self.where, list):
            try:
                kwargs.update(
                    {'elem_list': self.where, 'num': int(elem_src.id)})
            except ValueError:
                raise BaseParsingException('Некорректный параметр!')
        elif (function == getattr and
                elem_src.type == RequestsIdentifierEnum.text):
            args = [self.where, 'text', None]
        elif elem_src.type == RequestsIdentifierEnum.attr:
            args = [self.where, elem_src.id]
        else:
            # По умолчанию
            identifier = RequestsIdentifierEnum.values[elem_src.type]
            kwargs.update({identifier: elem_src.id})
        return args, kwargs
