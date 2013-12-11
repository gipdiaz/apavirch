from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.conf import settings

## ------------------------------------------- ##
class TipoEnvase (models.Model):
    idTipoEnvase = models.AutoField (primary_key = True)
    fabricante = models.CharField( max_length = 30, blank = False)
    peso = models.IntegerField (default = 1, blank = False)
    descripcion = models.CharField( max_length = 30, blank = False)
    
    class Meta:
        unique_together = ("fabricante","peso")
        verbose_name_plural = "Tipos de Envases"

    def __unicode__(self):
        return u'%s %s' % (self.peso, self.fabricante)

## ------------------------------------------- ##
class TipoDocumento (models.Model):
    idTipoDocumento = models.AutoField(primary_key = True)
    descripcion = models.CharField(max_length = 30, blank = False)
    
    class Meta:
        verbose_name_plural = "Tipos de Documentos"
    
    def __unicode__(self):
        return self.descripcion

## ------------------------------------------- ##
class TipoAlza (models.Model):
    idTipoAlza = models.AutoField (primary_key = True)
    descripcion = models.CharField("tipo de alza",max_length = 30, blank = False)
    
    class Meta:
        verbose_name_plural = "Tipos de Alzas"
    
    def __unicode__(self):
        return self.descripcion

## ------------------------------------------- ##
class TipoMarca (models.Model):
    idTipoMarca = models.AutoField (primary_key = True)
    descripcion = models.CharField(max_length = 100, blank = False)
    
    class Meta:
        verbose_name_plural = "Tipos de Marcas"
    
    def __unicode__(self):
        return self.descripcion

## ------------------------------------------- ##
class Ciudad(models.Model):
    codigoPostal = models.IntegerField(default = 0, primary_key = True)
    nombre = models.CharField(max_length = 30, blank = False)
    
    class Meta:
        verbose_name_plural = "Ciudades"
    
    def __unicode__(self):
        return self.nombre

## ------------------------------------------- ##
class Marca (models.Model):
    idMarca = models.AutoField(primary_key = True)
    descripcion = models.CharField (max_length =20)
    tipoMarca = models.ForeignKey(TipoMarca, null=False)
    
    class Meta:
        unique_together = ("descripcion","tipoMarca")
        verbose_name_plural = "Marcas"

    def habilitada (self, tambor):
        inspecciones = Inspeccion.objects.filter(tipoMarca=self.tipoMarca, apiario=tambor.loteExtraido.lote.apiario).order_by('-fechaInspeccion')
        if len(inspecciones) != 0:
            return inspecciones[0].cumpleProtocolo
        return False

    def __unicode__(self):
        return u'%s' % (self.descripcion)

## ------------------------------------------- ##
class Persona (models.Model):
    codigoUnicoIdentif = models.BigIntegerField(primary_key = True, blank = False) #CUIT / CUIL, verificar sea correcto
    tipoDocumento = models.ForeignKey(TipoDocumento, null = False)
    nroDocumento = models.IntegerField(blank = False)
    nombreYApellido = models.CharField(max_length=200, blank = False)       
    direccion = models.CharField(max_length = 30, blank = False)
    telefono = models.IntegerField(default = 0)
    email = models.EmailField(max_length = 75)
    fechaAlta = models.DateTimeField(default = timezone.now())
    
    class Meta:
        abstract = True
        verbose_name_plural = "Personas"
    
    def __unicode__(self):
        return self.nombreYApellido

## ------------------------------------------- ##
# class Operario(models.Model):
#     user = models.OneToOneField(User)
#     tipoOperario = models.ForeignKey(TipoOperario, null = False)
    
#     class Meta:
#         verbose_name_plural = "Operarios"
    
#     def __unicode__(self):
#         return self.nombre

## ------------------------------------------- ##

class Socio(Persona):
    nroRenapa = models.CharField(unique=True, max_length=200, blank = False)
    marcas = models.ManyToManyField(Marca, through="SocioMarca")

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    estadoActual = generic.GenericForeignKey('content_type', 'object_id')

    def activar(self):
        #import pdb; pdb.set_trace()
        estado = Activo(descripcion="Activo")
        estado.save()
        self.content_type = ContentType.objects.get_for_model(estado)
        self.object_id = estado.pk
        self.save()
        estado.socio = self
        estado.save()

    def desactivar(self):
        #import pdb; pdb.set_trace()
        estado = Inactivo(descripcion="Inactivo")
        estado.save()
        self.content_type = ContentType.objects.get_for_model(estado)
        self.object_id = estado.pk
        self.save()
        estado.socio = self
        estado.save()

    def probar(self, periodo):
        #import pdb; pdb.set_trace()
        estado = Prueba(descripcion="A Prueba", periodoAPrueba=periodo)
        estado.save()
        self.content_type = ContentType.objects.get_for_model(estado)
        self.object_id = estado.pk
        self.save()
        estado.socio = self
        estado.save()

    def getMarcasRelacionadas(self):
        return self.marcas.all()

    def getMarcasDisponibles(self):               
        return Marca.objects.all().exclude(idMarca__in = self.marcas.all().values_list('idMarca'))

    def asociarMarcas(self, marca):
        self.marcas.add(marca)
        self.save()



    class Meta:
        verbose_name_plural = "Socios"
    
    def __unicode__(self):
        return u'%s' % (self.nombreYApellido)

