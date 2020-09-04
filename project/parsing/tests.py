from urllib.parse import urlparse

from django.test import TestCase

from common.helpers import check_parentheses_in_string
from parsing.enum import IdentifierEnum
from parsing.parsers.exceptions import ElementNotFoundedOnPage
from parsing.site_config.config_parser import SiteConfigParser

from .models import Product
from .parsers import Parsing
from .parsers import PhotoDownloader


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
            print(url)
            try:
                price, photo = Parsing(url).parse()
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
                check_parentheses_in_string(string))

    def test_check_wrong_parentheses(self):
        for string in self.strings['wrong_strings']:
            self.assertFalse(
                check_parentheses_in_string(string))


class TestSiteConfigParser(TestCase):

    enum = IdentifierEnum

    # Словарь с тестовыми данными
    # Ключи - входные строки, значения -  словари с корректными результатами,
    # которые должны получиться при вызове определённых методов
    test_data_dict = {
        r'CLASS(ii-product__price-current_red); NUM(0); TEXT': {
            'split_by_brackets': None,
            'process_path_to_element': [[
                (enum.class_, 'ii-product__price-current_red'),
                (enum.num, '0'),
                (enum.text, '')
            ]]
        },
        r'XPATH(//*[@id="container"]/div[1]/div[3]/div[2]/div[2]/div/div/div[1]'
        r'/span); TEXT': {
            'split_by_brackets': None,
            'process_path_to_element': [[
                (enum.xpath, r'//*[@id="container"]/div[1]/div[3]/div[2]'
                             r'/div[2]/div/div/div[1]/span'),
                (enum.text, '')
            ]]
        },
        r'[XPATH(//*[@id="container"]/div[1]/div[3]/div[2]/div[2]/div/div/'
        r'div[1]/span); TEXT][CLASS(final-cost); NUM(0); TEXT][ID(photo);'
        r'TAG(a); ATTRIBUTE(href)]': {
            'split_by_brackets': [
                r'[XPATH(//*[@id="container"]/div[1]/div[3]/div[2]/div[2]/div/'
                r'div/div[1]/span); TEXT]',
                r'[CLASS(final-cost); NUM(0); TEXT]',
                r'[ID(photo);TAG(a); ATTRIBUTE(href)]'
            ],
            'process_path_to_element': [
                [(enum.xpath, r'//*[@id="container"]/div[1]/div[3]/div[2]'
                              r'/div[2]/div/div/div[1]/span'),
                 (enum.text, '')],
                [(enum.class_, 'final-cost'),
                 (enum.num, '0'),
                 (enum.text, '')],
                [(enum.id, 'photo'),
                 (enum.tag, 'a'),
                 (enum.attr, 'href')]
            ]
        },
        r'[CLASS(final-cost); NUM(0); TEXT][ID(photo); TAG(a); '
        r'ATTRIBUTE(href)]': {
            'split_by_brackets': [
                r'[CLASS(final-cost); NUM(0); TEXT]',
                r'[ID(photo); TAG(a); ATTRIBUTE(href)]'],
            'process_path_to_element': [
                [(enum.class_, 'final-cost'),
                 (enum.num, '0'),
                 (enum.text, '')],
                [(enum.id, 'photo'),
                 (enum.tag, 'a'),
                 (enum.attr, 'href')]
            ]
        }
    }

    def test_split_by_brackets(self):
        for input_string, result_dict in self.test_data_dict.items():
            real_result = SiteConfigParser.split_by_brackets(input_string, '[]')
            correct_result = result_dict.get('split_by_brackets')
            self.assertEqual(real_result, correct_result)

    def test_process_path_to_element(self):
        for input_string, result_dict in self.test_data_dict.items():
            correct_result = result_dict.get('process_path_to_element')
            result = SiteConfigParser.process_path_to_element(input_string)
            real_result = [[(elem.type, elem.identifier) for elem in seq]
                 for seq in result]
            self.assertEqual(real_result, correct_result)
