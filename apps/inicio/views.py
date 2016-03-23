from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import LoginForm

@login_required
def indexView(request):
    return render(request, "index.html")

def logoutView(request):
    logout(request)
    return redirect("/login/")


'''
    El metodo get permite buscar una key en el diccionario POST si no
    lo encuentra entonces el segundo parametro es el valor por default
    que es retornado, esta funcionalidad es propia del metodo get
'''
def loginView(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if (user is not None) and (user.is_active):
                login(request, user)
                return redirect(request.POST.get('next', '/'))
            else:
                messages.error(request, "Nombre de Usuario o contraseña Incorrecto")
                return redirect("/login/")
    form = LoginForm()
    return render(request, "login.html", {"form": form})
