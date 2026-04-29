from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from .forms import RegistoForm

def registo_view(request):
    if request.method == 'POST':
        form = RegistoForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Integração com a Parte 3: Associar automaticamente ao grupo 'autores'
            grupo_autores, created = Group.objects.get_or_create(name='autores')
            user.groups.add(grupo_autores)
            
            login(request, user) # Faz login automático após registo
            return redirect('index') # Altera para a tua rota principal
    else:
        form = RegistoForm()
    return render(request, 'accounts/registo.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST' or request.method == 'GET':
        logout(request)
        return redirect('login')