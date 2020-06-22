from urllib.parse import urlparse

from parsing.enum import PageParserEnum
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

    def __init__(self, url):
        assert url, 'Url не должен быть пустым!'

        self.url = url
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
        """Метод запуска и контроля парсинга. Возвращает данные в результате
        выполнения parse_data"""

        # TODO: проверить соединение с сайтом,
        # только после этого приступать к парсингу
        # (также удостовериться, что ссылка правильная)
        try:
            self.parser.open()
            parsing_result = self.parse_data()
            self.parser.close()
            return parsing_result
        except BaseParsingException as error:
            if self.parser:
                self.parser.close()
            raise error

    def parse_data(self):
        """Метод парсинга данных"""
        price = self.get_data_from_parser(
            self.site_config.price_src, self.price_processing)
        photo_name = self.get_data_from_parser(
            self.site_config.photo_src, self.photo_processing)
        return price, photo_name

    def get_data_from_parser(self, sequence, processing_func=None):
        """Получение информации из последовательности с последующей обработкой
        функцией processing_func
        """
        result = self.parser.parse_sequence(sequence)
        final_result = processing_func(result) if processing_func else result
        return final_result

    @staticmethod
    def price_processing(string):
        return ''.join([c for c in string if c.isdigit()])

    @staticmethod
    def photo_processing(string):
        success, photo_path, _ = PhotoDownloader(string).download()
        return photo_path
