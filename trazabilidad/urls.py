from django.conf.urls import patterns, url, include
from django.contrib.auth.views import login, logout
from trazabilidad.views import *

urlpatterns = patterns('apavirch.trazabilidad.views',
                       
    #-- funciones de la web --#                   
    #url(r'^$',reportAll),

)