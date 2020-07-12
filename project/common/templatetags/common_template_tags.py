import urllib.parse as urlparse

from django import template

from common.helpers import add_get_param_to_url


register = template.Library()


@register.simple_tag
def add_param_to_url(url, param, value):
    """Добавляет GET параметр в запрос"""
    new_url = add_get_param_to_url(url, {param: value})
    return f'?{urlparse.urlparse(new_url).query}'
