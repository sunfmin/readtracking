from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    (r'^contents/', 'contents.views.index'),

    # Uncomment this for admin:
#     (r'^admin/', include('django.contrib.admin.urls')),
)