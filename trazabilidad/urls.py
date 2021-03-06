from django.conf.urls import patterns, url, include
from django.contrib.auth.views import login, logout
from trazabilidad.views import *

urlpatterns = patterns('apavirch.trazabilidad.views',
                       
    #-- Index --#
    url(r'^$',index),
    (r'^grafico/simple/$', simple),
    (r'^grafico/simple2/$', simple2),

    #-- Lotes --#
    url(r'^lotes/$',lotes),
    url(r'^lotes/ingresar-lote/$',CrearLoteView.as_view()),
    url(r'^lotes/editar-lote/(?P<pk>\d+)/$',EditarLoteView.as_view()),
    url(r'^lotes/eliminar-lote/(?P<id>\d+)/$',eliminarLote),
    url(r'^lotes/extraer-lote/$',extraerLote),
    url(r'^lotes/dextraer-lote/$',dextraerLote),
    url(r'^lotes/devolver-lote/$',devolverLote),
    url(r'^lotes/lote-extraido/(?P<id>\d+)/$',loteExtraido),
    
    #-- Tambores --#
    url(r'^tambores/$',tambores),
    url(r'^tambores/fraccionar/(?P<id>\d+)/$', fraccionar),
    url(r'^tambores/tambor-fraccionado/(?P<id>\d+)/$', tamborFraccionado),

    #-- Socios --""
    url(r'^socios/$',socios),
    url(r'^socios/ingresar-socio/$',CrearSocioView.as_view()),
    url(r'^socios/editar-socio/(?P<pk>\d+)/$', EditarSocioView.as_view()),
    url(r'^socios/eliminar-socio/(?P<id>\d+)/$', eliminarSocio),
    url(r'^socios/activar-socio/$',activarSocio),
    url(r'^socios/desactivar-socio/$',desactivarSocio),
    url(r'^socios/marcas-socio/(?P<id>\d+)/$', marcasSocio),

    #-- Remitos --#
    url(r'^remitos/$', remitos),
    url(r'^remitos/ver-remito/(?P<id>\d+)/$',verRemito),

    #url(r'^remitos/ingresar-lote/$',CrearLoteView.as_view()),
    #url(r'^remitos/editar-lote/(?P<pk>\d+)/$',EditarLoteView.as_view()),
    #url(r'^remitos/eliminar-lote/(?P<id>\d+)/$',eliminarLote),
    url(r'^remitos/ingresar-remito/$',CrearRemitoView.as_view()),
    url(r'^remitos/editar-remito/(?P<pk>\d+)/$',EditarRemitoView.as_view()),
    url(r'^remitos/eliminar-remito/(?P<id>\d+)/$',eliminarRemito),

    #-- Reportes --#
    url(r'^reportes/lote-socio/(?P<id_socio>\d+)/$', PDFLoteSocioView.as_view()),
    url(r'^reportes/tambor-lote/(?P<id_lote>\d+)/$', PDFTamborLoteView.as_view()),
    url(r'^reportes/marcas-fraccionamientos/$', PDFMarcasFraccionamientosView.as_view()),
    
)