# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'people.views.home', name='home'),
    # url(r'^people/', include('people.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^api/download_agenda/(?P<email>.*)', 'people.views.download_agenda', name='download_agenda'),
    url(r'^api/upload_agenda/(?P<email>.*)', 'people.views.upload_agenda', name='upload_agenda'),

)
