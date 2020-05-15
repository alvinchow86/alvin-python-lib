from alvinchow.lib.exceptions import BaseException, FieldErrorsMixin


class DatabaseError(BaseException):
    pass


class NotFoundError(DatabaseError):
    pass


class MutationError(FieldErrorsMixin, DatabaseError):
    """ This is for Update, Create, Delete operations """
    pass


class UpdateError(MutationError):
    pass


class CreateError(MutationError):
    pass


class DeleteError(MutationError):
    pass
