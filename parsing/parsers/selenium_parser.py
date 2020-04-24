import os

from django.core.exceptions import ImproperlyConfigured
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver import ChromeOptions
from selenium.webdriver.remote.webelement import WebElement

from config.settings import ADDITIONAL_FILES_DIR

from parsing.parsers.base_parser import PageParser
from parsing.parsers.helpers import open_parser
from parsing.parsers.settings import SELENIUM_VISIBLE, SELENIUM_LOGS_FILE
from .constants import IdentifierEnum
from .exceptions import *


class SeleniumProgramEnum:
    Chrome = 0
    Firefox = 1


class SeleniumSettings:
    """Настройки Selenium в зависимости от типа выбранного вебдрайвера"""

    # Обязательные поля в настройках
    required_fields = [
        'webdriver_class',
        'option_class',
        'path',
    ]

    # Поля, которые не включаются в словарь, передаемый в класс веб-драйвера
    not_include_to_dict = [
        'webdriver_class',
        'option_class',
        'path',
    ]

    settings = {
        SeleniumProgramEnum.Chrome: dict(
            webdriver_class=webdriver.Chrome,
            option_class=ChromeOptions,
            path='chromedriver.exe'
        ),
        SeleniumProgramEnum.Firefox: dict(
            webdriver_class=webdriver.Firefox,
            option_class=FirefoxOptions,
            path='geckodriver.exe'
        )
    }

    def __init__(self, parser):
        self.type = parser.webdriver_type
        self.visible = parser.visible
        self.current_settings = self.settings[self.type].copy()

    @property
    def has_all_required_fields(self):
        """Проверяет наличие всех обязательных полей для данных настроек"""
        required_fields_set = set(self.required_fields)
        settings_keys_set = set(self.current_settings.keys())
        return required_fields_set.issubset(settings_keys_set)

    def check_all_required_fields(self):
        """Возращает ошибку, если настройки содержат не все обязательные поля
        :raise: ImproperlyConfigured
        """
        if not self.has_all_required_fields:
            raise ImproperlyConfigured(
                'В настройке Selenium содержатся не все обязательные поля')

    @property
    def webdriver_class(self):
        """Возвращает класс веб-драйвера для парсера"""
        return self.current_settings.get('webdriver_class')

    @property
    def executable_path(self):
        """Путь до исполняемого файла парсера"""
        return dict(executable_path=r'{}'.format(
                os.path.join(ADDITIONAL_FILES_DIR,
                             self.current_settings['path'])))

    @property
    def service_log_path(self):
        """Путь до файла логов парсера"""
        return dict(service_log_path=SELENIUM_LOGS_FILE)

    @property
    def visibility_settings(self):
        """Настройки видимости парсера"""
        if not self.visible:
            driver_options = self.current_settings['option_class']()
            driver_options.add_argument("--headless")
            driver_options.add_argument("--window-size=1366x768")
            return dict(options=driver_options)
        return {}

    def exclude_fields_from_dict(self, dictionary):
        """Убирает из словаря ненужные поля, описанные в not_include_to_dict
        :type dictionary: dict
        """
        result_dict = dictionary.copy()
        for key in self.not_include_to_dict:
            if key in result_dict:
                result_dict.pop(key)
        return result_dict

    def get_dict(self):
        """Возвращает словарь с настройками Selenium для передачи
        в конструктор вебдрайвера
        """
        settings_dict = self.settings[self.type].copy()
        self.check_all_required_fields()
        settings_dict = self.exclude_fields_from_dict(settings_dict)
        settings_dict.update(self.executable_path)
        settings_dict.update(self.service_log_path)
        settings_dict.update(self.visibility_settings)
        return settings_dict


class SeleniumPageParser(PageParser):
    """Парсер Selenium"""

    url = None
    visible = SELENIUM_VISIBLE
    webdriver_type = SeleniumProgramEnum.Chrome
    setting_class = SeleniumSettings

    def get_webdriver(self):
        """Возвращает веб-драйвер для парсера"""
        settings_dict = self.setting.get_dict()
        webdriver_class = self.setting.webdriver_class
        driver = webdriver_class(**settings_dict)
        return driver

    def __init__(self, url):
        self.url = url
        self.setting = SeleniumSettings(self)
        self.driver = self.get_webdriver()
        self.reset_where_to_find()

    @open_parser
    def open(self):
        super(SeleniumPageParser, self).open()
        self.driver.get(self.url)

    def close(self):
        super(SeleniumPageParser, self).close()
        self.driver.close()

    def reset_where_to_find(self):
        self.where = self.driver

    @staticmethod
    def get_num_of_list(elem_list, num):
        """Возвращается num-ый по счёту элемент массива"""
        assert isinstance(elem_list, list)

        if 0 <= num <= len(elem_list):
            try:
                return elem_list[num]
            except IndexError as e:
                print('Индекс вышел за границы массива!')

        return None

    def get_supported_identifiers(self):
        """Возвращает словарь поддерживаемых идентификторов и соответствующих
        им функций для текущего расположения веб-драйвера
        """
        identifier_functions = {}
        is_web_element = isinstance(self.where, WebElement)

        if (isinstance(self.where, self.setting.webdriver_class) or
                is_web_element):
            identifier_functions.update({
                IdentifierEnum.id: self.where.find_element_by_id,
                IdentifierEnum.class_: self.where.find_elements_by_class_name,
                IdentifierEnum.xpath: self.where.find_element_by_xpath,
                IdentifierEnum.tag: self.where.find_element_by_tag_name
            })
        if is_web_element:
            identifier_functions[IdentifierEnum.attr] = self.where.get_attribute
            identifier_functions[IdentifierEnum.text] = getattr
        if isinstance(self.where, list):
            identifier_functions[IdentifierEnum.num] = self.get_num_of_list
        return identifier_functions

    def get_param_for_identifier_function(self, function, elem_src):
        """Возвращает словарь параметров для передачи в функцию
        получения идентификатора
        :param elem_src: Тип идентификатора и сам идентификатор
        :type elem_src: TypeAndId
        :param elem_src: Функция для получения идентификатора
        :return args, kwargs: Неименованные/именованные аргументы для функции
        :raise BaseParsingException
        """
        args = []
        kwargs = {}
        if isinstance(self.where, list):
            try:
                kwargs['elem_list'] = self.where
                kwargs['num'] = int(elem_src.id)
            except ValueError:
                raise BaseParsingException('Некорректный параметр!')
        elif function == getattr and elem_src.type == IdentifierEnum.text:
            args = [self.where, 'text', None]
        else:
            # По умолчанию
            args = [elem_src.id]
        return args, kwargs

    def get_element_on_page(self, elem_src):
        """ Получение элемента на странице согласно идентификатору
        :param elem_src: Тип идентификатора и сам идентификатор
        :type elem_src: TypeAndId
        :raise: WrongIdentifier, ElementNotFoundedOnPage
        """

        identifier_functions = self.get_supported_identifiers()
        function = identifier_functions.get(elem_src.type)
        if not function:
            raise ElementNotFoundedOnPage(elem_src)

        args, kwargs = self.get_param_for_identifier_function(
            function, elem_src)
        print(f'Function={function}, id={elem_src.id}', end='')
        result = function(*args, **kwargs)
        print(f', result={result}')
        if not result:
            raise ElementNotFoundedOnPage()

        self.where = result
        return result
