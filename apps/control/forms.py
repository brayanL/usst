from django.forms import Form, CharField, TextInput, ModelForm, Select, DateInput, NumberInput
from .models import *
class EvalRiesgoForm(ModelForm):
    class Meta:
        model = evaluacion_riesgo
        exclude = ('usuario', 'evaluacion')
        widgets = {
            "localizacion": TextInput(attrs={"class": "form-control", "required": True}),
            "puesto": TextInput(attrs={"class": "form-control", "required": True}),
            "trabajadores": NumberInput(attrs={"class": "form-control", "required": True}),
            "fecha_eval": DateInput(attrs={"class": "form-control", "required": True}),
            "fecha_ul_eval": DateInput(attrs={"class": "form-control"})
        }