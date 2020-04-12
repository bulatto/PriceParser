class BaseEnumerate:
    values = {}

    @classmethod
    def get_choices(cls):
        return [(value, key) for key, value in cls.values.items()]