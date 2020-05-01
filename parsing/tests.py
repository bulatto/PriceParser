from django.test import TestCase
from django.contrib.auth.models import User
from urllib.parse import urlparse

from config.settings import DEFAULT_IMG_NAME
from parsing.parsers.exceptions import ElementNotFoundedOnPage
from parsing.site_config.config_parser import SiteConfigParser
from .models import Product
from .parsers import Parsing, PhotoDownloader


class TestParsing(TestCase):
    fixtures = ['sites.json']

    def get_one_site_from_each(self):
        """Для каждого уникального сайта в базе данных находит пи одному url"""
        sites_list = Product.objects.values_list('id', 'url')
        # Словарь, в которому будут содержаться уникальные сайты
        self.unique_sites = dict.fromkeys(
            set(urlparse(url).netloc for id, url in sites_list))
        # Найдем по одному представителя каждого сайта
        for id, url in sites_list:
            url_netloc = urlparse(url).netloc
            if self.unique_sites[url_netloc] is None:
                self.unique_sites[url_netloc] = url

    def print_unique_sites(self):
        """Вывод уникальных сайтов"""
        print('Unique sites:')
        for netloc, url in self.unique_sites.items():
            print(f'{netloc} - {url}')

    def setUp(self) -> None:
        self.get_one_site_from_each()
        self.print_unique_sites()

    def test_unique_sites(self):
        """Тесты для уникальных сайтов"""
        for url in self.unique_sites.values():
            print('--------------------------------')
            try:
                price, photo = Parsing(url).parse_data()
                print(f'Price - {price}; Photo - {photo}')
            except ElementNotFoundedOnPage:
                print(f'Не удалось найти элемент на странице {url}! '
                      'Проверьте конфигурацию сайта.')
                self.fail()
            print('--------------------------------')

            self.assertIsNotNone(price)
            self.assertIsNotNone(photo)


class TestPhotoDownloader(TestCase):
    image_urls = dict(
        correct='https://img2.wbstatic.net/big/new/8660000/8661404-1.jpg',
        wrong='https://img2.wbstatic.net/big/new/8660000/agigdigdaggdg-1.jpg',
        unsupported_format=''
    )

    def test_correct_url(self):
        success, photo, _ = PhotoDownloader(self.image_urls['correct']).download()
        self.assertTrue(success)
        self.assertIsNotNone(photo)

    def test_wrong_url(self):
        success, photo, _ = PhotoDownloader(self.image_urls['wrong']).download()
        self.assertFalse(success)
        self.assertIsNone(photo)

    def test_empty_url(self):
        success, photo, _ = PhotoDownloader('').download()
        self.assertFalse(success)
        self.assertIsNone(photo)


class TestCheckParentheses(TestCase):
    strings = dict(
        correct_strings=[
            '()[]([])',
            '[[[[]]]]',
            '[124[43[43(gsdg)]]gd]'
        ],
        wrong_strings=[
            '()[](])',
            '[[[[]])]',
            '[124[43[43(gsdg)]]gd)'
        ]
    )

    def test_check_correct_parentheses(self):
        for string in self.strings['correct_strings']:
            self.assertTrue(
                SiteConfigParser.check_parentheses_in_string(string))

    def test_check_wrong_parentheses(self):
        for string in self.strings['wrong_strings']:
            self.assertFalse(
                SiteConfigParser.check_parentheses_in_string(string))