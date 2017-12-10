from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'configuration.views.configuration', name='configuration'),

    url(r'^admin/', include(admin.site.urls)),
)
