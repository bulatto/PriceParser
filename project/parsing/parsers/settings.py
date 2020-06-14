import os
from configparser import ConfigParser

from django.core.exceptions import ImproperlyConfigured

from config.settings.base import PROJECT_SETTINGS_DIR


def get_parser_settings():
    """Возвращает объект с настройками парсеров из файла"""
    settings = ConfigParser()
    parser_setting_file_name = os.path.join(
        PROJECT_SETTINGS_DIR, 'parser_settings.txt')
    if not os.path.exists(parser_setting_file_name):
        raise ImproperlyConfigured(
            f'Файл {parser_setting_file_name} не найден!')

    settings.read(parser_setting_file_name)
    return settings


# Настройки парсеров
parser_settings = get_parser_settings()

