from django.forms import Form, CharField, TextInput, ModelForm, Select, DateInput, NumberInput
from .models import *
class EvalRiesgoForm(ModelForm):
    class Meta:
        model = evaluacion_riesgo
        fields = "__all__"
        widgets = {
            "localizacion": TextInput(attrs={"class": "form-control"}),
            "puesto": Select(attrs={"class": "form-control"}),
            "trabajadores": NumberInput(attrs={"class": "form-control"}),
            "fecha_eval": DateInput(attrs={"class": "form-control"}),
            "fecha_ul_eval": DateInput(attrs={"class": "form-control"})
        }