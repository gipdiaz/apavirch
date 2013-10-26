#from autoreports.admin import ReportAdmin
from django.contrib import admin
from trazabilidad.models import *
from trazabilidad.forms import *
from django import forms
from django.contrib.admin.options import InlineModelAdmin

## ----------------------------------- ##
class CustomModelAdmin(admin.ModelAdmin):
    
    def save_model(self, request, obj, form, change):
        obj.added_by = request.user
        obj.save()
    
    def queryset(self, request):
        qs = self.model._default_manager.get_query_set()
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        if request.user.is_superuser:
            return qs
        return qs.filter(added_by=request.user)

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        if request.user.is_superuser:
            return {
                    'add': self.has_add_permission(request),
                    'change': self.has_change_permission(request),
                    'delete': self.has_delete_permission(request),
            }
        else:
            return {}
## ----------------------------------- ##
class CustomPermissionAdmin(admin.ModelAdmin):
    
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        if request.user.is_superuser:
            return {
                    'add': self.has_add_permission(request),
                    'change': self.has_change_permission(request),
                    'delete': self.has_delete_permission(request),
            }
        else:
            return {}
## ----------------------------------- ##
class CiudadAdmin(CustomModelAdmin):
    list_display = ('descripcion', 'codigo_postal', 'added_by')
    ordering = ('-descripcion',)
    search_fields = ('descripcion',)
    exclude = ['added_by']

## ----------------------------------- ##
class GrupoAlzaInline(admin.TabularInline):
    model = Grupo_alza
    extra = 1
    formset = RequireOneFormSet

## ----------------------------------- ##
class LoteAdmin(CustomPermissionAdmin):
    fieldsets = [
        (None, {'fields': ['apiario', 'fecha_ingreso', 'observacion']}),
        ]
    inlines = [
        GrupoAlzaInline,
    ]
    list_display = ('nro_lote', 'apiario', 'fecha_ingreso', 'fecha_egreso','peso', 'observacion', 'devuelto')    
    
    list_filter = ['alza__alza_tipo__descripcion'] 

    search_fields = ('nro_lote', 'fecha_ingreso', 'fecha_egreso','peso', 'observacion', 'devuelto',)

    def save_model(self, request, obj, form, change):
        obj.added_by = request.user
        obj.save()

    def save_formset(self, request, form, formset, change):
        '''
           metodo que actualiza el peso total del lote mediante los grupos de alzas inline
        '''
        total = 0
        for i in range(int(request.POST['alza-TOTAL_FORMS'])):            
            key = 'alza-'+str(int(i))+'-peso'
            total += float(request.POST[key])
        instances = formset.save(commit=False)
        for instance in instances:
            instance.save()
        formset.save_m2m()
        instance.lote.update_total_peso(total)
## ----------------------------------- ##
class TamborInline(admin.TabularInline):
    model = Tambor
    extra = 1
    formset = RequireOneFormSet

class ExtraccionAdmin(CustomPermissionAdmin):
    fieldsets = [
        (None, {'fields': ['lote', 'operario', 'peso', 'observacion']}),
        ]
    inlines = [
        TamborInline,
    ]
    list_display = ('nro_extraccion', 'lote', 'operario', 'observacion')    
    #list_filter = ['alza__alza_tipo__descripcion'] 

    def save_model(self, request, obj, form, change):
        obj.added_by = request.user
        obj.save()
## ----------------------------------- ##
class PersonaAdmin(CustomPermissionAdmin):
    filter_horizontal = ('marcas',)
## ----------------------------------- ##
class GrupoAlzaAdmin(CustomPermissionAdmin):
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        if request.user.is_superuser:
            return {
                    'add': self.has_add_permission(request),
                    'change': self.has_change_permission(request),
                    'delete': self.has_delete_permission(request),
            }
        else:
            return {}
## ----------------------------------- ##
class TamborAdmin(CustomPermissionAdmin):
    list_display = ['nro_tambor','nro_extraccion','peso']

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        if request.user.is_superuser:
            return {
                    'add': self.has_add_permission(request),
                    'change': self.has_change_permission(request),
                    'delete': self.has_delete_permission(request),
            }
        else:
            return {}
## ----------------------------------- ##
class FraccionamientoAdmin(CustomPermissionAdmin):
    exclude = ('cantidad_envases',)
    list_display = ['nro_fraccionamiento','nro_tambor','envase_tipo','marca','cantidad_envases','fecha_fraccionamiento','operador']
## ----------------------------------- ##
class EnvaseAdmin(CustomPermissionAdmin):

    def nro_tambor(self, obj):
        return obj.nro_fraccionamiento.nro_tambor

    fieldsets = [
         (' ', {'fields': ['nro_envase','nro_tambor']}),
         (' ', {'fields': ['nro_fraccionamiento', 'envase_tipo', 'fecha_vencimiento','operador']}),
        ]

    readonly_fields = ('nro_envase','nro_tambor')

    list_display = ['nro_envase', 'nro_fraccionamiento', 'envase_tipo', 'fecha_vencimiento','operador','nro_tambor']


    


#    def nro_tambor(self, obj):
#        return '%s'%(obj.nro_fraccionamiento.nro_tambor)
#    nro_tambor.short_description = 'Numero Tambor'
    
## ----------------------------------- ##
admin.site.register(Grupo_alza, GrupoAlzaAdmin)
admin.site.register(Alza_tipo, CustomPermissionAdmin)
admin.site.register(Apiario, CustomPermissionAdmin)
admin.site.register(Ciudad, CiudadAdmin)
admin.site.register(Direccion, CustomPermissionAdmin)
admin.site.register(Documento_tipo, CustomPermissionAdmin)
admin.site.register(Envase, EnvaseAdmin)
admin.site.register(Envase_tipo, CustomPermissionAdmin)
admin.site.register(Extraccion, ExtraccionAdmin)
admin.site.register(Fraccionamiento, FraccionamientoAdmin)
admin.site.register(Inspeccion, CustomPermissionAdmin)
admin.site.register(Lote, LoteAdmin)
admin.site.register(Marca, CustomPermissionAdmin)
admin.site.register(Persona, PersonaAdmin)
admin.site.register(Remito, CustomPermissionAdmin)
admin.site.register(Remito_detalle)
admin.site.register(Socio, CustomPermissionAdmin)
admin.site.register(Tambor, TamborAdmin)