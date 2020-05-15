from alvinchow.redis.connection import get_connection


class LockError(Exception):
    pass


class LockTimeoutError(LockError):
    pass


DEFAULT_EXPIRATION_SECONDS = 300   # warning this should be longer than the max time it takes


class Lock:
    """
    Non-blocking Redis lock, using SETNX

    Does not implement retries or anything yet. Does not block.
    """

    redis_prefix = 'locks'

    def __init__(
        self,
        key: str,
        connection=None,
        connection_alias: str = None,
        expiration: int = DEFAULT_EXPIRATION_SECONDS,
        raise_timeout_exception: bool = True
    ):
        self.key = key
        self.expiration = expiration or DEFAULT_EXPIRATION_SECONDS  # make sure its set
        self.raise_timeout_exception = raise_timeout_exception

        assert connection or connection_alias, 'Must provide either a Redis connection or a connection alis'
        if connection_alias:
            self.connection = get_connection(connection_alias)
        else:
            self.connection = connection

        self.acquired = False

    def acquire(self):
        lock_acquired = self._set_lock()
        return lock_acquired

    def release(self):
        self._unset_lock()

    def _set_lock(self):
        redis_key = self._get_redis_key()
        success = self.connection.set(redis_key, 1, nx=True, ex=self.expiration)
        return bool(success)

    def _unset_lock(self):
        redis_key = self._get_redis_key()
        self.connection.delete(redis_key)

    def _get_redis_key(self):
        return '{}:{}'.format(self.redis_prefix, self.key)

    def __enter__(self):
        lock_acquired = self.acquire()
        if not lock_acquired and self.raise_timeout_exception:
            raise LockTimeoutError('Could not acquire lock')

        self.acquired = lock_acquired   # this is just for the raise_timeout_exception=False usage

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.acquired:
            self.release()

        self.acquired = False   # reset it
