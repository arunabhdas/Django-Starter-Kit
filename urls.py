from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',    
    url(r'^', include('home.urls')),
    #url(r'^accounts/', include('accounts.urls')),
    url(r'^admin/', include(admin.site.urls)),    
)

if settings.DEBUG:
    urlpatterns += (
        url(r'^media/(.*)$', 'django.views.static.serve', kwargs={'document_root': settings.MEDIA_ROOT, 'show_indexes':True}),
    )
