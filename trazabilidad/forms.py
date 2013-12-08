from django import forms
from django.forms.models import BaseInlineFormSet
from .models import Lote, GrupoAlza, Socio, SocioMarca
from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from django.core.exceptions import ValidationError


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


class FormSocio(ModelForm):
    Prueba = forms.CharField(max_length= 100)
    class Meta:
        fields = ('codigoUnicoIdentif' ,'tipoDocumento', 'nroDocumento','nombreYApellido','direccion','telefono','email', 'nroRenapa')
        model = Socio
    

class FormSocioEditar(ModelForm):
    class Meta:
        fields = ('codigoUnicoIdentif' ,'tipoDocumento', 'nroDocumento','nombreYApellido','direccion','telefono','email', 'nroRenapa')
        model = Socio

class FormSocioMarca(ModelForm):
    class Meta:
        model = SocioMarca






