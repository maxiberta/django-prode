from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'fixture.views.index', {}, 'frontpage'),
)
