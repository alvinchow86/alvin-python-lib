import os

import pytest

from alvinchow.lib.config import Configuration, Value
from alvinchow.lib.config.values import IntegerValue, FloatValue, BooleanValue, ListValue
from alvinchow.lib.config.exceptions import RequiredValueNotSet


def test_config_basic(mocker):

    class FooConfig(Configuration):
        DB_URL = Value()
        DEBUG_LEVEL = Value('INFO')
        HARDCODED_THING = 'hard'
        INT_VALUE = IntegerValue(1)
        FLOAT_VALUE = FloatValue(2.0)
        BOOL_VALUE = BooleanValue(False)
        BOOL_VALUE_TRUE = BooleanValue(True)
        BOOL_VALUE_UNKNOWN = BooleanValue()
        LIST_VALUE = ListValue()

    config = FooConfig()
    config.setup()

    assert config.DB_URL is None
    assert config.DEBUG_LEVEL == 'INFO'
    assert config.HARDCODED_THING == 'hard'
    assert config.BOOL_VALUE is False
    assert config.INT_VALUE == 1
    assert config.FLOAT_VALUE == 2.0
    assert config.BOOL_VALUE is False
    assert config.BOOL_VALUE_TRUE is True
    assert config.BOOL_VALUE_UNKNOWN is None

    env = {
        'DB_URL': 'localhost',
        'DEBUG_LEVEL': 'WARNING',
        'INT_VALUE': '123',
        'FLOAT_VALUE': '4.5',
        'BOOL_VALUE': 'true',
        'BOOL_VALUE_TRUE': 'false',
        'BOOL_VALUE_UNKNOWN': 'asdf',
        'LIST_VALUE': 'one,two, three '
    }
    mocker.patch.dict(os.environ, env)

    config = FooConfig()
    config.setup()

    assert config.DB_URL == 'localhost'
    assert config.DEBUG_LEVEL == 'WARNING'
    assert config.INT_VALUE == 123
    assert config.FLOAT_VALUE == 4.5
    assert config.BOOL_VALUE is True
    assert config.BOOL_VALUE_TRUE is False
    assert config.BOOL_VALUE_UNKNOWN is None
    assert config.LIST_VALUE == ['one', 'two', 'three']

    assert config.values['DB_URL'] == 'localhost'

    # Check __repr__
    assert 'DB_URL' in repr(FooConfig.DB_URL)


def test_required_value(mocker):
    class Config(Configuration):
        DB_URL = Value(required=True)

    config = Config()

    with pytest.raises(RequiredValueNotSet):
        config.setup()

    env = {
        'DB_URL': 'postgres://foo:bar@something.com',
    }
    mocker.patch.dict(os.environ, env)

    config = Config()
    config.setup()
    assert config.DB_URL


def test_required_values_override_option(mocker):
    """
    Test alternative way to set required values
    """
    class Base(Configuration):
        DB_URL = Value()
        REDIS_URL = Value()

    class Production(Base):
        required_values = ('DB_URL', Base.REDIS_URL)

    config = Production()

    with pytest.raises(RequiredValueNotSet):
        config.setup()

    env = {
        'DB_URL': 'postgres://foo:bar@something.com',
        'REDIS_URL': 'redis://something',
    }
    mocker.patch.dict(os.environ, env)

    config = Production()
    config.setup()
    assert config.DB_URL
    assert config.REDIS_URL
