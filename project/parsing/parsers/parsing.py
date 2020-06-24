import re
from urllib.parse import urlparse

from parsing.enum import PageParserEnum
from parsing.parsers.helpers import price_processing
from parsing.parsers.photo_downloader import PhotoDownloader
from parsing.parsers.requests_parser import RequestsPageParser
from parsing.parsers.selenium_parser import SeleniumPageParser
from parsing.site_config import all_sites_config

from .exceptions import *


parser_classes = {
    PageParserEnum.Selenium: SeleniumPageParser,
    PageParserEnum.Requests: RequestsPageParser
}


class Parsing:
    """Основной класс, соединяющий парсеры с сайтами"""

    def __init__(self, url, photo_is_needed=True):
        """
        :param url: Ссылка на сайт
        :param photo_is_needed: Нужно ли сохранять фото
        """
        assert url, 'Url не должен быть пустым!'

        self.url = url
        self.photo_is_needed = photo_is_needed
        self.site_config = self.get_site_config()
        self.parser = self.get_parser_class(self.site_config.parser_type)(url)

    @staticmethod
    def get_parser_class(parser_type):
        """Получение экземпляра парсера"""
        assert parser_type is not None, f'Некорретный тип парсера {parser_type}'

        parser_class = parser_classes.get(parser_type)
        if parser_class:
            return parser_class
        else:
            raise IncorrectParserType()

    def get_site_config(self):
        """Получение конфигурации сайта"""
        base_url = urlparse(self.url).netloc
        for site in all_sites_config:
            if base_url == urlparse(site.base_url).netloc:
                return site

        raise UnsupportedSiteUrl(base_url)

    def parse(self):
        """Вызвает функцию парсинга у парсера и передаёт ему необходимые
        данные для обработки
        """
        # Список кортежей, где первый элемент - последовательность парсинга,
        # второй - функция, применяемая после получения результата со страницы
        data_for_parsing = [
            (self.site_config.price_src, price_processing),
            (self.site_config.photo_src, self.photo_processing),
        ]
        return self.parser.parse(data_for_parsing)

    def photo_processing(self, string):
        photo_path = ''
        if self.photo_is_needed:
            success, photo_path, _ = PhotoDownloader(string).download()
        return photo_path
