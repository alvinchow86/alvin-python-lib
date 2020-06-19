from enum import Enum

import pytest

from datetime import datetime
from dateutil.tz import gettz, UTC
from sqlalchemy import Column, Integer

from alvinchow.sqlalchemy.types import (
    UTCDateTime, Text, EnumText, JSONB, JSON, EncryptedText
)
from alvinchow.lib.encryption import FernetEngine


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


key1 = 'bJQNtzcUHyIhi2_msM3JUWLFDFUbXfgJKqLB2lgI5oU='
key2 = 'IXIe0MFRXddkpqPzzP5AgQnTxtkNnhPQ6ozI_c2aLLM='


@pytest.fixture
def Secret(Base):
    class Secret(Base):
        __tablename__ = 'secret'
        id = Column(Integer, primary_key=True)
        secret1 = Column(EncryptedText(engine=FernetEngine(key1), preprocess=lambda x: x.upper()))
        secret2 = Column(EncryptedText(key=key1))
        secret3 = Column(EncryptedText(keys=[key1, key2]))

    return Secret


@pytest.fixture
def init_models(User, Secret):
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


def test_encrypted_text_type(session, Secret):
    secret = Secret(
        secret1='foo',
        secret2='bar',
        secret3='baz',
    )
    session.add(secret)
    session.commit()
    secret = session.query(Secret).first()

    assert secret.secret1 == 'FOO'
    assert secret.secret2 == 'bar'
    assert secret.secret3 == 'baz'
