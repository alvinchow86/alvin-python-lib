from alvinchow.lib.exceptions import BaseException, FieldErrorsMixin


class APIRequestError(BaseException):
    pass


class BadRequestError(FieldErrorsMixin, APIRequestError):
    pass


class UnauthenticatedError(APIRequestError):
    pass


class UnauthorizedError(APIRequestError):
    pass


class NotFoundError(APIRequestError):
    pass


class ServerError(APIRequestError):
    pass
