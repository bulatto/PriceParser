from configparser import ConfigParser
import re

from django.core.exceptions import ImproperlyConfigured

from common.helpers import check_parentheses_in_string
from parsing.enum import PageParserEnum
from parsing.parsers.helpers import get_identifier
from parsing.structures import ParsingElement


class SiteConfig:
    """Класс для хранения конфигураций сайтов"""
    def __init__(self, name, base_url, parser_type, price_src, photo_src):
        self.name = name
        self.base_url = base_url
        self.parser_type = parser_type
        self.price_src = price_src
        self.photo_src = photo_src


class SiteConfigParser(ConfigParser):
    """Обертка над ConfigParser для работы с параметрами сайтов"""

    # Прочитан ли файл
    is_file_readed = False
    # Обязательные поля для каждого сайта
    required_fields = (
        'BASE_URL',
        'PARSER_TYPE',
        'PRICE_PATH',
        'PHOTO_PATH'
    )

    def check_required_fields(self):
        """Проверка наличия всех необходимых полей
        :raise: ImproperlyConfigured
        """
        error_message = ('Обязательный параметр {0} отсутствует '
                         'в секции {1} конфигурации')
        for section in self.sections():
            for field in self.required_fields:
                if field not in self[section].keys():
                    raise ImproperlyConfigured(
                        error_message.format(field, section))

    def check_config_parentheses(self):
        """Проверка, что все скобки в файле конфигурации имеют пару (закрыты),
        и следуют в правильном порядке (открытая, затем закрытая скобка)

        :raise: ImproperlyConfigured
        """
        for section in self.sections():
            for field, value in self[section].items():
                result = check_parentheses_in_string(value)
                if not result:
                    raise ImproperlyConfigured(
                        f'В конфигурации сайтов в разделе [{section}] {field} '
                        f'неверно расставлены скобки')

    @staticmethod
    def split_by_brackets(string, list_brackets='[]'):
        """Разделить строку по скобкам, проверяя закрытость скобок, для того,
        чтобы не произошла ошибка, если параметр содержит такие же скобки

        :param string: Строка для разделения
        :param list_brackets: Вид скобок '()' или '[]'
        :return: Список строк
        """
        assert list_brackets in ['()', '[]'], 'Неправильно заданы скобки'

        if string[0] != '[' and string[-1] != ']':
            return

        open_char, close_char = list_brackets
        splitted_list = []

        stack = []
        for num, ch in enumerate(string):
            if ch not in list_brackets:
                continue
            elif ch in '([':
                stack.append((num, ch))
            elif not stack:
                raise ImproperlyConfigured()
            else:
                popped_num, popped_char = stack.pop()
                if popped_char != open_char:
                    raise ImproperlyConfigured()
                if not stack:
                    splitted_list.append(string[popped_num: num + 1])
        return splitted_list

    @classmethod
    def process_path_to_element(cls, element_path):
        """Обрабатывает пути к элементам сайта, которые необходимо получить
        :raise: ImproperlyConfigured
        """
        result_sequence = []
        regexp = r'(?:([A-Z]+) *)(?:\((.+?)\))?(?: *;? *)'

        if element_path[0] == '[' and element_path[-1] == ']':
            sequences_list = cls.split_by_brackets(element_path, '[]')
        else:
            sequences_list = [element_path]

        for sequence in sequences_list:
            regexp_result = re.findall(regexp, sequence)
            if not regexp_result:
                raise ImproperlyConfigured(
                    f'Неверно задана строка в конфигурации - "{element_path}"')
            seq = []
            for string_type, param in regexp_result:
                # Получение типа идентификатора
                string_key, identifier_type = get_identifier(string_type)
                seq.append(ParsingElement(identifier_type, param))

            result_sequence.append(seq)

        return result_sequence

    def read(self, filenames, encoding=None):
        """Функция для чтения файла настроек, также здесь осуществляются
        некоторые проверки коррректности заполнения файла"""

        super(SiteConfigParser, self).read(filenames, encoding)
        # Проверка наличия всех обязательных полей
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
                parser_type=PageParserEnum.get_parser_type(site['PARSER_TYPE']),
                price_src=self.process_path_to_element(site['PRICE_PATH']),
                photo_src=self.process_path_to_element(site['PHOTO_PATH'])
            )
            all_sites.append(config)

        return all_sites
