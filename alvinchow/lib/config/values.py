import os

from alvinchow.lib.config.exceptions import RequiredValueNotSet


class Value:
    def __init__(self, default_value=None, environ_name=None, required=False):
        self.default_value = default_value
        self.name = None   # always need this
        self.custom_environ_name = None
        self.required = required

    def set_name(self, name):
        self.name = name

    @property
    def environ_name(self):
        return self.custom_environ_name or self.name

    def get_value_from_environment(self):
        return os.environ.get(self.environ_name)

    def get_value(self, required=False):
        value = self.get_value_from_environment()
        if value is None:
            if self.required or required:
                raise RequiredValueNotSet('Config var {} not set'.format(self.name))
            return self.default_value
        else:
            return self.to_python(value)

    def to_python(self, value):
        """
        Subclass can override this
        """
        return value

    def __repr__(self):
        return '<Value(name={})'.format(self.name)


class IntegerValue(Value):
    def to_python(self, value):
        return int(value)


class FloatValue(Value):
    def to_python(self, value):
        return float(value)


class BooleanValue(Value):
    true_values = ('1', 'true', 'yes', 't', 'y')
    false_values = ('0', 'false', 'no', 'f', 'n')

    def to_python(self, value):
        value_lower = value.lower()
        if value_lower in self.true_values:
            return True
        elif value_lower in self.false_values:
            return False

        return None


class ListValue(Value):
    def to_python(self, value):
        return [val.strip() for val in value.split(',')]
