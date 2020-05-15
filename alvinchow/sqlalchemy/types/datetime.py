from dateutil.tz import UTC

from sqlalchemy import types


class UTCDateTime(types.TypeDecorator):
    """ Datetime with timezone that always ensures UTC tz """

    impl = types.DateTime(timezone=True)

    def process_bind_param(self, value, dialect):
        if value is not None:
            return value.astimezone(UTC)
