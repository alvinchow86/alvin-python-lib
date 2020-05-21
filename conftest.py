import os
import pytest

from alvinchow.redis.connection import configure_connection, get_connection

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, configure_mappers
from sqlalchemy.ext.declarative import declarative_base


DEFAULT_REDIS_ALIAS = 'default'
database_url = os.environ.get('DATABASE_URL', 'postgres://root:@localhost/postgres')


@pytest.fixture(autouse=True, scope='session')
def initialsetup():
    configure_connection(DEFAULT_REDIS_ALIAS, host='localhost')


@pytest.fixture
def redis_conn(redis):
    return get_connection(DEFAULT_REDIS_ALIAS)


@pytest.yield_fixture
def redis():
    # Clear Redis between tests
    conn = get_connection(DEFAULT_REDIS_ALIAS)
    conn.flushdb()
    yield None


# --------------------
# Sqlalchemy fixtures
# --------------------


# This is a dummy thing, tests can override this to declare custom classes
@pytest.fixture
def init_models():
    pass


@pytest.fixture
def Base():
    return declarative_base()


@pytest.fixture
def engine():
    engine = create_engine(database_url)
    return engine


@pytest.fixture
def connection(engine):
    return engine.connect()


@pytest.yield_fixture
def session(engine, Base, init_models):
    configure_mappers()
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    session.close_all()
    Base.metadata.drop_all(engine)
    engine.dispose()
