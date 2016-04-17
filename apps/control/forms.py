from django.forms import Form, CharField, TextInput, ModelForm, Select, DateInput, NumberInput
from django.contrib.auth.models import User
from .models import *
class EvalRiesgoForm(ModelForm):
    class Meta:
        model = EvaluacionRiesgo
        exclude = ('usuario', 'evaluacion')
        widgets = {
            "localizacion": TextInput(attrs={"class": "form-control", "required": True}),
            "puesto": TextInput(attrs={"class": "form-control", "required": True}),
            "trabajadores": NumberInput(attrs={"class": "form-control", "required": True}),
            "fecha_eval": DateInput(attrs={"class": "form-control", "required": True}),
            "fecha_ul_eval": DateInput(attrs={"class": "form-control"})
        }

class PeligrosForm(ModelForm):
    class Meta:
        model = PeligroDetalle
        fields = "__all__"
        widgets = {
            "nombre": TextInput(attrs={"class": "form-control", "required": True}),
            "factor_r": Select(attrs={"class": "form-control", "required": True})
        }

class UsuariosForm(ModelForm):
    class Meta:
        model = User
        exclude = ('is_staff', 'is_active', 'is_superuser', 'password', 'groups', 'date_joined')
        widgets = {
            "username": TextInput(attrs={"class": "form-control", "required": True}),
            "first_name": TextInput(attrs={"class": "form-control"}),
            "last_name": TextInput(attrs={"class": "form-control"}),
            "email": TextInput(attrs={"class": "form-control", "type": "email"}),
        }
