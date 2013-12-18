from django.http import HttpResponse, request, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.generic import DetailView, ListView, CreateView, UpdateView
from django.contrib import auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import UserCreationForm
from django import forms 
from django.forms.models import inlineformset_factory, formset_factory
from django.template import RequestContext, Template, Context
from django.contrib.contenttypes.models import ContentType
from .models import *
from .forms import FormLote, GrupoAlzaFormSet, FormSocioEditar, FormSocio, FormMarcaSocio, MarcaFormSet, FormTambor, FormRemito, RemitoDetalleFormSet, RemitoDetalleForm

from django.forms import Form

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter
import matplotlib
import datetime 
import random
from django.utils import timezone
from apavirch import settings

#-------------------------------------------------------#
#--------------------   EXTRAS   -----------------------#

def group_required(*group_names):
    def in_groups(u):
        if u.is_authenticated():
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False
    return user_passes_test(in_groups, login_url='/')

@login_required
def index(request):
    return render_to_response('trazabilidad/index.html',context_instance=RequestContext(request))

def simple():
    cant = []
    marcas = []
    marcas_obj = Marca.objects.all().order_by("idMarca")
    for m in marcas:
        cant.append(Fraccionamiento.objects.filter(marca=marca).count())
        marcas.append(m.pk)

    fig=Figure()
    ax=fig.add_subplot(111)
    x=[]
    y=[]
    now=datetime.datetime.now()
    delta=datetime.timedelta(days=1)
    for i in range(10):
        x.append(now)
        now+=delta
        y.append(random.randint(0, 1000))
    ax.plot_date(x, y, '-')
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    canvas=FigureCanvas(fig)
    response=HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response

#-------------------------------------------------------#
#-------------------   LOTES   -------------------------#

class CrearLoteView(CreateView):
    template_name = 'trazabilidad/ingresar-lote.html'
    model = Lote
    form_class = FormLote
    success_url = '/lotes/'

    @method_decorator(group_required('Encargados de Sala','Encargados de Entrada y Salida'))
    def dispatch(self, *args, **kwargs):
        return super(CrearLoteView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        grupoAlza_form = GrupoAlzaFormSet()
        return self.render_to_response(
            self.get_context_data(form=form,
                                  grupoAlza_form=grupoAlza_form))

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        grupoAlza_form = GrupoAlzaFormSet(self.request.POST)
        if (form.is_valid() and grupoAlza_form.is_valid()):
            return self.form_valid(form, grupoAlza_form, request.user)
        else:
            return self.form_invalid(form, grupoAlza_form)

    def form_valid(self, form, grupoAlza_form, user):
        peso = 0
        for f in grupoAlza_form:
            try:
                if f.cleaned_data['peso']:
                    peso = peso + f.cleaned_data['peso']
            except KeyError:
                pass
        estado = Ingresado(observacion='Ingresado', peso=peso, operario=user)
        estado.save()
        lote = Lote(apiario=form.cleaned_data['apiario'], peso=peso, observacion=form.cleaned_data['observacion'], content_type = ContentType.objects.get_for_model(estado), object_id = estado.pk)
        lote.save()
        estado.lote = lote
        estado.save()
        grupoAlza_form.instance = lote
        grupoAlza_form.save()
        return HttpResponseRedirect('/lotes/')

    def form_invalid(self, form, grupoAlza_form):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  grupoAlza_form=grupoAlza_form))

