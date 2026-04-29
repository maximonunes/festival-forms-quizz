from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from .forms import RegistoForm


def magic_link_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            token = str(uuid.uuid4())
            
            # Guardamos o token e o ID do utilizador na sessão do servidor
            # Definimos que o link expira em 300 segundos (5 minutos)
            request.session['magic_token'] = token
            request.session['magic_user_id'] = user.id
            request.session.set_expiry(300) 
            
            magic_url = request.build_absolute_uri(f'/accounts/login/magic/{token}/')
            
            print(f"\n--- MAGIC LINK PARA {user.username} ---")
            print(magic_url)
            print("---------------------------------------\n")
            
            return render(request, 'accounts/magic_sent.html', {'email': email})
        except User.DoesNotExist:
            return render(request, 'accounts/magic_sent.html', {'error': 'Email não encontrado'})
            
    return render(request, 'accounts/magic_request.html')

def magic_login(request, token):
    # 1. Recuperamos os dados guardados na sessão
    saved_token = request.session.get('magic_token')
    user_id = request.session.get('magic_user_id')

    # 2. Verificamos se o token é igual ao que enviámos
    if saved_token and saved_token == token:
        user = get_object_or_404(User, id=user_id)
        login(request, user)
        
        # Limpamos a sessão para o token não ser usado outra vez
        del request.session['magic_token']
        del request.session['magic_user_id']
        
        return redirect('index')
    
    # Se o token for inválido ou expirou
    return render(request, 'accounts/magic_sent.html', {'error': 'Link inválido ou expirado.'})

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