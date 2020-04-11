import os
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver import ChromeOptions
from selenium.webdriver.remote.webelement import WebElement

from config.settings import ADDITIONAL_FILES_DIR

from parsing.parsers.base_parser import PageParser
from parsing.parsers.helpers import open_parser
from parsing.parsers.settings import SELENIUM_VISIBLE, SELENIUM_LOGS_FILE
from .constants import IdentifierEnum, SeleniumSettings
from .exceptions import *


class SeleniumPageParser(PageParser):
    class SeleniumProgram:
        Chrome = 0
        Firefox = 1

        settings = {
            Chrome: SeleniumSettings(
                webdriver_class=webdriver.Chrome,
                option_class=ChromeOptions,
                path=r'{}'.format(
                    os.path.join(ADDITIONAL_FILES_DIR, 'chromedriver.exe'))
            ),
            Firefox: SeleniumSettings(
                webdriver_class=webdriver.Firefox,
                option_class=FirefoxOptions,
                path=r'{}'.format(
                    os.path.join(ADDITIONAL_FILES_DIR, 'geckodriver.exe'))
            )
        }

    url = None
    visible = SELENIUM_VISIBLE
    program = SeleniumProgram.Firefox

    @classmethod
    def get_webdriver(cls):
        setting = cls.SeleniumProgram.settings[cls.program]
        if not cls.visible:
            driver_options = setting.option_class()
            driver_options.add_argument("--headless")
            driver_options.add_argument("--window-size=1366x768")
            driver = setting.webdriver_class(
                executable_path=setting.path, options=driver_options,
                service_log_path=SELENIUM_LOGS_FILE
            )
        else:
            driver = setting.webdriver_class(
                executable_path=setting.path,
                service_log_path=SELENIUM_LOGS_FILE
            )
        return driver

    def __init__(self, url):
        self.url = url
        self.driver = self.get_webdriver()
        self.setting = self.SeleniumProgram.settings[self.program]
        self.reset_where_to_find()

    @open_parser
    def open(self):
        print(f'Открытие сайта {self.url}')
        self.driver.get(self.url)

    def close(self):
        print('Закрытие сайта')
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
