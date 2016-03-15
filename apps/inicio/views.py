from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import LoginForm

@login_required
def indexView(request):
    return render(request, "index.html")

def logoutView(request):
    logout(request)
    return redirect("/login/")


def loginView(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if (user is not None) and (user.is_active):
                login(request, user)
                return redirect("/")
            else:
                #messages.error(request, "Nombre de Usuario o contraseña Incorrecto")
                print("Credenciales incorrectas")
                return redirect("/login/")
    form = LoginForm()
    return render(request, "login.html", {"form": form})