## ------------------------------------------- ##        
class SocioEstado(models.Model):
    idSocioEstado = models.AutoField(primary_key = True)
    descripcion = models.CharField(max_length=200, blank = True)
    fecha = models.DateTimeField(default = timezone.now())
    socio = models.ForeignKey(Socio, null=True)

    class Meta:
        abstract = True
        verbose_name_plural = "Estados de los Socios"

## ------------------------------------------- ##
class Prueba(SocioEstado):
    #idPrueba = models.AutoField(primary_key = True)
    periodoAPrueba = models.CharField(max_length=100, blank = False)

    class Meta:
        verbose_name_plural = "Estado Prueba de los Socios"

    def __unicode__(self):
        return u'%s' % (self.__class__.__name__)


## ------------------------------------------- ##
class Activo(SocioEstado):
    #idActivo = models.AutoField(primary_key = True)

    class Meta:
        verbose_name_plural = "Estado Activo de los Socios"


    def __unicode__(self):
        return u'%s' % (self.__class__.__name__)

## ------------------------------------------- ##
class Inactivo(SocioEstado):
    #idInactivo = models.AutoField(primary_key = True)

    class Meta:
        verbose_name_plural = "Estado Inactivo de los Socios"
        
    def __unicode__(self):
        return u'%s' % (self.__class__.__name__)

## ------------------------------------------- ##
class SocioMarca (models.Model):
    idSocioMarca = models.AutoField (primary_key = True)    
    socio = models.ForeignKey (Socio, null=False)           
    marca = models.ForeignKey (Marca, null=False)
    fechaAlta = models.DateTimeField(default = timezone.now())
    fechaValidez = models.DateTimeField(blank=True)

    class Meta:
        unique_together = ("socio", "marca")
        verbose_name_plural = "Socios Marcas"
    
    def __unicode__(self):

        return u'%s' % (self.socio)


## ------------------------------------------- ##
class Apiario(models.Model):         
    nroChacra = models.CharField(primary_key=True,max_length = 30, blank=False)
    socio = models.ForeignKey(Socio, null = False)
    cantidadColmenas = models.IntegerField(default = 0)
    fechaAlta = models.DateTimeField(default = timezone.now())
    operario = models.ForeignKey(User, null=False)
    
    class Meta:
        verbose_name_plural = "Apiarios"
    
    def __unicode__(self):
        return u'Chacra %s' % (self.nroChacra)

## ------------------------------------------- ##
class Inspeccion(models.Model):             
    idInspeccion = models.AutoField(primary_key = True)     
    apiario = models.ForeignKey(Apiario, null=False)
    tipoMarca = models.ForeignKey(TipoMarca, null=False)
    fechaInspeccion = models.DateTimeField('Fecha de Inspeccion', blank = False)
    cumpleProtocolo = models.BooleanField (default = False)
    observacion = models.CharField(max_length=300, blank = False)
    operario = models.ForeignKey(User, null=False)
    
    class Meta:
        verbose_name_plural = "Inspecciones"
    
    def __unicode__(self):
        return self.observacion

## ------------------------------------------- ##
class Lote(models.Model):             
    idLote = models.AutoField(primary_key= True)
    apiario = models.ForeignKey(Apiario)
    peso = models.DecimalField(max_digits = 10, decimal_places = 2, blank = True, default = 0)
    observacion = models.CharField(max_length=300)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    estadoActual = generic.GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name_plural = "Lotes"

    def extraer(self, user, peso, observacion=""):
        estado = Extraido(observacion=observacion, peso=peso, operario=user)
        estado.save()

        while peso > settings.CAPACIDAD_TAMBOR:
            tambor = Tambor (loteExtraido = estado, peso = settings.CAPACIDAD_TAMBOR, operario = user)
            tambor.save()
            peso = peso - settings.CAPACIDAD_TAMBOR
        if peso!= 0:
            tambor = Tambor (loteExtraido = estado, peso = peso, operario = user)
            tambor.save()

        self.content_type = ContentType.objects.get_for_model(estado)
        self.object_id = estado.pk
        self.save()
        estado.lote = self
        estado.save()

    def devolver(self, user):
        #import pdb; pdb.set_trace()
        estado = Devuelto(observacion='Devuelto', peso=20, operario=user)
        estado.save()
        self.content_type = ContentType.objects.get_for_model(estado)
        self.object_id = estado.pk
        self.save()
        estado.lote = self
        estado.save()

    def extraerDeNuevo(self, user, peso, observacion=""):
        #estado = Extraido(observacion=observacion, peso=peso, operario=user)
        #estado.save()

        #import pdb; pdb.set_trace()

        estado = Extraido.objects.get(pk=self.object_id)

        Tambor.objects.filter(loteExtraido=estado).delete()

        while peso > settings.CAPACIDAD_TAMBOR:
            tambor = Tambor (loteExtraido = estado, peso = settings.CAPACIDAD_TAMBOR, operario = user)
            tambor.save()
            peso = peso - settings.CAPACIDAD_TAMBOR
        if peso!= 0:
            tambor = Tambor (loteExtraido = estado, peso = peso, operario = user)
            tambor.save()

        estado.peso = peso
        estado.save()

    def fueExtraido(self):
        pass

    def __unicode__(self):
        return u'Lote numero %s - Estado %s' % (self.idLote, self.content_type)

