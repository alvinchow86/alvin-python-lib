from alvinchow.lib.config.values import Value


class ConfigurationMetaclass(type):
    def __init__(cls, name, bases, attrs):
        super(ConfigurationMetaclass, cls).__init__(name, bases, attrs)

        for key, val in attrs.items():
            if isinstance(val, Value):
                # Let Value know its own name
                val.set_name(key)


class Configuration(metaclass=ConfigurationMetaclass):
    """
    Set these class variables:

    - required_values: tuple() of strings or Values to override as being required
      (alternative to doing Value(required=True))
    """
    required_values = ()

    def __init__(self):
        self._values = {}   # track a separate dictionary
        self.required_values_set = set()

        for value in self.required_values:
            if isinstance(value, str):
                value = getattr(self, value)
            self.required_values_set.add(value)

    def setup(self):
        uppercase_attrs = get_uppercase_attrs(self)
        for key, item in uppercase_attrs.items():
            required_override = False
            if item in self.required_values_set:
                required_override = True

            if isinstance(item, Value):
                value = item.get_value(required=required_override)
            else:
                value = item
            setattr(self, key, value)
            self._values[key] = value

    @property
    def values(self):
        return self._values


def get_uppercase_attrs(obj):
    attrs = {}
    for key in dir(obj):
        if not key.startswith('_') and key == key.upper():
            value = getattr(obj, key)
            attrs[key] = value

    return attrs
