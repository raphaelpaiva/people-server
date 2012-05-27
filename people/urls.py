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
    
    url(r'^api/sincronizar/(?P<email>.*)', 'people.views.sincronizar', name='sincronizar'),

    url(r'^api/get_usuario/(?P<usuario_id>[0-9]+)', 'people.views.get_usuario', name='get_usuario'),

    url(r'^api/get_agenda/(?P<agenda_id>[0-9]+)', 'people.views.get_agenda', name='get_agenda'),

    url(r'^api/get_contato/(?P<contato_id>[0-9]+)', 'people.views.get_contato', name='get_contato'),
)
