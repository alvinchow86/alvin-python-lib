from enum import Enum

import pytest

from datetime import datetime
from dateutil.tz import gettz, UTC
from sqlalchemy import Column, Integer

from alvinchow.sqlalchemy.types import (
    UTCDateTime, Text, EnumText, JSONB, JSON
)


class Category(Enum):
    FOO = 'foo'
    BAR = 'bar'


@pytest.fixture
def User(Base):
    class User(Base):
        __tablename__ = 'user'
        id = Column(Integer, primary_key=True)
        created_at = Column(UTCDateTime)
        name = Column(Text)
        category = Column(EnumText)
        data = Column(JSONB)
        stuff = Column(JSON)

    return User


@pytest.fixture
def init_models(User):
    pass


def test_utcdatetime_type(session, User):
    """
    Test that UTCDatetime works
    """
    ptz = gettz('US/Pacific')
    local_time = datetime(2019, 1, 1, 12, 0, tzinfo=ptz)  # 12pm PST, 20pm UTC
    user = User(created_at=local_time)
    session.add(user)
    session.commit()

    # tzinfo should be converted properly
    user = session.query(User).filter_by(id=user.id).first()
    assert user.created_at == datetime(2019, 1, 1, 20, 0, tzinfo=UTC)


def test_text_type(session, User):
    user1 = User(name='asdf')
    session.add(user1)
    session.commit()

    user1 = session.query(User).filter_by(id=user1.id).first()
    assert user1.name == 'asdf'

    user2 = User(name='')
    session.add(user2)
    session.commit()

    user2 = session.query(User).filter_by(id=user2.id).first()
    assert user2.name is None


def test_enum_text_type(session, User):
    user = User(category=Category.FOO)
    session.add(user)
    session.commit()

    assert user.category == 'foo'
