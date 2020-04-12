import os
import random
import requests
from urllib.parse import urlparse

from config.settings import GOODS_IMAGE_PATH
from .exceptions import (
    UnsupportedFileFormat, FileNotDownloaded, PhotoDownloaderException)


class PhotoDownloader:
    """Класс, отвечающий за загрузку изображения по ссылке"""

    photo_url = None
    supported_formats = ['jpg', 'png', 'jpeg']

    def __init__(self, url=None):
        self.photo_url = url

    def get_file_format(self):
        """Получает расширение файла изображения для дальнейшей обработки
        :raise: FileNotDownloaded, UnsupportedFileFormat
        """
        url_path = urlparse(self.photo_url).path.lower()
        if not url_path:
            raise FileNotDownloaded(self.photo_url)
        for f in self.supported_formats:
            if url_path.endswith(f):
                return f
        raise UnsupportedFileFormat(url_path)

    @staticmethod
    def generate_file_name(img_format):
        """Генерирует имя файла изображения, проверяет, что имя уникально
        :param img_format: Расширение файла изображения
        """
        is_unique = False
        file_name = None
        while not is_unique:
            random_num = random.randint(100, 10 ** 6)
            file_name = f'img_{random_num}.{img_format}'
            is_unique = not os.path.exists(file_name)
        return file_name

    def get_file_name(self):
        """Определяет формат изображения и возвращает путь к новому файлу.
        Если папка не существует, она создаётся
        """
        if not os.path.exists(GOODS_IMAGE_PATH):
            os.makedirs(GOODS_IMAGE_PATH)
        image_format = self.get_file_format()
        file_name = self.generate_file_name(image_format)
        return file_name

    def _download(self):
        """Загружает изображение по ссылке и возвращает 2 значения:
        признак успешного завершения и путь до файла, если не было ошибок
        :raise: FileNotDownloaded"""

        img = requests.get(self.photo_url)
        if (img.status_code != 200 or not img.content or
                not img.headers['Content-Type'].startswith('image')):
            raise FileNotDownloaded(self.photo_url)
        file_name = self.get_file_name()
        try:
            full_file_name = os.path.join(GOODS_IMAGE_PATH, file_name)
            with open(full_file_name, "wb") as out:
                out.write(img.content)
            return True, file_name
        except Exception as e:
            print(f'Произошла ошибка при сохранении картинки: {e}')
            return False, None

    def download(self):
        """Скачивает изображение по ссылке и возвращает признак успешности
        завершения операции и путь до файла (если возникли ошибки то путь до
        до дефолтного изображения), а также сообщение об ошибке (если есть)
        """
        success = False
        file_name = None
        error = ''

        try:
            if not self.photo_url:
                raise FileNotDownloaded()
            success, file_name = self._download()
        except (PhotoDownloaderException, requests.RequestException) as e:
            error = e

        photo_path = file_name if success else None
        return success, photo_path, error
