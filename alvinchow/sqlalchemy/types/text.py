from enum import Enum
import re

from sqlalchemy import types


MULTIPLE_SPACE_REGEX = re.compile(r'\s+')


class Text(types.TypeDecorator):
    """ Ensures we do not store blank strings, only NULL """

    impl = types.Text

    def __init__(
        self,
        strip_whitespace=False,
        replace_multiple_spaces=False,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.strip_whitespace = strip_whitespace
        self.replace_multiple_spaces = replace_multiple_spaces

    def process_bind_param(self, value, dialect):
        if value:
            if self.strip_whitespace:
                value = value.strip()
            if self.replace_multiple_spaces:
                value = MULTIPLE_SPACE_REGEX.sub(' ', value)

        else:
            value = None
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
