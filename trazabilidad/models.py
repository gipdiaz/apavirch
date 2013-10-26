from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
## ------------------------------------------- ##
class Envase_tipo (models.Model):
    MATERIAL = (
        ('VIDRIO', 'VIDRIO'),
        ('PLASTICO', 'PLASTICO'),        
    )             
    idEnvaseTipo = models.AutoField (primary_key = True)
    marca = models.CharField( max_length = 30, blank = False)
    capacidad = models.IntegerField (default = 1, blank = False)
    material = models.CharField (max_length = 30, choices = MATERIAL)
    
    class Meta:
        unique_together = ("idEnvaseTipo","marca","capacidad")
        verbose_name_plural = "Tipos de Envases"

    def __unicode__(self):
        return u'%s %s %s' % (self.envase_tipo_id, self.capacidad, self.marca)
## ------------------------------------------- ##
class TipoDocumento (models.Model):
    documento_tipo_id = models.CharField (max_length = 2, primary_key = True)
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
class Ciudad(models.Model):    
    codigoPostal = models.IntegerField(default = 0, primary_key = True)
    descripcion = models.CharField(max_length = 30, blank = False)
    added_by = models.ForeignKey('auth.User')
    
    class Meta:
        verbose_name_plural = "Ciudades"
    
    def __unicode__(self):
        return self.descripcion
## ------------------------------------------- ##
class Direccion (models.Model):    
    idDireccion = models.AutoField(primary_key = True)
    calle = models.CharField(max_length = 30, blank = False)
    numero = models.IntegerField(default=0)
    ciudad = models.ForeignKey(Ciudad, null = False)
    
    class Meta:
        verbose_name_plural = "Direcciones"
    
    def __unicode__(self):
        return (self.calle, self.numero, self.ciudad)
## ------------------------------------------- ##
class Marca (models.Model):
    idMarca = models.AutoField(primary_key = True)
    nombre = models.CharField (max_length =20, primary_key = True)   
    habilitada = models.BooleanField (default = False)
    
    class Meta:
        verbose_name_plural = "Marcas"
    
    def __unicode__(self):
        return u'%s' % (self.nombre)
## ------------------------------------------- ##
class Persona (models.Model):
    codigoUnicoIdentif = models.IntegerField(primary_key = True, blank = False) #CUIT / CUIL, verificar sea correcto
    user = models.OneToOneField(User)
    tipoDocumento = models.ForeignKey(TipoDocumento, null = False)
    nroDocumento = models.IntegerField(blank = False)
    nombre = models.CharField(max_length=200, blank = False)       
    fechaAlta = models.DateTimeField('Fecha de alta', default = timezone.now())
    telefono = models.IntegerField(default = 0)
    email = models.EmailField(max_length = 75)
    marcas = models.ManyToManyField(Marca)
    
    class Meta:
        verbose_name_plural = "Personas"
    
    def __unicode__(self):
        return self.nombre    
## ------------------------------------------- ##
class Socio(models.Model):
    SOCIO_ESTADOS = (
        ('INACTIVO', 'INACTIVO'),
        ('A PRUEBA', 'A PRUEBA'),
        ('ACTIVO', 'ACTIVO'),        
    )             
    idRenapa = models.CharField(max_length=200, primary_key=True, blank = False)    
    persona = models.ForeignKey (Persona, null=False)
    estado = models.CharField(max_length=8, choices=SOCIO_ESTADOS)
    
    class Meta:
        unique_together = ("idRenapa","persona")
        verbose_name_plural = "Socios"
    
    def __unicode__(self):
        return self.persona.nombre
## ------------------------------------------- ##
class Apiario(models.Model):         
    idChacra = models.CharField(primary_key=True,max_length = 30, blank=False)
    socio = models.ForeignKey(Socio, null = False)
    nroColmena = models.IntegerField(default = 0)     
    fechaAlta = models.DateTimeField('Fecha de alta', default = timezone.now())
    
    class Meta:
        verbose_name_plural = "Apiarios"
    
    def __unicode__(self):
        return self.nro_chacra
## ------------------------------------------- ##
class Inspeccion(models.Model):             
    idInspeccion = models.AutoField(primary_key = True, unique_for_year = True)     
    apiario = models.ForeignKey(Apiario)    
    fechaInspeccion = models.DateTimeField('Fecha de Inspeccion', blank = False)
    observacion = models.CharField(max_length=300, blank = False)
    habilita = modelhabilitas.BooleanField (default = False)
    
    class Meta:
        unique_together =  ("idInspeccion", "apiario")
        verbose_name_plural = "Inspecciones"
    
    def __unicode__(self):
        return self.observacion
## ------------------------------------------- ##
class Lote(models.Model):             
    idLote = models.AutoField(primary_key= True, unique_for_year = True)     
    apiario = models.ForeignKey(Apiario)
    fechaIngreso = models.DateTimeField('Fecha de Ingreso', default = timezone.now())
    fechaEgreso = models.DateTimeField ('Fecha de Egreso', blank = True, null = True)
    peso = models.DecimalField(max_digits = 10, decimal_places = 2, blank = True, default = 0)
    observacion = models.CharField(max_length=300)
    devuelto = models.BooleanField (default = False)

    class Meta:
        unique_together = ("nro_lote","apiario")
        verbose_name_plural = "Lotes"
    
    def update_total_peso(self, peso_total):
        self.peso = peso_total
        self.save()

    def __unicode__(self):
        return str(self.nro_lote)
