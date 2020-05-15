import pytest
from sqlalchemy import Column, Text, Integer

from alvinchow.sqlalchemy.exceptions import DatabaseError
from alvinchow.sqlalchemy.session import commit_session_or_raise


class FooError(Exception):
    pass


@pytest.fixture
def Foo(Base):
    class Foo(Base):
        __tablename__ = 'foo'
        id = Column(Integer, primary_key=True)
        name = Column(Text)

    return Foo


@pytest.fixture
def init_models(Foo):
    pass


def test_commit_session_or_raise(Foo, session):
    foo = Foo(id=1, name='foo')
    session.add(foo)
    commit_session_or_raise(session)

    def make_db_error():
        foo2 = Foo(id=1, name='bar')
        session.add(foo2)

    # Try to make a DB error (unique id constraint)
    make_db_error()
    with pytest.raises(DatabaseError):
        commit_session_or_raise(session)

    make_db_error()
    with pytest.raises(FooError):
        commit_session_or_raise(session, exception=FooError)

    make_db_error()
    with pytest.raises(Exception):
        commit_session_or_raise(session, exception=None)
