import functools


def raises_exception_or_none(raise_default=True, allowed_exception=None, allowed_exceptions=None):
    """
    Decorates a function to take in a raise_exception arg, which is set to False, will suppress
    raising exceptions if its instance of allowed_exception.

    Addes a raise_exception argument to a function
    """

    if allowed_exception:
        allowed_exceptions = (allowed_exception,)
    else:
        allowed_exceptions = allowed_exceptions or (Exception,)

    def wrapper(func):
        @functools.wraps(func)
        def wrapped_func(*args, raise_exception=raise_default, **kwargs):
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                if not raise_exception and isinstance(e, allowed_exceptions):
                    return None
                raise e
            return result

        return wrapped_func

    return wrapper