## ------------------------------------------- ##
class GrupoAlza (models.Model):             
    ALZA_ESTADOS = (
        ('LLENA','LLENA'),
        ('VACIA','VACIA')
    )             
    idAlza = models.AutoField (primary_key = True)
    tipoAlza = models.ForeignKey(TipoAlza, null = False)
    lote = models.ForeignKey(Lote, null = False, related_name='alza')
    cantidadAlzas = models.IntegerField(blank = False)     
    peso = models.DecimalField(max_digits = 6, decimal_places = 2, blank = False)    

    class Meta:
        unique_together = ("lote", "alza_tipo")
        verbose_name_plural = "Grupos de Alzas"
        verbose_name = "Grupo de Alza"
    
    def __unicode__(self):
        return str(self.nro_alza)
## ------------------------------------------- ##
class Extraccion (models.Model):
    idExtraccion = models.AutoField (primary_key = True, unique_for_year = True)
    lote = models.OneToOneField (Lote)
    operario = models.ForeignKey (Persona, null = False)
    peso = models.DecimalField(max_digits = 6, decimal_places = 2, blank = False)
    fecha = models.DateTimeField ('Fecha de Extraccion', default = timezone.now())
    observacion = models.CharField (max_length = 300, blank = True)
    
    class Meta:
        verbose_name_plural = "Extracciones"
    
    def __unicode__(self):
        return u'%s' % (self.nro_extraccion)

## ------------------------------------------- ##
class Tambor (models.Model):
    idTambor = models.AutoField (primary_key = True)
    extraccion = models.ForeignKey (Extraccion, null = False)
    peso = models.DecimalField (max_digits = 6, decimal_places = 2, blank = False)
    
    class Meta:
        unique_together =  ("idTambor","extraccion")
        verbose_name_plural = "Tambores"
    
    def __unicode__(self):
        return u'%s' % (self.nro_tambor)
## ------------------------------------------- ##
# class Marca_Persona (models.Model):
#     codigo = models.AutoField (primary_key = True)    
#     socio = models.ForeignKey (Socio)           
#     marca = models.ForeignKey (Marca)  

#     class Meta:
#         unique_together = ("socio", "marca")
#         verbose_name_plural = "Marcas Personas"
    
#     def __unicode__(self):
#         pass
## ------------------------------------------- ##    
class Fraccionamiento (models.Model):
    idFraccionamiento = models.AutoField (primary_key = True)
    tambor = models.OneToOneField (Tambor, null = False)
    tipoEnvase = models.ForeignKey(tipoEnvase, null = False)
    marca = models.ForeignKey (Marca, null = False)
    operador = models.ForeignKey(Persona, null = False)
    cantidadEnvases = models.IntegerField (default = 0)
    fecha = models.DateTimeField ('Fecha de Fraccionamiento', default = timezone.now())

    class Meta:
        unique_together =  ("idFraccionamiento","tambor")
        verbose_name_plural = "Fraccionamientos"
    
    def __unicode__(self):
        return u'%s' % (self.nro_fraccionamiento)

    def save(self, *args, **kwargs):
        
        # Sino esta creado el fraccionamiento         
        if not self.pk:
            self.cantidad_envases = (self.tambor.peso / self.tipoEnvase.capacidad)
        
        # Se crea el fraccionamiento
        super(Fraccionamiento, self).save(*args, **kwargs)
        
        # Se crean los envases
        if self.pk:
            for i in range(self.cantidadEnvases):
                envase = Envase (fraccionamiento = self, tipoEnvase = self.tipoEnvase, operador = self.operador)
                envase.save()

## ------------------------------------------- ##
class Remito (models.Model):
    idRemito = models.AutoField (primary_key = True, unique_for_year = True)            
    operador = models.ForeignKey(Persona, null = False)
    fecha = models.DateTimeField ('Fecha de Retiro', default = timezone.now())
    observacion = models.CharField (max_length = 100)
    
    class Meta:
        verbose_name_plural = "Remitos"
    
    def __unicode__(self):
        return self.observacion
## ------------------------------------------- ##
class RemitoDetalle (models.Model):
    idRemitoDetalle = models.AutoField (primary_key = True)
    remito = models.ForeignKey (Remito, null = False)
    tambor = models.ForeignKey (Tambor)
    
    class Meta:
        unique_together =  ("nro_remito_detalle","renglon","nro_remito")
        verbose_name_plural = "Detalles de Remitos"
    
    def __unicode__(self):
        pass

from django.db.models.signals import pre_save

def lote_handler(sender, instance,raw , **kwargs):
    print sender
    print instance.peso

pre_save.connect(lote_handler, sender=Lote)
