from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^ask', 'tracking.views.ask'),
    (r'^dicts/update_order/(?P<id>\d*)', 'tracking.views.my_dicts_update_order'),
    (r'^dicts/update_order', 'tracking.views.my_dicts_update_order'),
    (r'^dicts', 'tracking.views.dicts'),
    (r'^mydics/add/(?P<id>\d+)', 'tracking.views.add_to_mydics'),
    (r'^mydics/remove/(?P<id>\d+)', 'tracking.views.remove_from_mydics'),
    (r'^loader.js', 'tracking.views.loader'),
    (r'^/?$', 'tracking.views.index'),
)
