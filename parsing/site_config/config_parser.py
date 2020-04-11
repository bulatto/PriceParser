from configparser import ConfigParser

from django.core.exceptions import ImproperlyConfigured

from parsing.parsers.constants import IdentifierEnum, TypeAndId, PageParserEnum


class SiteConfig:
    def __init__(self, name, base_url, parser_type, price_src, photo_src):
        self.name = name
        self.base_url = base_url
        self.parser_type = parser_type
        self.price_src = price_src
        self.photo_src = photo_src


class ConfigParseHelper:
    """Класс-помощник для парсера файла конфигурации.
    Содержит полезные словари, параметры и функции для парсинга
    """

    # Обязательные поля для каждого сайта
    required_fields = (
        'BASE_URL',
        'PARSER_TYPE',
        'PRICE_PATH',
        'PHOTO_PATH'
    )

    # Словарь для перевода идентификаторов из текста
    str_to_identifier = {
        'ID': IdentifierEnum.id,
        'CLASS': IdentifierEnum.class_,
        'XPATH': IdentifierEnum.xpath,
        'TAG': IdentifierEnum.tag,
        'ATTRIBUTE': IdentifierEnum.attr,
        'TEXT': IdentifierEnum.text,
        'NUM': IdentifierEnum.num,
    }

    # Идентификаторы, для которых не нужны параметры (в строковом виде)
    no_need_for_param = ['TEXT']

    @classmethod
    def get_parser_type(cls, string):
        """Возвращает id парсера
        :param string: Строка с названием парсера
        :return: id парсера
        :raise: ImproperlyConfigured
        """
        for name, parser_id in PageParserEnum.values.items():
            if name.upper() == string.upper():
                return parser_id
        raise ImproperlyConfigured(f'Указан некорректный тип парсера {string}')

    @classmethod
    def get_identifier(cls, string):
        """Находит идентификатор в начале строки или генерирует ошибку
        :param string: Строка с идентификатором и параметром функции
        :type string: str
        :raise: ImproperlyConfigured
        """
        assert string, "Строка пуста!"

        for key, value in cls.str_to_identifier.items():
            if string.startswith(key):
                return key, value
        raise ImproperlyConfigured(
            f'Идентификатор не был найден в начале строки "{string}"')


class SiteConfigParser(ConfigParser):
    """Обертка над ConfigParser для работы с параметрами сайтов"""

    # Параметр, прочитан ли файл
    is_file_readed = False

    def check_required_fields(self):
        """Проверка наличия всех необходимых полей
        :raise: ImproperlyConfigured"""

        error_message = ('Обязательный параметр {0} отсутствует '
                         'в секции {1} конфигурации')
        for section in self.sections():
            for field in ConfigParseHelper.required_fields:
                if field not in self[section].keys():
                    raise ImproperlyConfigured(
                        error_message.format(field, section))

    @staticmethod
    def check_parentheses_in_string(string):
        """Проверяет закрытость скобок в строке.
        Возвращает True, если все хорошо, иначе False
        :param string: Строка, которую необходимо проверить
        :return: Корректность расстановки скобок (True/False)
        """
        # Символы, которые учитываются при подсчёте
        open_chars, close_chars = '([', ')]'

        parentheses = []
        for ch in (c for c in string if c in open_chars + close_chars):
            if ch in open_chars:
                parentheses.append(ch)
            else:
                if not parentheses or (
                        parentheses.pop() != open_chars[close_chars.index(ch)]):
                    return False
        return len(parentheses) == 0

    def check_config_parentheses(self):
        """Проверка, что все скобки в файле конфигурации имеют пару (закрыты)
        :raise: ImproperlyConfigured
        """
        for section in self.sections():
            for field, value in self[section].items():
                result = self.check_parentheses_in_string(value)
                if not result:
                    raise ImproperlyConfigured(
                        f'В cекции {section} в параметре {field} '
                        f'неверно расставлены скобки')

    @classmethod
    def get_param_in_parentheses(cls, element, parentheses, key=''):
        """Возвращает параметры в скобках (фигурных и круглых).
        Все скобки считаются закрытыми, поскольку ранее провелась проверка
        :param element: Строка со скобками
        :param key: Обрабатываемый параметр
        :param parentheses: Скобки '()' или '[]'
        :raise: ImproperlyConfigured
        """
        assert parentheses in ['()', '[]'], 'Неправильно заданы скобки'
        assert element, 'Пустая строка'

        # Проверка, что указаны скобки
        if (element.startswith(parentheses[0]) and
                element.endswith(parentheses[1])):
            param = element[1:-1]
        else:
            return element

        # Если внутри скобок пусто
        if not param:
            raise ImproperlyConfigured(
                f'Некорректно указаны параметры для идентификатора {key}')

        if parentheses == '()':
            return param
        elif parentheses == '[]':
            return cls.process_path_to_element(param)
        raise ImproperlyConfigured('Произошла ошибка при обработке параметров!')

    @classmethod
    def process_one_identifier(cls, element):
        """Обрабатывает один идентификатор (часть пути к элементу сайта)
        :raise: ImproperlyConfigured
        """

        if not element:
            raise ImproperlyConfigured(
                f'Некорректная конфигурация сайта!')

        # Получение идентификатора, с которого начинается строка
        key, identifier = ConfigParseHelper.get_identifier(element)
        # Обрезание строки (удаление идентификатора)
        element = element[len(key):]

        # Проверка необходимости параметров
        if key in ConfigParseHelper.no_need_for_param:
            if len(element) > 0:
                raise ImproperlyConfigured(
                    f'Посторонние символы после идентификатора {key}')
            return identifier, None

        param = cls.get_param_in_parentheses(element, '()', key)
        return identifier, param

    @classmethod
    def process_path_to_element(cls, element_path):
        """Обрабатывает пути к элементам сайта, которые необходимо получить
        :raise: ImproperlyConfigured
        """
        source = []
        # Удаляем пробелы
        element_path = element_path.replace(' ', '')

        # Ищем квадратные скобки
        if element_path.find('[') != -1 and element_path.find('];') != -1:
            index = element_path.find('];')
            if len(element_path) <= index + 2:
                raise ImproperlyConfigured(
                    f'Некорректно указаны параметры для идентификатора')
            param = cls.get_param_in_parentheses(element_path[:index + 1], '[]')
            source.append(param)
            element_path = element_path[index + 2:]

        # Разделяем строку по символу ';'
        elements = element_path.split(';')

        for element in elements:
            identifier, param = cls.process_one_identifier(element)
            source.append(TypeAndId(type=identifier, id=param))

        return source

    def read(self, filenames, encoding=None):
        super(SiteConfigParser, self).read(filenames, encoding)
        # Проверка наличия всех обязятальных полей
        self.check_required_fields()
        # Проверка корректности расстановки скобок
        self.check_config_parentheses()

    def parse_sites_config(self):
        """Предназначен для обработки параметров сайтов из файла конфигурации"""
        all_sites = []

        if not self.sections():
            print('Внимание! Файл конфигурации не содержит информацию о сайтах')

        for section in self.sections():
            site = self[section]
            config = SiteConfig(
                name=section,
                base_url=site['BASE_URL'],
                parser_type=ConfigParseHelper.get_parser_type(
                    site['PARSER_TYPE']),
                price_src=self.process_path_to_element(site['PRICE_PATH']),
                photo_src=self.process_path_to_element(site['PHOTO_PATH'])
            )
            all_sites.append(config)

        return all_sites
