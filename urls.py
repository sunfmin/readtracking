from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^ask', 'tracking.views.ask'),
    (r'^loader.js', 'tracking.views.loader'),
    (r'^/?$', 'tracking.views.index'),
)
