from alvinchow.redis.cache.cache import RedisCache
from alvinchow.redis.connection import get_connection


# Global map of cache instances
caches = {}


def get_cache(alias="default"):
    try:
        cache = caches[alias]
    except KeyError:
        connection = get_connection(alias)
        cache = RedisCache(connection)
        caches[alias] = cache

    return cache
