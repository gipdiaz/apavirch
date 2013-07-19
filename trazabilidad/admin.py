from django.contrib import admin
from trazabilidad.models import *

## ----------------------------------- ##

class CiudadAdmin(admin.ModelAdmin):
    list_display = ('descripcion', 'codigo_postal', 'added_by')
    ordering = ('-descripcion',)
    search_fields = ('descripcion',)
    exclude = ['added_by']
    
    def save_model(self, request, obj, form, change):
        obj.added_by = request.user
        obj.save()
        
    def queryset(self, request):
        qs = super(CiudadAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(added_by=request.user)
    
    """def has_change_permission(self, request, obj=None):
        if not obj:
            return True # So they can see the change list page
        if request.user.is_superuser or obj.author == request.user:
            return True
        else:
            return False
    
    has_delete_permission = has_change_permission"""

admin.site.register(Alza)
admin.site.register(Alza_tipo)
admin.site.register(Apiario)
admin.site.register(Ciudad, CiudadAdmin)
admin.site.register(Direccion)
admin.site.register(Documento_tipo)
admin.site.register(Envase)
admin.site.register(Envase_tipo)
admin.site.register(Extraccion)
admin.site.register(Fraccionamiento)
admin.site.register(Inspeccion)
admin.site.register(Lote)
admin.site.register(Marca)
admin.site.register(Persona)
admin.site.register(Remito)
admin.site.register(Remito_detalle)
admin.site.register(Socio)
admin.site.register(Tambor)