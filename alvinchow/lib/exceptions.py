class BaseException(Exception):
    """
    Useful base exception class, adds some common attributes (code, data) to the built-in class
    """
    def __init__(self, message=None, code=None, data=None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.data = data


class FieldError:
    """
    Helper class to store errors related to an input field (e.g. for a REST API)
    """
    def __init__(self, field, message=None, code=None):
        self.field = field
        self.message = message
        self.code = code


class FieldErrorsMixin:
    """
    Mixin to add field_errors property to an exception class
    """
    def __init__(self, *args, field_errors=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.field_errors = field_errors or []


class FieldErrorsException(FieldErrorsMixin, BaseException):
    """
    Exception that has field_errors
    """
    pass
