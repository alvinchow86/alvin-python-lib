import functools
from sqlalchemy.orm.exc import NoResultFound

from alvinchow.sqlalchemy.exceptions import NotFoundError


def instance_or_id(value, getter, exception=None):
    """
    Given a value, returns the object instance. If it looks like an ID type, fetches from DB
    """
    if isinstance(value, (int, str)):
        try:
            instance = getter(value)
        except NotFoundError:
            if exception:
                raise exception()
            else:
                raise NotFoundError()
    else:
        instance = value

    return instance


def coerce_to_id(value):
    if isinstance(value, (int, str)):
        return value
    else:
        return value.id


def handle_db_not_found(raise_default=True, exception=NotFoundError):
    """
    Decorator to handle catching SQLALchemy NoResultFound error, transform to NotFoundError

    Add raise_exception=True/False
    """

    def wrap(func):
        @functools.wraps(func)
        def wrapped_func(*args, raise_exception=raise_default, **kwargs):
            try:
                result = func(*args, **kwargs)
            except NoResultFound:
                if raise_exception:
                    raise exception()
                else:
                    return None
            return result

        return wrapped_func

    return wrap