class EditarLoteView(UpdateView):
    template_name = 'trazabilidad/editar-lote.html'
    model = Lote
    form_class = FormLote
    success_url = '/lotes/'

    @method_decorator(group_required('Encargados de Sala','Encargados de Entrada y Salida'))
    def dispatch(self, *args, **kwargs):
        return super(EditarLoteView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if GrupoAlza.objects.filter(lote=self.object).count() == 0:
            extra = 1
        else:
            extra = 0
        GrupoAlzaFormSet = inlineformset_factory(Lote, GrupoAlza, extra=extra, max_num=3, can_delete=True, fields=("idGrupoAlza","tipoAlza","lote","cantidadAlzas","peso"))
        grupoAlza_form = GrupoAlzaFormSet(instance = self.object)
        return self.render_to_response(
            self.get_context_data(form=form,
                                  grupoAlza_form=grupoAlza_form))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        grupoAlza_form = GrupoAlzaFormSet(request.POST, request.FILES, instance=self.object)
        if (form.is_valid() and grupoAlza_form.is_valid()):
            return self.form_valid(form, grupoAlza_form, request.user)
        else:
            return self.form_invalid(form, grupoAlza_form)

    def form_valid(self, form, grupoAlza_form, user):   
        #self.object = form.save()
        #grupoAlza_form.instance = self.object
        #grupoAlza_form.save()
        #return HttpResponseRedirect('/lotes/')
        peso = 0
        for f in grupoAlza_form:
            try:
                if f.cleaned_data['peso']:
                    peso = peso + f.cleaned_data['peso']
            except KeyError:
                pass
        lote = self.get_object()
        #lote = Lote.objects.get(idLote=form.cleaned_data['idLote'])
        lote.apiario = form.cleaned_data['apiario']
        lote.peso = peso
        lote.observacion = form.cleaned_data['observacion']
        lote.save()
        estado = Ingresado.objects.get(lote=lote)
        estado.peso = peso
        estado.save()
        grupoAlza_form.instance = self.object
        grupoAlza_form.save()
        return HttpResponseRedirect('/lotes/')

    def form_invalid(self, form, grupoAlza_form):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  grupoAlza_form=grupoAlza_form))

@group_required('Encargados de Sala','Encargados de Entrada y Salida','Encargados de Extraccion')
def lotes(request):
    lotes = Lote.objects.all()
    return render_to_response('trazabilidad/lotes.html',{'lotes':lotes},context_instance=RequestContext(request))

@group_required('Encargados de Sala','Encargados de Entrada y Salida')
def eliminarLote(request, id):
    lote = Lote.objects.get(pk=id)
    GrupoAlza.objects.filter(lote=lote).delete()
    lote.delete()
    return HttpResponseRedirect("/lotes/")

def extraerLote(request):
    if request.user.groups.filter(name='Encargados de Sala').exists() or request.user.groups.filter(name='Encargados de Extraccion').exists():
        if request.is_ajax():
            id = request.GET.get('id')
            peso = float(request.GET.get('peso'))
            observacion = request.GET.get('observacion')
            user = request.user
            lote = Lote.objects.get(pk=id)
            if lote.estadoActual.__class__.__name__ == "Ingresado":
                lote.extraer(user, peso, observacion)
                return HttpResponse("")
    else:
        return HttpResponse('No tiene permisos para realizar esta tarea')

def dextraerLote(request):
    if request.user.groups.filter(name='Encargados de Sala').exists() or request.user.groups.filter(name='Encargados de Extraccion').exists():
        if request.is_ajax():
            id = request.GET.get('id')
            peso = float(request.GET.get('peso'))
            observacion = request.GET.get('observacion')
            user = request.user
            lote = Lote.objects.get(pk=id)
            if (lote.estadoActual.__class__.__name__ == "Extraido") or (lote.estadoActual.__class__.__name__ == "Devuelto"):
                lote.extraerDeNuevo(user, peso, observacion)
                return HttpResponse("Lote Extraido")
            return HttpResponse("El lote no se puede extraer")
        else:
            return HttpResponse('No es una peticion Ajax')
    else:
        return HttpResponse('No tiene permisos para realizar esta tarea')

#@group_required('Encargados de Sala','Encargados de Entrada y Salida')
def devolverLote(request):
    if request.user.groups.filter(name='Encargados de Sala').exists() or request.user.groups.filter(name='Encargados de Entrada y Salida').exists():
        if request.is_ajax():
            print "entre al ajax"
            id = request.GET.get('id')
            user = request.user
            lote = Lote.objects.get(pk=id)
            if lote.estadoActual.__class__.__name__ == "Extraido":
                print "antes de devolver"
                lote.devolver(user)
                return HttpResponse("Lote Devuelto")
            return HttpResponse("El lote no se puede devolver")
        else:
            return HttpResponse('No es una peticion Ajax')
    else:
        return HttpResponse('No tiene permisos para realizar esta tarea')

#@group_required('Encargados de Sala','Encargados de Extraccion')
def loteExtraido(request, id):
    if request.user.groups.filter(name='Encargados de Sala').exists() or request.user.groups.filter(name='Encargados de Extraccion').exists():
        lote = Lote.objects.get(pk=id)
        estado = Extraido.objects.get(lote=lote)
        tambores = Tambor.objects.filter(loteExtraido=estado)
        return render_to_response('trazabilidad/lote-extraido.html',{'lote':lote, 'tambores':tambores}, context_instance=RequestContext(request))
    else:
        #return HttpResponseRedirect("/lotes/")
        msj = 'No tiene permisos para realizar esta tarea'
        return render_to_response('trazabilidad/lote-extraido.html',{'msj':msj}, context_instance=RequestContext(request))


#-------------------------------------------------------#
#-------------------   SOCIOS  -------------------------#


class CrearSocioView(CreateView):
    template_name = 'trazabilidad/ingresar-socio.html'
    model = Socio
    form_class = FormSocio

    @method_decorator(group_required('Encargados de Sala'))
    def dispatch(self, *args, **kwargs):
        return super(CrearSocioView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)        
        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if (form.is_valid()):
            return self.form_valid(form, request.user)
        else:
            return self.form_invalid(form)

    def form_valid(self, form, user):       
        print form.cleaned_data
        estado = Prueba(descripcion = 'A Prueba', periodoAPrueba = form.cleaned_data['Prueba'])
        estado.save()
        socio = Socio(nroRenapa = form.cleaned_data['nroRenapa'], codigoUnicoIdentif = form.cleaned_data['codigoUnicoIdentif'],
            tipoDocumento = form.cleaned_data['tipoDocumento'], nroDocumento = form.cleaned_data['nroDocumento'],
            nombreYApellido = form.cleaned_data['nombreYApellido'], direccion = form.cleaned_data['direccion'],
            telefono = form.cleaned_data['telefono'], email = form.cleaned_data['email'],
            ciudad = form.cleaned_data['ciudad'],
            content_type = ContentType.objects.get_for_model(estado), 
            object_id = estado.pk) 
        socio.save()
        estado.socio = socio
        estado.save()
        return HttpResponseRedirect('/socios/')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class EditarSocioView(CreateView):
    template_name = 'trazabilidad/editar-socio.html'
    model = Socio
    form_class = FormSocio

    @method_decorator(group_required('Encargados de Sala'))
    def dispatch(self, *args, **kwargs):
        return super(EditarSocioView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()        
        if (self.object.estadoActual.descripcion == 'Activo'):
            form_class = self.get_form_class()
            form = self.get_form(FormSocioEditar)
        else:                
            prueba_periodo = Prueba.objects.get(pk=self.object.object_id).periodoAPrueba
            form = FormSocio(instance = self.object, initial={'Prueba': prueba_periodo})

        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if (self.object.estadoActual.descripcion == 'Activo'):
            form_class = FormSocioEditar
        else:                
            form_class = FormSocio
        form = self.get_form(form_class)
        if (form.is_valid()):
            return self.form_valid(form, request.user)
        else:
            return self.form_invalid(form)

    def form_valid(self, form, user):       
        self.object = form.save()
        if (self.object.estadoActual.descripcion == 'A Prueba'):
            prueba_periodo = Prueba.objects.get(pk=self.object.object_id)
            prueba_periodo.periodoAPrueba = form.cleaned_data['Prueba']
            prueba_periodo.save()        
        return HttpResponseRedirect('/socios/')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

 
@group_required('Encargados de Sala')
def probarSocio(request):
    #-- funcion para cambiar el estado del socio a 'A PRUEBA'  --#
    if request.is_ajax():
        print "entre al ajax"
        id = request.GET.get('id')
        user = request.user
        socio = Socio.objects.get(pk=id)
        if socio.estadoActual.__class__.__name__ == "Prueba":
            print "antes de extraer"
            socio.probar('un anio')
            return HttpResponse("Socio a prueba")
        return HttpResponse("El socio no se pudo ingresar en periodo de prueba")
    else:
        return HttpResponse('No es una peticion Ajax')


@group_required('Encargados de Sala')
def activarSocio(request):
    #--  funcion para cambiar el estado del socio a 'ACTIVO'  --#
    if request.is_ajax():
        print "entre al ajax"
        id = request.GET.get('id')
        user = request.user
        socio = Socio.objects.get(pk=id)
        print socio.estadoActual.__class__.__name__
        if socio.estadoActual.descripcion == "A Prueba":
            print "antes de extraer"
            socio.activar()
            return HttpResponse("Socio activo")
        return HttpResponse("El socio no se pudo activar")
    else:
        return HttpResponse('No es una peticion Ajax')

@group_required('Encargados de Sala')
def desactivarSocio(request):
    #-- funcion para cambiar el estado del socio a 'INACTIVO' --#
    if request.is_ajax():
        id = request.GET.get('id')
        user = request.user
        socio = Socio.objects.get(pk=id)
        if socio.estadoActual.__class__.__name__ == "Activo":
            print "antes de extraer"
            socio.desactivar()
            return HttpResponse("Socio inactivo")
        return HttpResponse("El socio no se pudo desactivar")
    else:
        return HttpResponse('No es una peticion Ajax')

@group_required('Encargados de Sala')
def eliminarSocio(request, id):
    socio = Socio.objects.get(pk=id)
    socio.delete()
    return HttpResponseRedirect("/socios/")

@group_required('Encargados de Sala')
def socios(request):
    #--  funcion que retorna todos los socios  --#
    """ Gestion de socios """
    socios = Socio.objects.all()
    return render_to_response('trazabilidad/socios.html',{'socios':socios},context_instance=RequestContext(request))


#-------------------------------------------------------#
#------------------   TAMBORES   -----------------------#

@group_required('Encargados de Sala','Encargados de Fraccionamiento')
def tambores(request, msj = None):
    print msj
    """ Gestion de tambores """
    if request.GET.get('id') != None:
        print "entre al ajax"
        id = request.GET.get('id')
        lote = Lote.objects.get(pk=id)
        estado = Extraido.objects.get(lote=lote)
        buscar = True
        busqueda = "Lote "+str(lote.pk)
        tambores = Tambor.objects.filter(loteExtraido=estado)
        print "antes del render"
        if msj != None:
            return render_to_response('trazabilidad/tambores.html',{'msj':msj,'buscar':buscar,'busqueda':busqueda,'tambores':tambores},context_instance=RequestContext(request))
        return render_to_response('trazabilidad/tambores.html',{'buscar':buscar,'busqueda':busqueda,'tambores':tambores},context_instance=RequestContext(request))
    else:
        buscar = False
        tambores = Tambor.objects.all()
        if msj != None:
            return render_to_response('trazabilidad/tambores.html',{'msj':msj,'buscar':buscar,'tambores':tambores},context_instance=RequestContext(request))
        return render_to_response('trazabilidad/tambores.html',{'buscar':buscar,'tambores':tambores},context_instance=RequestContext(request))

@group_required('Encargados de Sala','Encargados de Fraccionamiento')
def fraccionar(request, id):
    print "fracionando"
    #-- funcion para asignar marcas a socios --#
    tambor = Tambor.objects.get(pk=id)
    socio = tambor.loteExtraido.lote.apiario.socio
    if request.POST:        
        form = FormTambor(request.POST)
        #form.clean()          
        if form.is_valid():
            print ("el form es validator")
            operario = request.user
            tipoEnvase = form.cleaned_data['tipoEnvase']
            cantidadEnvases = tambor.peso / tipoEnvase.peso
            marca = form.cleaned_data['marca']
            if socio.tieneMarca(marca):
                if marca.habilitada(tambor, socio):
                    frac = Fraccionamiento(tambor=tambor,tipoEnvase=tipoEnvase, marca=marca, operario=operario, cantidadEnvases=cantidadEnvases)
                    frac.save()
                    tambor.fraccionado = True
                    tambor.save()
                    #print "return 1"
                    return HttpResponse ("Se fracciono el tambor")
                    #return HttpResponseRedirect('/tambores/')
                else:
                    msj = 'La ultima inspeccion no aprueba el fraccionamiento de la marca %s en el apiario %s' % (marca,tambor.loteExtraido.lote.apiario)
                    #tambores = Tambor.objects.all()
                    #return render_to_response('trazabilidad/tambores.html',{'msj':msj,'tambores':tambores},context_instance=RequestContext(request))
                    #print "return 2"
                    return HttpResponse (msj)
            else:
                msj = "El socio no posee la marca %s" % (marca)
                return HttpResponse (msj)
                #print "return 3"
                #msj = 'El socio %s no posee la marca %s' % (socio, marca)
                #tambores = Tambor.objects.all()
                #return render_to_response('trazabilidad/tambores.html',{'msj':msj,'tambores':tambores},context_instance=RequestContext(request))
    else:

        form = FormTambor()    
        print"este es el form", form
        return render_to_response('trazabilidad/fraccionar.html', {'form':form, 'socio':socio, 'tambor':tambor}, context_instance=RequestContext(request))

@group_required('Encargados de Sala','Encargados de Fraccionamiento')
def tamborFraccionado(request, id):
    tambor = Tambor.objects.get(pk=id)
    if tambor.fraccionado:
        frac = Fraccionamiento.objects.get(tambor=tambor)
    return render_to_response('trazabilidad/tambor-fraccionado.html',{'frac':frac}, context_instance=RequestContext(request))


#-------------------------------------------------------#
#-------------------   MARCAS   ------------------------#


@login_required
def marcasSocio(request, id):
    #-- funcion para asignar marcas a socios --#
    socio = Socio.objects.get(pk=id)
    print "entre a la vista"
    if request.POST:
        print "entre al POST"        
        formset = MarcaFormSet(request.POST)
        for form in formset:
            print form.is_valid()
            print form             
            if form.is_valid():
                print "El form es valido", form
                if form.cleaned_data['checkSocioMarca']:
                    idMarca = form.cleaned_data['idMarca']
                    marca = Marca.objects.get(pk=idMarca)     
                    #import pdb; pdb.set_trace()             
                    if len(SocioMarca.objects.filter(socio=socio, marca=marca)) == 0:
                        print marca.idMarca  
                        socioMarca = SocioMarca(socio=socio, marca=marca, fechaValidez=timezone.now())
                        socioMarca.save()
                        print 'grabo'
                else:
                    idMarca = form.cleaned_data['idMarca']
                    marca = Marca.objects.get(pk=idMarca)     
                    #import pdb; pdb.set_trace()             
                    if len(SocioMarca.objects.filter(socio=socio, marca=marca)) != 0:
                        print marca.idMarca  
                        SocioMarca.objects.get(socio=socio, marca=marca).delete()
                        print 'borrl'   
        return HttpResponseRedirect('/socios/')
    else:
        sm = socio.marcas.all().order_by('idMarca')
        print "Marcas del Socio == ", sm
        marcas = Marca.objects.all().order_by('idMarca')
        initial_data = []
        i = sm.count()
        j = 0
        for marca in marcas:
            aux = {}
            aux['idMarca'] = marca.idMarca
            aux['descripcion'] = marca.descripcion
            aux['tipoMarca'] = marca.tipoMarca
            aux['checkSocioMarca'] = False
            if i > j:
                print "Primer if", sm[j]
                if sm[j] == marca:
                    print "Segundo if", sm[j]
                    aux['checkSocioMarca'] = True
                    j = j + 1
            initial_data.append(aux)
        print "------------------------------"
        print initial_data
        form = MarcaFormSet(initial=initial_data)
        print form
        return render_to_response('trazabilidad/marcas-socio.html',
            {'form':form, 'socio':socio},
            context_instance=RequestContext(request))


#-------------------------------------------------------#
#------------------   REMITOS   ------------------------#


@group_required('Encargados de Sala','Encargados de Entrada y Salida')
def remitos(request):
    #--  funcion que retorna todos los remitos  --#
    """ Gestion de remitos """
    remitos = Remito.objects.all()
    return render_to_response('trazabilidad/remitos.html',{'remitos':remitos},context_instance=RequestContext(request))

def verRemito(request, id):
    if request.user.groups.filter(name='Encargados de Sala').exists() or request.user.groups.filter(name='Encargados de Entrada y Salida').exists():
        remito = Remito.objects.get(pk=id)
        remito_detalle = RemitoDetalle.objects.filter(remito=remito)
        print "==========000000000==========="
        return render_to_response('trazabilidad/ver-remito.html',{'remito':remito, 'remito_detalle':remito_detalle}, context_instance=RequestContext(request))
    else:
        #return HttpResponseRedirect("/lotes/")
        msj = 'No tiene permisos para realizar esta tarea'
        return render_to_response('trazabilidad/ver-remito.html',{'msj':msj}, context_instance=RequestContext(request))

'''
@login_required
def ingresarRemito(request):
    ##-- funcion para dar de alta un remito  --#
    user = request.user
    name = 'ingresar Remito'
    if request.POST:
        try:
            form = FormRemito(request.POST)
        except ValueError:
            form = FormRemito(request.POST)
        if form.is_valid():
            form.save()
            url = '/remitos/'
            return HttpResponseRedirect(url)  
    else:
        form = formLote(request.POST)
    return render_to_response('trazabilidad/ingresar-remito.html',{'form':form, 'name':name}, context_instance=RequestContext(request))

'''

class CrearRemitoView(CreateView):
    template_name = 'trazabilidad/ingresar-remito.html'
    model = Remito
    form_class = FormRemito
    #success_url = 'success/'

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        remitoDetalle_form = RemitoDetalleFormSet()
        return self.render_to_response(
            self.get_context_data(form=form,
                                  remitoDetalle_form=remitoDetalle_form))
        #return render_to_response('trazabilidad/ingresar-remito.html',{'form':form, 'name':name}, context_instance=RequestContext(request))


    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        remitoDetalle_form = RemitoDetalleFormSet(self.request.POST)
        if (form.is_valid() and remitoDetalle_form.is_valid()):
            return self.form_valid(form, remitoDetalle_form, request.user)
        else:
            return self.form_invalid(form, remitoDetalle_form)

    def form_valid(self, form, remitoDetalle_form, user):
        peso = 0
        if form.is_valid():
            remito = Remito(operario=user, socio = form.cleaned_data['socio'], observacion=form.cleaned_data['observacion'])
            remito.save()
            for f in remitoDetalle_form:
                print "remito detalle", f
                if f.is_valid():
                    try:
                        if f.cleaned_data['fraccionamiento'] != None:
                            print 'es un fraccionamiento ', f.cleaned_data['fraccionamiento']
                            remitoDetalle = RemitoDetalle(remito = remito, fraccionamiento = f.cleaned_data['fraccionamiento'])
                        if f.cleaned_data['tambor'] != None:
                            print 'es un tambor ', type(f.cleaned_data['tambor'])
                            remitoDetalle = RemitoDetalle(remito = remito, tambor = f.cleaned_data['tambor']) 
                        remitoDetalle.save()
                        
                        #else:
                        #    remitoDetalle = RemitoDetalle(remito = remito, tambor = f.cleaned_data['tambor'], fraccionamiento = None)
                        #remitoDetalle.save()
                    except KeyError:
                        remito.remove()                    
                        pass
                else:
                    remito.remove()
            return HttpResponseRedirect('/remitos/')

    def form_invalid(self, form, remitoDetalle_form):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  remitoDetalle_form = remitoDetalle_form))

#@login_required
class EditarRemitoView(UpdateView):
    template_name = 'trazabilidad/editar-remito.html'
    model = Remito
    form_class = FormRemito
    success_url = '/remitos/'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)    
        print '=============='
        print form_class
        print form
        print '<<<<<<<<<<<<<<<'
        RemitoDetalleFormSet = formset_factory(Remito, RemitoDetalle, extra=1, can_delete=True, fields=("","lote","cantidadAlzas","peso"))
        remitoDetalle_form = RemitoDetalleFormSet()
        return self.render_to_response(            
            self.get_context_data(form=form,
                                  remitoDetalle_form=remitoDetalle_form))
        '''
        tipoDetalle = forms.ChoiceField(choices = CHOICES, required=True)
        tambor = forms.ModelChoiceField(queryset=Tambor.objects.all(), required = False)
        fraccionamiento = forms.ModelChoiceField(queryset=Fraccionamiento.objects.all(), required = False)
               
        
            prueba_periodo = Prueba.objects.get(pk=self.object.object_id).periodoAPrueba
            form = FormSocio(instance = self.object, initial={'Prueba': prueba_periodo})

        return self.render_to_response(self.get_context_data(form=form))

        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if GrupoAlza.objects.filter(lote=self.object).count() == 0:
            extra = 1
        else:
            extra = 0
        GrupoAlzaFormSet = inlineformset_factory(Lote, GrupoAlza, extra=extra, max_num=3, can_delete=True, fields=("idGrupoAlza","tipoAlza","lote","cantidadAlzas","peso"))
        grupoAlza_form = GrupoAlzaFormSet(instance = self.object)
        return self.render_to_response(
            self.get_context_data(form=form,
                                  grupoAlza_form=grupoAlza_form))
        '''




    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)        
        remitoDetalle_form = RemitoDetalleFormSet(request.POST, request.FILES, instance=self.object)
        if (form.is_valid() and remitoDetalle_form.is_valid()):
            return self.form_valid(form, remitoDetalle_form, request.user)
        else:
            return self.form_invalid(form, remitoDetalle_form)

    def form_valid(self, form, remitoDetalle_form, user):   
        self.object = form.save()
        remitoDetalle_form.instance = self.object
        remitoDetalle_form.save()
        return HttpResponseRedirect('/remitos/')

    def form_invalid(self, form, remitoDetalle_form):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  remitoDetalle_form=remitoDetalle_form))


@login_required
def eliminarRemito(request, id):
    remito = Remito.objects.get(pk=id)
    RemitoDetalle.objects.filter(remito = remito).delete()
    remito.delete()
    return HttpResponseRedirect("/remitos/")


#-------------------------------------------------------#
#-----------------   REPORTES   ------------------------#


from wkhtmltopdf.views import PDFTemplateView

from django.shortcuts import get_object_or_404

class PDFLoteSocioView(PDFTemplateView):
    template_name = 'trazabilidad/pdfs/lote-socio.html'
    #header_template = 'trazabilidad/pdfs/cabecera.html'
    footer_template = 'trazabilidad/pdfs/pie.html'
    filename = 'lote-socio.pdf'
    #context_object_name = "persona"
    show_content_in_browser = True
    cmd_options = {
        'footer-line': True,
    }

    def __init__(self):
        pass
  
    def get_context_data(self, **kwargs):
        socio = get_object_or_404(Socio, codigoUnicoIdentif=self.kwargs['id_socio'])
        lt = Lote.objects.all()
        lotes = []
        for l in lt:
            if l.apiario.socio == socio:
                lotes.append(l)
        #for domicilio in domicilios:
        #    domicilio.tipo = coremodels.DomicilioDePersona.objects.get(domicilio=domicilio.pk).tipo
        if (lotes == []):
            lotes = None
        return {'socio': socio, 'lotes': lotes}

class PDFTamborLoteView(PDFTemplateView):
    template_name = 'trazabilidad/pdfs/tambor-lote.html'
    #header_template = 'trazabilidad/pdfs/cabecera.html'
    footer_template = 'trazabilidad/pdfs/pie.html'
    filename = 'tambor-lote.pdf'
    #context_object_name = "persona"
    show_content_in_browser = True
    cmd_options = {
        'footer-line': True,
    }

    def __init__(self):
        pass
  
    def get_context_data(self, **kwargs):
        lote = get_object_or_404(Lote, idLote=self.kwargs['id_lote'])
        socio = lote.apiario.socio
        estado = Extraido.objects.get(lote=lote)
        tambores = Tambor.objects.filter(loteExtraido=estado)
        if (tambores == []):
            tambores = None
        return {'lote':lote, 'socio': socio, 'tambores': tambores}

class PDFMarcasFraccionamientosView(PDFTemplateView):
    template_name = 'trazabilidad/pdfs/marcas-fraccionamientos.html'
    #header_template = 'trazabilidad/pdfs/cabecera.html'
    footer_template = 'trazabilidad/pdfs/pie.html'
    filename = 'marcas-fraccionamientos.pdf'
    #context_object_name = "persona"
    show_content_in_browser = True
    cmd_options = {
        'footer-line': True,
    }

    def __init__(self):
        pass
  
    def get_context_data(self, **kwargs):

        cant = []
        marcas = []
        marcas_obj = Marca.objects.all().order_by("idMarca")
        for m in marcas_obj:
            cant.append(Fraccionamiento.objects.filter(marca=m).count())
            marcas.append(m.descripcion)

        fig = Figure()
        fig = Figure(facecolor='white', edgecolor='white')
        ax = fig.add_subplot(1,1,1)

        x = matplotlib.numpy.arange(0, len(marcas))

        ind = matplotlib.numpy.arange(len(cant))

        width = 0.4
        colors = ["red","blue","green","orange","yellow"]
        ax.bar(ind, cant, width, color=colors)

        ax.set_xticks(ind + width / 2.0)
        ax.set_xticklabels(marcas)
        ax.set_xlabel("Marcas Registradas")
        ax.set_ylabel("Cantidad de Fraccionamientos")
        ax.set_title("Cantidad de Fraccionamientos por Marcas")

        padding = 0.2
        ax.set_xlim([x.min() - padding, x.max() + width + padding])

        canvas =  FigureCanvas(fig)
        response = HttpResponse(content_type='image/png')
        canvas.print_png(response)
        filename = "marcas-fraccionamientos.png"
        path = settings.MEDIA_ROOT+filename
        fig.savefig(path)
        fecha = timezone.now()

        i = 0
        for marca in marcas_obj:
            marca.cant = cant[i]
            i = i + 1

        return {'marcas':marcas_obj,'cant':cant,'fecha':fecha,'filename':filename}


def simple2():
    cant = []
    marcas = []
    marcas_obj = Marca.objects.all().order_by("idMarca")
    for m in marcas_obj:
        cant.append(Fraccionamiento.objects.filter(marca=m).count())
        marcas.append(m.descripcion)

    fig = Figure()
    fig = Figure(facecolor='white', edgecolor='white')
    ax = fig.add_subplot(1,1,1)

    x = matplotlib.numpy.arange(0, len(marcas))

    ind = matplotlib.numpy.arange(len(cant))

    #height = 0.8
    width = 0.5
    colors = ["red","blue","green","orange","yellow"]
    ax.bar(ind, cant, width, color=colors)

    ax.set_xticks(ind + width / 2.0)
    ax.set_xticklabels(marcas)
    ax.set_xlabel("Marcas Registradas")
    ax.set_ylabel("Cantidad de Fraccionamientos")
    ax.set_title("Cantidad de Fraccionamientos por Marcas")

    padding = 0.2
    ax.set_xlim([x.min() - padding, x.max() + width + padding])

    canvas =  FigureCanvas(fig)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    filename = "marcas-fraccionamientos.png"
    fig.savefig(filename)
    #return HttpResponse("funciono")
    return