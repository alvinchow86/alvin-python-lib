import pytest

from functools import partial

from alvinchow.redis.lock import Lock as Lock, LockTimeoutError

pytestmark = pytest.mark.usefixtures('redis')


DefaultLock = partial(Lock, connection_alias='default')


@pytest.fixture
def conn(redis_conn):
    return redis_conn


def test_lock_basic(conn):
    lock1 = Lock('foo', connection=conn, expiration=60)
    assert lock1.acquire() is True

    assert conn.get('locks:foo') == b'1'

    lock2 = Lock('foo', connection_alias='default', expiration=60)
    assert lock2.acquire() is False

    lock1.release()

    assert not conn.exists('locks:foo')

    assert lock2.acquire() is True


def test_lock_context_manager(conn):
    foo_lock = DefaultLock('foo')

    x = 5
    with foo_lock as lock:
        assert lock.acquired
        x += 1

    assert x == 6


def test_lock_context_manager_exceptions(conn):
    lock1 = DefaultLock('foo')
    lock1.acquire()

    with pytest.raises(LockTimeoutError):
        with DefaultLock('foo'):
            print('should not run')    # pragma: no cover


def test_lock_no_timeout_exception_usage(conn):
    lock1 = DefaultLock('foo')
    lock1.acquire()

    with DefaultLock('foo', raise_timeout_exception=False) as lock:
        assert lock.acquired is False
