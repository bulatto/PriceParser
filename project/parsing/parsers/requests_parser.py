import requests
from bs4 import BeautifulSoup

from parsing.parsers.base_parser import PageParser
from parsing.parsers.helpers import open_parser


class RequestsPageParser(PageParser):
    url = None

    def __init__(self, url):
        self.url = url

    @staticmethod
    def return_bs(url):
        response = requests.get(url)
        return BeautifulSoup(response.text, "html.parser")

    @open_parser
    def open(self):
        print(f'Открытие сайта {self.url}')
        self.response = requests.get(self.url)
        self.bs = BeautifulSoup(self.response.text, "html.parser")

    def get_element_on_page(self, elem_src):
        # TODO: доработать функционал
        raise NotImplementedError()