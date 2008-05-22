from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    (r'^contents/create', 'contents.views.create'),
    (r'^contents/new', 'contents.views.new'),
    (r'^contents/(?P<id>\d+)', 'contents.views.show'),
    (r'^contents/', 'contents.views.index'),
    (r'^/?$', 'contents.views.index'),

    # Uncomment this for admin:
#     (r'^admin/', include('django.contrib.admin.urls')),
)
