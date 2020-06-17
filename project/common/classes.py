class BaseEnumerate:
    values = {}

    @classmethod
    def get_choices(cls):
        return [item for item in cls.values.items()]
