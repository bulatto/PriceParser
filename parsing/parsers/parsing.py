from urllib.parse import urlparse

from parsing.parsers.photo_downloader import PhotoDownloader
from parsing.parsers.requests_parser import RequestsPageParser
from parsing.parsers.selenium_parser import SeleniumPageParser
from parsing.site_config import all_sites_config
from .constants import PageParserEnum
from .exceptions import *


class Parsing:
    """Основной класс, соединяющий парсеры с сайтами"""

    def __init__(self, url):
        self.url = url
        self.site_config = self.get_site_config()
        self.parser = self.get_parser(
            self.site_config.parser_type, url)

    @staticmethod
    def get_parser(parser_type, url):
        """Получение экземпляра парсера"""
        assert parser_type is not None, f'Некорретный тип парсера - {parser_type}'
        assert url, f'Задана некорретная ссылка на сайт - {url}'

        parser_class = {
            PageParserEnum.Selenium: SeleniumPageParser,
            PageParserEnum.Requests: RequestsPageParser
        }.get(parser_type)

        if not parser_class:
            raise IncorrectParserType()

        return parser_class(url)

    def get_site_config(self):
        base_url = urlparse(self.url).netloc
        for site in all_sites_config:
            if base_url == urlparse(site.base_url).netloc:
                return site
        raise UnsupportedSiteUrl(base_url)

    def parse_data(self):
        # TODO: проверить соединение с сайтом,
        # только после этого приступать к парсингу
        # (также удостовериться, что ссылка правильная)
        try:
            self.parser.open()
            site = self.site_config
            price = self.process_price(site.price_src)
            photo_name = self.process_photo(site.photo_src)
            self.parser.close()
            return price, photo_name
        except BaseParsingException as error:
            if self.parser:
                self.parser.close()
            raise error

    def process_element(self, source):
        self.parser.reset_where_to_find()
        for elem_source in source:
            element = self.parser.get_page_elem(elem_source)
            if not element:
                raise ElementNotFoundedOnPage('Элемент не найден на странице!')
        return element

    def process_price(self, source):
        element = self.process_element(source)
        return ''.join([c for c in element if c.isdigit()])

    def process_photo(self, source):
        element = self.process_element(source)
        success, photo_path, _ = PhotoDownloader(element).download()
        return photo_path