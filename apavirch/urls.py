from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import patterns, include, url
from apavirch import views, settings
from django.contrib import admin
from django.contrib.auth.views import login, logout
#import notifications#############################

from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = patterns('',
    
    # Admin, login y logout
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', login, {'template_name':'admin/login.html'}),
    #url(r'^accounts/', include('registration.backends.default.urls')),
    (r'^accounts/', include('registration.backends.default.urls')),
#    url(r'^accounts/register/$', views.register, name='register'),
    #url(r'^inbox/notifications/', include(notifications.urls)),#####################
    
    #url(r'^notifications/$', views.notifications, name='notifications' ),##############
    #url(r'^autoreports/', include('autoreports.urls')),
    # Apavirch
    url(r'^$', views.index, name='index'),
    
    # Trazabilidad
    url(r'^', include('trazabilidad.urls')),

    # Media y Static PATH
    (r'^media/(?P<path>.*)$','django.views.static.serve',
        {'document_root':settings.MEDIA_ROOT}),
    (r'^static/(?P<path>.*)$','django.views.static.serve',
        {'document_root': settings.STATIC_ROOT})
)
