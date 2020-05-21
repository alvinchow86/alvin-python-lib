class SimpleEnumMetaclass(type):
    """
    Simpler alternative to Enum that just uses strings

    This adds the ability to check membership and to iterate
    """
    def __init__(cls, name, bases, attrs):
        values = []

        for key, val in attrs.items():
            if not key.startswith('_') and isinstance(val, str):
                values.append(val)

        super(SimpleEnumMetaclass, cls).__init__(name, bases, attrs)
        cls._values = tuple(values)
        cls._values_set = set(values)

    def __iter__(cls):
        return iter(cls._values)

    def __contains__(cls, value):
        return value in cls._values_set


class SimpleEnum(metaclass=SimpleEnumMetaclass):
    pass
