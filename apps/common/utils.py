from datetime import date, datetime, timedelta

from django.conf import settings
import pytz


def get_timezone_from_offset(minutes, default='US/Eastern'):
    """
    Return pytz timezone give offset in minutes. If none found, then returns the EST as the default timezone.
    Javascript sends offset in minutes. -120 = GMT+0200, we're storing that in  request.COOKIES.get('timezone_offset')
    
    minutes = request.COOKIES.get('timezone_offset') or 0
    """
    if minutes < 0:
        minutes = -minutes
        minus = True
    else:
        minus = False

    min = minutes % 60
    hours = (minutes - min) / 60
    offset = "%s%02d%02d" % (minus and "+" or "-", hours, min)

    # This is only method I found to determine timezone by offset.
    # HACK: doing reversed(), to match offset 240, to EST instead of AST
    for tz in reversed(pytz.common_timezones):
        now = datetime.now(pytz.timezone(tz))
        if now.strftime("%z") == offset:
            return tz
    return pytz.timezone(default)
