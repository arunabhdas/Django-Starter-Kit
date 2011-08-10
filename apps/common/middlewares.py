"""
This module contains some custom middlewares
Docs about default middlewares in django can be found at https://docs.djangoproject.com/en/dev/ref/middleware/
"""
import re

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect

from common.utils import get_timezone_from_offset


class SetCookieForProtectedEnvironment(object):
    COOKIE_NAME = 'admin_secret'
    
    def process_request(self, request):
        if not self.is_secret_protected(request) or (self.is_secret_protected(request) and\
            self.COOKIE_NAME in request.COOKIES) or request.GET.has_key(settings.ADMIN_SECRET):
            return None
        return HttpResponse("Access Denied")
    
    def process_response(self, request, response):
        if self.is_secret_protected(request) and not self.COOKIE_NAME in request.COOKIES and\
            request.GET.has_key(settings.ADMIN_SECRET):
            response.set_cookie(self.COOKIE_NAME, True, max_age = 365 * 24 * 60 * 60)
        return response
    
    def is_secret_protected(self, request):
        return (not settings.DEBUG and request.path.startswith('/admin'))


class ExceptionUserInfoMiddleware(object):
    """
    Adds user details to request context on receiving an exception, so that they show up in the error emails.
    
    Add to settings.MIDDLEWARE_CLASSES and keep it outermost or on top if possible. This allows
    it to catch exceptions in other middlewares as well.
    """
    
    def process_exception(self, request, exception):
        """
        Process the exception.
            `request` - request that caused the exception
            `exception` - actual exception being raised
        """
        try:
            if request.user.is_authenticated():
                request.META['USERNAME'] = str(request.user.username)
                request.META['USER_EMAIL'] = str(request.user.email)
        except:
            pass


class CookieToUserTimezone():
    def process_request(self, request):
        """
        Populates user_profile.timezone with timezone offset set by javascript.
        """
        minutes = int(request.COOKIES.get('timezone_offset') or 0)
        tz = get_timezone_from_offset(minutes)
        
        if request.user.is_authenticated():
            pass
            # Process timezone, or save to db etc.
