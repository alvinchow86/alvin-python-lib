from datetime import datetime

from alvinchow.lib.dates import utcnow, timestamp_to_datetime
from dateutil.tz import UTC


def test_utcnow():
    now = utcnow()
    assert now.tzinfo == UTC


def test_timestamp_to_datetime():
    dt = timestamp_to_datetime(1546300800)
    assert dt == datetime(2019, 1, 1, 0, tzinfo=UTC)
