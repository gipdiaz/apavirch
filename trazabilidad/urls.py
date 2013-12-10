from django.conf.urls import patterns, url, include
from django.contrib.auth.views import login, logout
from trazabilidad.views import *

urlpatterns = patterns('apavirch.trazabilidad.views',
                       
    #-- Index --#
    url(r'^$',index),

    #-- Lotes --#
    url(r'^lotes/$',lotes),
    url(r'^lotes/ingresar-lote/$',CrearLoteView.as_view()),
    url(r'^lotes/editar-lote/(?P<pk>\d+)/$',EditarLoteView.as_view()),
    url(r'^lotes/eliminar-lote/(?P<id>\d+)/$',eliminarLote),
    url(r'^lotes/extraer-lote/$',extraerLote),
    url(r'^lotes/devolver-lote/$',devolverLote),
    url(r'^lotes/lote-extraido/(?P<id>\d+)/$',loteExtraido),
    #url(r'^lotes/modal/$',modal),

    #-- Socios --""
    url(r'^socios/$',socios),
    url(r'^socios/ingresar-socio/$',CrearSocioView.as_view()),
    url(r'^socios/editar-socio/(?P<pk>\d+)/$', EditarSocioView.as_view()),
    url(r'^socios/activar-socio/$',activarSocio),
    url(r'^socios/desactivar-socio/$',desactivarSocio),
    #url(r'^socios/marcas-socio/(?P<pk>\d+)/$', MarcasSocioView.as_view()),
    url(r'^socios/marcas-socio/(?P<id>\d+)/$', marcasSocio),

)