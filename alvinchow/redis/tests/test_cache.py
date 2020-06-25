import pytest

from alvinchow.redis.cache import get_cache, caches

pytestmark = pytest.mark.usefixtures('redis')


def test_get_cache():
    cache = get_cache("default")
    assert caches["default"] == cache
    cache = get_cache("default")


def test_cache_set_get():
    cache = get_cache("default")
    cache.set('foo', 'bar')
    assert cache.get('foo') == 'bar'
    assert cache.exists('foo') is True
    assert cache.get('asdf') is None

    cache.delete('foo')
    assert cache.get('foo') is None
    assert cache.exists('foo') is False

    items = [
        123,
        [1, 2, 3],
        {'a': 'bee', 'c': [4, 5]}
    ]
    for item in items:
        cache.set('item', item)
        assert cache.get('item') == item


def test_cache_handle_invalid(redis_conn):
    cache = get_cache("default")
    redis_conn.set('foo', b"123][]")

    assert cache.get('foo') is None

    # Set some invalid utf-8
    redis_conn.set('foo', b'asdf\x12\x9934')
    assert cache.get('foo') is None
