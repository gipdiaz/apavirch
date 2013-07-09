from django.db import models
from django.utils import timezone

#---------------------------------
class Envase_tipo (models.Model):
    MATERIAL = (
        ('VIDRIO', 'VIDRIO'),
        ('PLASTICO', 'PLASTICO'),        
    )             
    envase_tipo_id = models.AutoField (primary_key = True)
    marca = models.CharField( max_length = 30, blank = False)
    capacidad = models.IntegerField (default = 1000, blank = False)
    material = models.CharField (max_length = 30, choices = MATERIAL)
    
    class Meta:
        unique_together = ("envase_tipo_id","marca","capacidad")
#---------------------------------
class Documento_tipo (models.Model):
    documento_tipo_id = models.CharField (max_length = 2, primary_key = True)
    descripcion = models.CharField(max_length = 30, blank = False)
#---------------------------------
class Alza_tipo (models.Model):
    alza_tipo_id = models.AutoField (primary_key = True)
    descripcion = models.CharField(max_length = 30, blank = False)    
#---------------------------------
class Ciudad(models.Model):    
    codigo_postal = models.IntegerField(default = 0, primary_key = True)
    descripcion = models.CharField(max_length = 30, blank = False)
#---------------------------------
class Direccion (models.Model):    
    direccion_id = models.AutoField(primary_key = True)
    calle = models.CharField(max_length = 30, blank = False)
    numero = models.IntegerField(default=0)
    ciudad = models.ForeignKey(Ciudad, null = False)
#---------------------------------    
class Persona (models.Model):
    cod_unico_identif = models.IntegerField(primary_key = True, blank = False) #CUIT / CUIL, verificar sea correcto
    documento_tipo = models.ForeignKey(Documento_tipo, null = False)
    nro_documento = models.IntegerField(blank = False)
    nombre = models.CharField(max_length=200, blank = False)       
    fecha_alta = models.DateTimeField('Fecha de alta', default = timezone.now())
    telefono = models.IntegerField(default = 0)
    email = models.EmailField(max_length = 75)    
#---------------------------------    
class Socio(models.Model):
    SOCIO_ESTADOS = (
        ('INACTIVO', 'INACTIVO'),
        ('A PRUEBA', 'A PRUEBA'),
        ('ACTIVO', 'ACTIVO'),        
    )             
    nro_renapa = models.CharField(max_length=200, primary_key=True, blank = False)    
    persona = models.ForeignKey (Persona, null=False)
    estado = models.CharField(max_length=8, choices=SOCIO_ESTADOS)               
    
    class Meta:
        unique_together = ("nro_renapa","persona")
        
#---------------------------------
class Apiario(models.Model):         
    nro_chacra = models.CharField(primary_key=True,max_length = 30, blank=False)
    socio = models.ForeignKey(Socio, null = False)
    nro_colmena = models.IntegerField(default = 0)     
    fecha_alta = models.DateTimeField('Fecha de alta', default = timezone.now())
    # ubicacion, en caso de llegar con el tiempo, dejar un formato facil de guardar y reutilizable
    #fijate gato que dato se necesita aca para geodjango
    latitud = models.DecimalField (max_digits = 3, decimal_places = 3)    # Ver si podemos encajar esto con el plugin de google
    longitud = models.DecimalField (max_digits = 3, decimal_places = 3)   # Ver si podemos encajar esto con el plugin de google
          
#---------------------------------

class Inspeccion(models.Model):             
    nro_inspeccion = models.AutoField(primary_key = True, unique_for_year = True)     
    apiario = models.ForeignKey(Apiario)    
    fecha_inspeccion = models.DateTimeField('Fecha de Inspeccion', blank = False)
    observacion = models.CharField(max_length=300, blank = False)
    habilita = models.BooleanField (default = False)
    
    class Meta:
        unique_together =  ("nro_inspeccion", "apiario")        
#---------------------------------

