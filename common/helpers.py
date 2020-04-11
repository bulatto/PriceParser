import os

from config.settings import BASE_DIR


def relative_path(path):
    """Возвращает относительный путь от корневой директории проекта
    :param path: абсолютный путь к файлу или папке
    :return: относительный путь к файлу или папке
    """
    return os.path.relpath(os.path.abspath(path), BASE_DIR)


def check_or_create_dir(directory):
    """Если директория не существует, то она создаётся"""
    if not os.path.exists(directory):
        os.mkdir(directory)
