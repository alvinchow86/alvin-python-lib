from enum import Enum

from sqlalchemy import types


class Text(types.TypeDecorator):
    """ Ensures we do not store blank strings, only NULL """

    impl = types.Text

    def process_bind_param(self, value, dialect):
        value = value or None
        return value


class EnumText(types.TypeDecorator):
    """
    Let's you pass in Enum as well as strings
    """
    impl = Text

    def process_bind_param(self, value, dialect):
        if value:
            if isinstance(value, Enum):
                value = value.value
        return value