## ------------------------------------------- ##        
class LoteEstado(models.Model):
    idLoteEstado = models.AutoField(primary_key = True, blank = False)
    observacion = models.CharField(max_length=200, blank = True)
    peso = models.DecimalField(max_digits = 10, decimal_places = 2, null = False)
    fecha = models.DateTimeField(default = timezone.now())
    operario = models.ForeignKey(User, null=False)
    lote = models.ForeignKey(Lote, null=True)

    class Meta:
        abstract = True
        verbose_name_plural = "Estados de los Lotes"

## ------------------------------------------- ##
class Ingresado(LoteEstado):

    class Meta:
        verbose_name_plural = "Estado Ingresado de los Lotes"

    def __unicode__(self):
        return u'%s' % (self.__class__.__name__)
## ------------------------------------------- ##
class Devuelto(LoteEstado):

    class Meta:
        verbose_name_plural = "Estado Devuelto de los Lotes"

    def __unicode__(self):
        return u'%s' % (self.__class__.__name__)

## ------------------------------------------- ##
class Extraido(LoteEstado):

    class Meta:
        verbose_name_plural = "Estado Extraido de los Lotes"

    def __unicode__(self):
        return u'%s' % (self.__class__.__name__)

## ------------------------------------------- ##
class Tambor (models.Model):
    idTambor = models.AutoField (primary_key = True)
    loteExtraido = models.ForeignKey (Extraido, null = False)
    peso = models.DecimalField (max_digits = 6, decimal_places = 2, blank = False)
    fraccionado = models.BooleanField(default = False)
    operario = models.ForeignKey(User, null=False)
    
    class Meta:
        verbose_name_plural = "Tambores"
    
    def __unicode__(self):
        return u'Tambor %s' % (self.idTambor)

## ------------------------------------------- ##
class GrupoAlza (models.Model):             
    idGrupoAlza = models.AutoField (primary_key = True)
    tipoAlza = models.ForeignKey(TipoAlza, null = False)
    lote = models.ForeignKey(Lote, null = False, related_name='alza')
    cantidadAlzas = models.IntegerField(blank = False)     
    peso = models.DecimalField(max_digits = 6, decimal_places = 2, blank = False)

    class Meta:
        unique_together = ("lote", "tipoAlza")
        verbose_name_plural = "Grupos de Alzas"
    
    def __unicode__(self):
        return u'%s %s %s' % (self.idGrupoAlza, self.tipoAlza, self.lote)

## ------------------------------------------- ##    
class Fraccionamiento (models.Model):
    idFraccionamiento = models.AutoField (primary_key = True)
    tambor = models.OneToOneField (Tambor, null = False)
    tipoEnvase = models.ForeignKey(TipoEnvase, null = False)
    marca = models.ForeignKey (Marca, null = False)
    operario = models.ForeignKey(User, null = False)
    cantidadEnvases = models.IntegerField (default = 0)
    fecha = models.DateTimeField (default = timezone.now())

    class Meta:
        verbose_name_plural = "Fraccionamientos"
    
    def __unicode__(self):
        return u'%s %s %s %s' % (self.idFraccionamiento, self.tambor, self.tipoEnvase, self.marca)

## ------------------------------------------- ##
class Remito (models.Model):
    idRemito = models.AutoField (primary_key = True, )            
    operario = models.ForeignKey(User, null = False)
    socio = models.ForeignKey(Socio, null = False)
    fecha = models.DateTimeField (default = timezone.now())
    observacion = models.CharField (max_length = 100)
    
    class Meta:
        verbose_name_plural = "Remitos"
    
    def __unicode__(self):
        return u'%s %s' % (self.idRemito, self.observacion)

## ------------------------------------------- ##
class RemitoDetalle (models.Model):
    idRemitoDetalle = models.AutoField (primary_key = True)
    remito = models.ForeignKey (Remito, null = False)
    tambor = models.ForeignKey (Tambor, null=True, blank=True)
    fraccionamiento = models.ForeignKey (Fraccionamiento, null=True, blank = True)
    
    class Meta:        
        verbose_name_plural = "Detalles de Remitos"
    
    def __unicode__(self):
        return u'%s' % (self.idRemitoDetalle)
