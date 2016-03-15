from django.shortcuts import render
from .forms import *
# Create your views here.
def new_eval_riesgo(request):
    form = EvalRiesgoForm()
    return render(request, "new_eval_riesgo.html", {"collapse_er": "in", "active_n": "active", "form": form})
