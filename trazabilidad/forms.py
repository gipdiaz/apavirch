from django import forms
from django.forms.models import BaseInlineFormSet
from .models import Lote, GrupoAlza, Socio, SocioMarca, Marca, TipoEnvase, Apiario, Remito, RemitoDetalle, Fraccionamiento, Tambor
from django.forms import ModelForm, Form
from django.forms.models import inlineformset_factory, formset_factory, modelformset_factory
from django.core.exceptions import ValidationError

#-------------------------------------------------------#
#--   Forms de Lote  --#
class FormLote(ModelForm):
    class Meta:
            fields = ('apiario','peso','observacion')
            model = Lote

class GAForm(ModelForm):
    class Meta:
        model = GrupoAlza

class GrupoAlzaRequiredFormSet(forms.models.BaseInlineFormSet):

    def clean(self):

        super(GrupoAlzaRequiredFormSet, self).clean()

        count = 0
        for form in self.forms:
            try:
                if form.cleaned_data:
                    count += 1
            except AttributeError:
                pass
        if count < 1:
            raise forms.ValidationError('Se necesita al menos un Grupo de Alza')

GrupoAlzaFormSet = inlineformset_factory(Lote, GrupoAlza,form=GAForm,formset=GrupoAlzaRequiredFormSet, extra=1, max_num=3, fields=("idGrupoAlza","tipoAlza","lote","cantidadAlzas","peso"))


#-------------------------------------------------------#
#---------  Forms de Socio  ----------------------------#

class FormSocio(ModelForm):
    #--  form para editar/ingresar socios cuyo estado es a prueba --#
    Prueba = forms.CharField(max_length= 100)
    class Meta:
        fields = ('codigoUnicoIdentif' ,'tipoDocumento', 'nroDocumento','nombreYApellido','direccion','telefono','email', 'nroRenapa')
        model = Socio
    
class FormSocioEditar(ModelForm):
    #--  form para editar socios cuyo estado no es a prueba  --#
    class Meta:
        fields = ('codigoUnicoIdentif' ,'tipoDocumento', 'nroDocumento','nombreYApellido','direccion','telefono','email', 'nroRenapa')
        model = Socio


class FormMarcaSocio(Form):
    #--  form para gestionar las marcas del socio --#
    checkSocioMarca = forms.BooleanField(required=False)
    idMarca = forms.IntegerField(required= False)
    descripcion = forms.CharField (max_length =20, required= False)
    tipoMarca = forms.CharField (max_length =20, required= False)

MarcaFormSet = formset_factory(FormMarcaSocio, extra = 0)

#-------------------------------------------------------#
#---------  Forms de Tambor  ---------------------------#

class FormTambor(Form):
    tipoEnvase = forms.ModelChoiceField(queryset=TipoEnvase.objects.all(), required=True)
    marca = forms.ModelChoiceField(queryset=Marca.objects.all(), required=True)


#-------------------------------------------------------#
#---------  Forms de Apiario  ---------------------------#

class FormApiarioSocio(Form):
    class Meta:
        fields = ('nroChacra' ,'cantidadColmenas')
        model = Apiario

ApiarioSocioFormSet = modelformset_factory(Apiario, extra = 1)



#-------------------------------------------------------#
#---------  Forms de Remito  ---------------------------#

class FormRemito(ModelForm):
    #--  form para editar/ingresar remitos--#
    class Meta:
        fields = ('socio','observacion')
        model = Remito

class RemitoDetalleForm(Form):
    CHOICES = (
    (Tambor.__class__.__name__, 'Tambor'),
    (Fraccionamiento.__class__.__name__, 'Fraccionamiento'),
    )

    tipoDetalle = forms.ChoiceField(choices = CHOICES, required=True)
    tambor = forms.ModelChoiceField(queryset=Tambor.objects.all(), required = False)
    fraccionamiento = forms.ModelChoiceField(queryset=Fraccionamiento.objects.all(), required = False)

class RemitoDetalleRequiredFormSet(forms.models.BaseInlineFormSet):

    def clean(self):

        super(RemitoDetalleRequiredFormSet, self).clean()

        count = 0
        for form in self.forms:
            try:
                if form.cleaned_data:
                    count += 1
            except AttributeError:
                pass
        if count < 1:
            raise forms.ValidationError('Se necesita al menos detalle')

RemitoDetalleFormSet = formset_factory(RemitoDetalleForm, extra=1)


#-------------------------------------------------------#
#---------  Forms de Remito  ---------------------------#

class FormApiarioSocio(Form):
    class Meta:
        fields = ('nroChacra' ,'cantidadColmenas')
        model = Apiario

ApiarioSocioFormSet = modelformset_factory(Apiario, extra = 1)





