from time import sleep


def open_parser(function):
    """Декоратор для открытия парсера с возможностью повторной попытки"""
    def fun(self):
        for i in range(2):
            try:
                function(self)
                break
            except:
                print('Произошла ошибка при открытии сайта!')
            sleep(1)
    return fun