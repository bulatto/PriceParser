from collections import namedtuple


class BaseEnumerate:
    values = {}

    @classmethod
    def get_choices(cls):
        return [(value, key) for key, value in cls.values.items()]


class IdentifierEnum(BaseEnumerate):
    id = 0
    class_ = 1
    xpath = 2
    tag = 3
    attr = 4
    text = 5
    num = 6

    values = {
        'id': id,
        'class_': class_,
        'xpath': xpath,
        'tag': tag,
        'attr': attr,
        'text': text,
        'num': num,
    }


class PageParserEnum(BaseEnumerate):
    Selenium = 0
    Requests = 1

    values = {
        'Selenium': Selenium,
        'Requests': Requests,
    }


TypeAndId = namedtuple('TypeAndId', ['type', 'id'])
SeleniumSettings = namedtuple(
    'SeleniumSettings', ['webdriver_class', 'option_class', 'path'])
