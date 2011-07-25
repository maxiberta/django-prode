from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'django_prode.views.index', {}, 'frontpage'),
)
