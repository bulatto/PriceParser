import os

from django.core.exceptions import ImproperlyConfigured

from config.settings.base import BASE_DIR
from config.settings.base import LOGS_DIR

from .enum import SeleniumProgramEnum
from .settings import parser_settings


# Определение секции Selenium
if not parser_settings.has_section('Selenium'):
    raise ImproperlyConfigured(
        'В файлах настроек парсера не найдена секция Selenium')
selenium_section = parser_settings['Selenium']


# Настройка видимости сайта при парсинге с помощью Selenium (по умолчанию False)
SELENIUM_VISIBLE = bool(selenium_section.getboolean('VISIBLE'))


# Путь до логов парсера Selenium
SELENIUM_LOGS_FILE = os.path.join(LOGS_DIR, 'selenium.log')


# Выбор программы для Selenium парсера
webdriver_type = selenium_section.get('SELENIUM_WEBDRIVER_TYPE')
if not webdriver_type:
    raise ImproperlyConfigured(
        'Параметр SELENIUM_WEBDRIVER_TYPE не заполнен')
SELENIUM_WEBDRIVER_TYPE = SeleniumProgramEnum.get_program_type(webdriver_type)


# Файл вебдрайвера для Selenium
SELENIUM_WEBDRIVER_FILE = selenium_section.get('WEBDRIVER_FILE')
if not SELENIUM_WEBDRIVER_FILE:
    raise ImproperlyConfigured(
        f'Не определён параметр WEBDRIVER_FILE для парсера Selenium')
elif not os.path.exists(os.path.join(
        BASE_DIR, 'additional_files', SELENIUM_WEBDRIVER_FILE)):
    raise ImproperlyConfigured(
        f'Файл, описанный в WEBDRIVER_FILE для парсера Selenium, отсутствует')
