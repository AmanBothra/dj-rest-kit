import datetime
from types import SimpleNamespace

import pytz
from django.conf import settings

from dj_rest_kit import helpers, constants

if not settings.configured:
    settings.configure(TIME_ZONE="UTC", USE_TZ=True)


def test_get_user_timezone_from_request():
    request = SimpleNamespace(headers={"timezone": "Asia/Kolkata"})
    assert helpers.get_user_timezone_from_request(request) == "Asia/Kolkata"


def test_get_user_timezone_from_request_default():
    request = SimpleNamespace(headers={})
    assert helpers.get_user_timezone_from_request(request) == "UTC"


def test_convert_to_utc_and_back():
    tz = pytz.timezone("Asia/Kolkata")
    aware = tz.localize(datetime.datetime(2023, 1, 1, 8, 30))
    utc_dt = helpers.convert_to_utc(aware)
    assert utc_dt.tzinfo == pytz.UTC
    converted = helpers.convert_to_user_timezone(utc_dt, user_timezone="Asia/Kolkata")
    assert converted == aware


def test_convert_to_formatted_user_timezone():
    tz = pytz.timezone("Asia/Kolkata")
    aware = tz.localize(datetime.datetime(2023, 1, 1, 8, 30))
    utc_dt = helpers.convert_to_utc(aware)
    formatted = helpers.convert_to_formatted_user_timezone(utc_dt, user_timezone="Asia/Kolkata")
    assert formatted == aware.strftime(constants.DateTimeFormat.DATE_TIME)


def test_convert_user_datetime_str_to_utc():
    result = helpers.convert_user_datetime_str_to_utc("2023-01-01 08:30", "Asia/Kolkata")
    tz = pytz.timezone("Asia/Kolkata")
    aware = tz.localize(datetime.datetime(2023, 1, 1, 8, 30))
    expected = helpers.convert_to_utc(aware)
    assert result == expected
