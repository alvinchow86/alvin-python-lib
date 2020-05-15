from sqlalchemy import types
from sqlalchemy.dialects.postgresql import JSON, JSONB


class JSON(types.TypeDecorator):
    """
    Just set none_as_null=True as default
    """
    impl = JSON(none_as_null=True)


class JSONB(types.TypeDecorator):
    """
    Just set none_as_null=True as default
    """
    impl = JSONB(none_as_null=True)
