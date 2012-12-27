from django.conf.urls.defaults import patterns

from teleport.views import *

urlpatterns = patterns('',
    (r'^(?P<filepath>[^/]+)/$', ApiHandler.as_view()),
)