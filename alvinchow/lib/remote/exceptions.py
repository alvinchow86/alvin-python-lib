from alvinchow.lib.exceptions import BaseException, FieldErrorsMixin


class ApiRequestErroruestError(BaseException):
    pass


class BadRequestError(FieldErrorsMixin, ApiRequestErroruestError):
    pass


class UnauthenticatedError(ApiRequestErroruestError):
    pass


class UnauthorizedError(ApiRequestErroruestError):
    pass


class NotFoundError(ApiRequestErroruestError):
    pass


class ServerError(ApiRequestErroruestError):
    pass
