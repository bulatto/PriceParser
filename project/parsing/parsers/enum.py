from django.core.exceptions import ImproperlyConfigured

from common.constants import BaseEnumerate


class SeleniumProgramEnum(BaseEnumerate):
    Chrome = 0
    Firefox = 1

    values = {
        Chrome: 'Chrome',
        Firefox: 'Firefox',
    }

    @classmethod
    def get_program_type(cls, string_type):
        for program_type, str_type in cls.values.items():
            if str_type == string_type:
                return program_type
        raise ImproperlyConfigured(
            f'Указан некорректный тип парсера Selenium - {string_type}')
