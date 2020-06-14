from django.core.exceptions import ImproperlyConfigured

from common.classes import BaseEnumerate


class IdentifierEnum(BaseEnumerate):
    """Типы идентификаторов элементов на html странице"""
    id = 0
    class_ = 1
    xpath = 2
    tag = 3
    attr = 4
    text = 5
    num = 6

    values = {
        id: 'id',
        class_: 'class',
        xpath: 'xpath',
        tag: 'tag',
        attr: 'attr',
        text: 'text',
        num: 'num',
    }

    # Словарь для перевода идентификаторов из текста
    str_to_identifier = {
        'ID': id,
        'CLASS': class_,
        'XPATH': xpath,
        'TAG': tag,
        'ATTRIBUTE': attr,
        'TEXT': text,
        'NUM': num,
    }


class PageParserEnum(BaseEnumerate):
    """Типы парсеров html страниц"""

    Selenium = 0
    Requests = 1

    values = {
        Selenium: 'Selenium',
        Requests: 'Requests',
    }

    @classmethod
    def get_parser_type(cls, string):
        """Возвращает id парсера по строке
        :param string: Строка с названием парсера
        :return: id парсера
        :raise: ImproperlyConfigured
        """
        for parser_id, name in PageParserEnum.values.items():
            if name.upper() == string.upper():
                return parser_id
        raise ImproperlyConfigured(f'Указан некорректный тип парсера {string}')
