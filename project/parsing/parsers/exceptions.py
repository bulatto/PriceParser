class BaseParsingException(Exception):
    """Базовый класс для исключений, связанных с парсингом"""
    message = 'Произошла ошибка!'

    def __str__(self):
        return self.message


class IncorrectParserType(BaseParsingException):
    message = 'Задан некорретный тип парсера!'


class UnsupportedSiteUrl(BaseParsingException):
    message = 'Данный сайт {0} не поддерживается!'

    def __init__(self, url):
        self.message = self.message.format(url)


class ElementNotFoundedOnPage(BaseParsingException):
    message = 'Не удалось найти элемент на странице!'

    def __init__(self, elem_src=None):
        if elem_src:
            self.message += f'(type={elem_src.type}, id={elem_src.id})'


# Исключения, связанные с загрузкой файлов
class PhotoDownloaderException(BaseParsingException):
    """Базовый класс для исключений при загрузке изображения"""
    pass


class FileNotDownloaded(PhotoDownloaderException):
    message = 'Файл не был загружен!'
    message_url = 'Файл не был загружен (url={0})!'

    def __init__(self, url=None):
        if url:
            self.message = self.message_url.format(url)


class UnsupportedFileFormat(PhotoDownloaderException):
    message = 'Неподдерживаемый тип файла!'
    message_with_file = 'Неподдерживаемый тип файла (файл {0})!'

    def __init__(self, file_name=None):
        if file_name:
            self.message = self.message_with_file.format(file_name)
