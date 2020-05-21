import pytest

import copy

from alvinchow.redis import connection
from alvinchow.redis.connection import (
    get_connection, configure_connection, _create_connection,
    connections
)
from alvinchow.redis.exceptions import RedisConfigurationError

pytestmark = pytest.mark.usefixtures('redis')


def test_connection():
    connection = get_connection('default')
    connection.ping()

    connection.set('foo', 'bar')
    assert connection.get('foo') == b'bar'


def test_connection_creation():
    connections.clear()

    connection = get_connection('default')

    assert connections['default'] == connection

    with pytest.raises(RedisConfigurationError):
        _create_connection('nonexistent')

    with pytest.raises(RedisConfigurationError):
        _create_connection('default')


def test_configure_connection_url():
    orig_connection_configs = copy.deepcopy(connection.connection_configs)

    configure_connection('default', url='redis://user:password@redis.com:6379')
    config = connection.connection_configs['default']
    assert config['host'] == 'redis.com'
    assert config['port'] == 6379
    assert config['password'] == 'password'

    # restore original settings
    connection.connection_configs = orig_connection_configs
