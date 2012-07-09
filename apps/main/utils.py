from datetime import date, datetime, timedelta

from django.conf import settings
import gc
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


def queryset_iterator(queryset, chunksize=1000):
    '''''
    Iterate over a Django Queryset ordered by the primary key

    This method loads a maximum of chunksize (default: 1000) rows in it's
    memory at the same time while django normally would load all rows in it's
    memory. Using the iterator() method only causes it to not preload all the
    classes.

    Note that the implementation of the iterator does not support ordered query sets.
    
    Source: http://djangosnippets.org/snippets/1949/
    '''
    pk = 0
    last_pk = queryset.order_by('-pk')[0].pk
    queryset = queryset.order_by('pk')
    while pk < last_pk:
        for row in queryset.filter(pk__gt=pk)[:chunksize]:
            pk = row.pk
            yield row
        gc.collect()
