import pytest
from sqlalchemy import Column, Text, Integer
from sqlalchemy.orm.exc import NoResultFound


from alvinchow.sqlalchemy.exceptions import NotFoundError
from alvinchow.sqlalchemy.utils import (
    instance_or_id, coerce_to_id,
    handle_db_not_found
)


@pytest.fixture
def Foo(Base):
    class Foo(Base):
        __tablename__ = 'foo'
        id = Column(Integer, primary_key=True)
        name = Column(Text)
        type = Column(Text)

    return Foo


@pytest.fixture
def init_models(Foo):
    pass


class FooError(Exception):
    pass


def test_instance_or_id(session, Foo):
    foo = Foo(name='foo')
    session.add(foo)
    session.commit()

    def get_foo(id):
        try:
            return session.query(Foo).filter_by(id=id).one()
        except NoResultFound:
            raise NotFoundError()

    assert instance_or_id(foo, get_foo) == foo
    assert instance_or_id(foo.id, get_foo) == foo

    bad_id = foo.id + 100
    with pytest.raises(NotFoundError):
        instance_or_id(bad_id, get_foo)

    with pytest.raises(FooError):
        instance_or_id(bad_id, get_foo, FooError)


def test_coerce_to_id(session, Foo):
    foo = Foo(name='foo')
    session.add(foo)
    session.commit()

    assert coerce_to_id(foo) == foo.id
    assert coerce_to_id(foo.id) == foo.id


def test_handle_db_not_found(session, Foo):
    foo = Foo(name='foo')
    session.add(foo)
    session.commit()

    @handle_db_not_found()
    def get_foo(id):
        return session.query(Foo).filter_by(id=id).one()

    foo_id = foo.id
    bad_id = 5555

    assert get_foo(foo_id) == foo
    assert get_foo(bad_id, raise_exception=False) is None

    with pytest.raises(NotFoundError):
        assert get_foo(bad_id)

    @handle_db_not_found(raise_default=False)
    def get_foo2(id):
        return session.query(Foo).filter_by(id=id).one()

    assert get_foo2(bad_id) is None
