from datetime import datetime

import pytest

from lastfm_backup.main import _parse_dt_into_timestamp, _chunks


@pytest.mark.parametrize(("dt_str", "expected_timestamp"), [
    ("2020-09-01", datetime(2020, 9, 1).timestamp()),
    ("2020-02-28", datetime(2020, 2, 28).timestamp()),
    ("2021-01-16 09:56.52", datetime(2021, 1, 16, 9, 56, 52).timestamp()),
    ("2021-03-19 23:52.01", datetime(2021, 3, 19, 23, 52, 1).timestamp()),
    ("2021-03-19T23:52.01", datetime(2021, 3, 19, 23, 52, 1).timestamp())
])
def test_should_parse_datetime_formats(dt_str, expected_timestamp):
    parsed_dt = _parse_dt_into_timestamp(dt_str)
    assert parsed_dt == expected_timestamp, f"Could not parse datetime string: {dt_str}, expected: {expected_timestamp}"


def test_chunking_iterable():
    chunks_iter = _chunks(n=4, iterable=range(1, 15))
    assert list(chunks_iter) == [
        (1, 2, 3, 4),
        (5, 6, 7, 8),
        (9, 10, 11, 12),
        (13, 14)
    ]
