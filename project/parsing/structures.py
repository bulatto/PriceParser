from parsing.enum import IdentifierEnum


class ParsingElement:
    """Класс для обозначения единичного элемента на странице.
    Используется в качестве единицы последовательности для парсинга
    """

    type = None
    identifier = None
    # Идентификаторы, для которых не нужны параметры
    no_need_for_param = [IdentifierEnum.text]

    def __init__(self, type, identifier):
        assert isinstance(type, int)

        self.type = type
        self.identifier = (
            identifier if identifier not in self.no_need_for_param else None)

    @property
    def verbose_type(self):
        if self.type is not None and self.type in IdentifierEnum.values:
            return IdentifierEnum.values[self.type]

    def __str__(self):
        return f'ParsingElement(type={self.verbose_type},id={self.identifier})'