class Lote(models.Model):             
    nro_lote = models.AutoField(default = 0, primary_key= True, unique_for_year = True)     
    apiario = models.ForeignKey(Apiario)
    
    fecha_ingreso = models.DateTimeField('Fecha de Ingreso', default = timezone.now())
    fecha_egreso = models.DateTimeField ('Fecha de Egreso', blank = True)
    peso = models.DecimalField(max_digits = 6, decimal_places = 2, blank = False)
    observacion = models.CharField(max_length=300)

    class Meta:
        unique_together = ("nro_lote","apiario")        
#---------------------------------

class Alza (models.Model):             
    ALZA_ESTADOS = (
        ('LLENA','LLENA'),
        ('VACIA','VACIA')
    )             
    nro_alza = models.AutoField (primary_key = True, unique_for_year = True)
    alza_tipo = models.ForeignKey(Alza_tipo, null = False)
    apiario = models.ForeignKey(Apiario, null = False)
    condicion = models.CharField(max_length = 30, choices = ALZA_ESTADOS, default = 'LLENA')    
    cantidad_alzas = models.IntegerField(default = 0, blank = False)     
    peso = models.DecimalField(max_digits = 6, decimal_places = 2, blank = False)    

    class Meta:
        unique_together = ("nro_alza","alza_tipo", "apiario", "condicion")    
#---------------------------------
class Extraccion (models.Model):             
    nro_extraccion = models.AutoField (primary_key = True, unique_for_year = True)
    fecha_extraccion = models.DateTimeField ('Fecha de Extraccion', default = timezone.now())
    lote = models.ForeignKey (Lote, null = False)
    operario = models.ForeignKey (Persona, null = False)
    observacion = models.CharField (max_length = 300, blank = True)
    
    class Meta:
        unique_together =  ("nro_extraccion","lote")
#---------------------------------
class Tambor (models.Model):
    nro_tambor = models.AutoField (primary_key = True, unique_for_year = True)
    nro_extraccion = models.ForeignKey (Extraccion, null = False)
    peso = models.DecimalField (max_digits = 6, decimal_places = 2, blank = False)
    
    class Meta:
        unique_together =  ("nro_tambor","nro_extraccion")
#---------------------------------
class Marca (models.Model):
    nombre = models.CharField (max_length =20, primary_key = True)
    socio = models.ForeignKey (Persona)           
    habilitada = models.BooleanField (default = False)
    
#---------------------------------
class Fraccionamiento (models.Model):
    nro_fraccionamiento = models.AutoField (primary_key = True, unique_for_year = True)
    nro_tambor = models.ForeignKey (Tambor, null = False)
    fecha_fraccionamiento = models.DateTimeField ('Fecha de Fraccionamiento', default = timezone.now())
    operador = models.ForeignKey(Persona, null = False)
    
    class Meta:
        unique_together =  ("nro_fraccionamiento","nro_tambor")
#---------------------------------
class Envase (models.Model):
    nro_envase = models.AutoField (primary_key = True, unique_for_year = True)
    nro_fraccionamiento = models.ForeignKey (Tambor, null = False)
    envase_tipo = models.ForeignKey (Envase_tipo, null = False)
    # esta fecha tiene que ser calculada segun la fecha de fraccionamiento
    fecha_vencimiento = models.DateTimeField ('Fecha de Fraccionamiento', default = timezone.now())
    marca = models.ForeignKey (Marca, null = False)
    operador = models.ForeignKey(Persona, null = False)
    
    class Meta:
        unique_together =  ("nro_envase","nro_fraccionamiento")                
#---------------------------------
class Remito (models.Model):
    nro_remito = models.AutoField (primary_key = True, unique_for_year = True)            
    fecha_remito = models.DateTimeField ('Fecha de Retiro', default = timezone.now())
    operador = models.ForeignKey(Persona, null = False)
    observacion = models.CharField (max_length = 100)
    
#---------------------------------
class Remito_detalle (models.Model):
    nro_remito_detalle = models.AutoField (primary_key = True)
    renglon = models.IntegerField (default = 0)         # campo autonumerico dentro del remito
    nro_remito = models.ForeignKey (Remito, null = False)    
    nro_envase = models.ForeignKey (Envase)
    nro_tambor = models.ForeignKey (Tambor)

    class Meta:
        unique_together =  ("nro_remito_detalle","renglon","nro_remito")        