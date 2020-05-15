from urllib.parse import urlparse

import redis

from alvinchow.redis.exceptions import RedisConfigurationError


__all__ = ['get_connection', 'get_redis_connection', 'configure_connection']


# Global map of Redis connections
connections = {}

# Map of Redis connection configurations
connection_configs = {}


def get_connection(alias):
    try:
        connection = connections[alias]
    except KeyError:
        connection = _create_connection(alias)
    return connection


def configure_connection(alias: str, host='localhost', port=6379, password='', url=None, **extra_settings):
    """
    Save Redis connection args (host, credentials) and map them to an "alias"
    """
    if url:
        # Just pass in RFC URL string
        url_parsed = urlparse(url)
        host = url_parsed.hostname or host
        port = url_parsed.port or port
        password = url_parsed.password or password

    connection_configs[alias] = dict(
        host=host, port=port, password=password, **extra_settings
    )


def _create_connection(alias, force=False):
    try:
        connection_config = connection_configs[alias]
    except KeyError:
        raise RedisConfigurationError('Connection settings not defined for {}'.format(alias))

    if alias in connections and not force:
        raise RedisConfigurationError('Connection {} already exists'.format(alias))

    connection = redis.StrictRedis(**connection_config)

    connections[alias] = connection

    return connection


# Just an alias
get_redis_connection = get_connection
