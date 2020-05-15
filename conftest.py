import pytest


from alvinchow.redis.connection import configure_connection, get_connection


DEFAULT_REDIS_ALIAS = 'default'


@pytest.fixture(autouse=True, scope='session')
def initialsetup():
    configure_connection(DEFAULT_REDIS_ALIAS, host='localhost')


@pytest.fixture
def conn():
    return get_connection(DEFAULT_REDIS_ALIAS)


@pytest.yield_fixture(autouse=True)
def commonsetup():
    # Clear Redis between tests
    conn = get_connection(DEFAULT_REDIS_ALIAS)
    conn.flushdb()
    yield None
