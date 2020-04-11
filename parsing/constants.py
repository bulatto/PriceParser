TASK_TIMEOUT = 3 * 60
PRICE_NOT_FOUNDED = 'Цена не найдена'
link_to_index_page = "<a href='/'>Вернуться на главную страницу</a>"


class BaseEnumerate:
    values = {}

    @classmethod
    def get_choices(cls):
        return [(value, key) for key, value in cls.values.items()]
