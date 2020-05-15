from datetime import datetime

from dateutil.tz import UTC


def utcnow():
    """
    Like built-in utcnow, but always returns time-aware datetime instead of naive
    """
    return datetime.utcnow().replace(tzinfo=UTC)


def timestamp_to_datetime(timestamp):
    """
    Takes a unix timestamp (seconds), converts to datetime
    """
    return datetime.utcfromtimestamp(timestamp).replace(tzinfo=UTC)
