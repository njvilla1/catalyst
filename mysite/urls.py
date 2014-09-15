from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
#from mysite import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    url(r'^catalyst/', include ('catalyst.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG :
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )
