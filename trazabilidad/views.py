from django.http import HttpResponse, request, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.generic import DetailView, ListView, CreateView, UpdateView
from django.contrib import auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django import forms 
from django.forms.models import inlineformset_factory, formset_factory
from django.template import RequestContext, Template, Context
from django.contrib.contenttypes.models import ContentType
from .models import *
from .forms import FormLote, GrupoAlzaFormSet, FormSocioEditar, FormSocio, FormMarcaSocio, MarcaFormSet, FormTambor, FormRemito, RemitoDetalleFormSet, RemitoDetalleForm

from django.forms import Form

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

#-------------------------------------------------------#
#-------------------   LOTES   -------------------------#

class CrearLoteView(CreateView):
    template_name = 'trazabilidad/ingresar-lote.html'
    model = Lote
    form_class = FormLote

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
        #grupoAlza_form.clean()
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
        self.object = form.save()
        grupoAlza_form.instance = self.object
        grupoAlza_form.save()
        return HttpResponseRedirect('/lotes/')

    def form_invalid(self, form, grupoAlza_form):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  grupoAlza_form=grupoAlza_form))

@group_required('Encargados de Sala','Encargados de Entrada y Salida')
def lotes(request):
    lotes = Lote.objects.all()
    return render_to_response('trazabilidad/lotes.html',{'lotes':lotes},context_instance=RequestContext(request))

@login_required
def eliminarLote(request, id):
    lote = Lote.objects.get(pk=id)
    GrupoAlza.objects.filter(lote=lote).delete()
    lote.delete()
    return HttpResponseRedirect("/lotes/")

@login_required
def extraerLote(request):
    if request.is_ajax():
        id = request.GET.get('id')
        peso = float(request.GET.get('peso'))
        observacion = request.GET.get('observacion')
        user = request.user
        lote = Lote.objects.get(pk=id)
        if lote.estadoActual.__class__.__name__ == "Ingresado":
            lote.extraer(user, peso, observacion)
            return HttpResponse("Lote Extraido")
        return HttpResponse("El lote no se puede extraer")
    else:
        return HttpResponse('No es una peticion Ajax')

@login_required
def dextraerLote(request):
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

@login_required
def devolverLote(request):
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

def loteExtraido(request, id):
    lote = Lote.objects.get(pk=id)
    estado = Extraido.objects.get(lote=lote)
    tambores = Tambor.objects.filter(loteExtraido=estado)
    return render_to_response('trazabilidad/lote-extraido.html',{'lote':lote, 'tambores':tambores}, context_instance=RequestContext(request))


#-------------------------------------------------------#
#-------------------   SOCIOS  -------------------------#


class CrearSocioView(CreateView):
    #--  clase para dar altas de socios  --#
    template_name = 'trazabilidad/ingresar-socio.html'
    model = Socio
    form_class = FormSocio

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
            content_type = ContentType.objects.get_for_model(estado), 
            object_id = estado.pk) 
        socio.save()
        estado.socio = socio
        estado.save()
        return HttpResponseRedirect('/socios/')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class EditarSocioView(CreateView):
    #-- clase para editar el socio  --#
    template_name = 'trazabilidad/editar-socio.html'
    model = Socio
    form_class = FormSocio

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

 
@login_required
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


@login_required
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

@login_required
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
def socios(request):
    #--  funcion que retorna todos los socios  --#
    """ Gestion de socios """
    socios = Socio.objects.all()
    return render_to_response('trazabilidad/socios.html',{'socios':socios},context_instance=RequestContext(request))


#-------------------------------------------------------#
#------------------   TAMBORES   -----------------------#

@group_required('Encargados de Sala')
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

@login_required
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
                    print "return 1"
                    return HttpResponse ("Funciono")
                    #return HttpResponseRedirect('/tambores/')
                else:
                    #msj = 'La ultima inspeccion no aprueba el fraccionamiento de la marca %s en el apiario %s' % (marca,tambor.loteExtraido.lote.apiario)
                    #tambores = Tambor.objects.all()
                    #return render_to_response('trazabilidad/tambores.html',{'msj':msj,'tambores':tambores},context_instance=RequestContext(request))
                    print "return 2"
                    return HttpResponse ("No Funciono")
            else:
                return HttpResponse ("Funciono 2")
                print "return 3"
                #msj = 'El socio %s no posee la marca %s' % (socio, marca)
                #tambores = Tambor.objects.all()
                #return render_to_response('trazabilidad/tambores.html',{'msj':msj,'tambores':tambores},context_instance=RequestContext(request))
    else:

        form = FormTambor()    
        print"este es el form", form
        return render_to_response('trazabilidad/fraccionar.html', {'form':form, 'socio':socio, 'tambor':tambor}, context_instance=RequestContext(request))

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
    if request.POST:        
        formset = MarcaFormSet(request.POST)
        for form in formset:             
            if form.is_valid():
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
        # condicion = 'SELECT CASE WHEN idMarca=marca_id THEN "True" ELSE "False" END FROM trazabilidad_sociomarca where idMarca=marca_id and socio_id = '+str(socio.codigoUnicoIdentif)
        # marcasSocio = Marca.objects.extra(select={'checkSocioMarca': condicion})
        # initial_data = []        
        # #import pdb; pdb.set_trace()
        # for marca in marcasSocio:            
        #     aux = {}
        #     for f in marca._meta.fields:
        #         if f.name in ['tipoMarca']:
        #             aux['tipoMarca'] = getattr(marca, f.name).descripcion
        #         else:
        #             aux[f.name] = getattr(marca, f.name)
        #     aux['checkSocioMarca'] = marca.checkSocioMarca
        #     initial_data.append(aux)

        # form = MarcaFormSet(initial=initial_data)

        sm = socio.marcas.all()
        marcas = Marca.objects.all()
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
                print sm[j]
                if sm[j] == marca:
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

@group_required('Encargados de Sala')
def remitos(request):
    #--  funcion que retorna todos los remitos  --#
    """ Gestion de remitos """
    remitos = Remito.objects.all()
    return render_to_response('trazabilidad/remitos.html',{'remitos':remitos},context_instance=RequestContext(request))

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