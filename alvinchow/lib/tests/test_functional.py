import pytest

from alvinchow.lib.functional import raises_exception_or_none


class FooError(Exception):
    pass


class BarError(Exception):
    pass


def test_raises_exception_or_none():
    # Catch all
    @raises_exception_or_none()
    def func_anyexception():
        raise FooError()

    with pytest.raises(FooError):
        func_anyexception()

    assert func_anyexception(raise_exception=False) is None

    # Single allowed_exception
    @raises_exception_or_none(allowed_exception=FooError)
    def func_allowed_exception(exc=None):
        if exc:
            raise exc
        return 1

    assert func_allowed_exception() == 1
    assert func_allowed_exception(FooError, raise_exception=False) is None
    with pytest.raises(BarError):
        func_allowed_exception(BarError)

    # Multiple allowed_exceptions
    @raises_exception_or_none(allowed_exceptions=(FooError, BarError))
    def func_allowed_exceptions(exc=None):
        if exc:
            raise exc
        return 1

    assert func_allowed_exceptions(BarError, raise_exception=False) is None

    # raise_default arg
    @raises_exception_or_none(raise_default=False, allowed_exception=FooError)
    def func_raise_default_false(exc=None):
        if exc:
            raise exc
        return 1

    assert func_raise_default_false(FooError) is None
