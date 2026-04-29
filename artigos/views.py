from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Artigo, Comentario
from .forms import ArtigoForm  # Precisamos de criar este form

# 1. Listagem: Todos podem ver
def lista_artigos(request):
    artigos = Artigo.objects.all().order_by('-data_criacao')
    return render(request, 'artigos/lista.html', {'artigos': artigos})

# 2. Criar: Apenas grupo 'autores'
@login_required
def criar_artigo(request):
    # Verifica se o utilizador pertence ao grupo 'autores'
    if not request.user.groups.filter(name='autores').exists():
        return redirect('artigos:lista_artigos')
    
    if request.method == 'POST':
        form = ArtigoForm(request.POST, request.FILES)
        if form.is_valid():
            artigo = form.save(commit=False)
            artigo.autor = request.user  # Define o autor como o utilizador logado
            artigo.save()
            return redirect('artigos:lista_artigos')
    else:
        form = ArtigoForm()
    
    return render(request, 'artigos/criar_artigo.html', {'form': form})

# 3. Editar: Apenas o próprio autor
@login_required
def editar_artigo(request, artigo_id):
    artigo = get_object_or_404(Artigo, id=artigo_id)
    
    # Segurança: Apenas o autor original pode editar
    if artigo.autor != request.user:
        return redirect('artigos:lista_artigos')
    
    if request.method == 'POST':
        form = ArtigoForm(request.POST, request.FILES, instance=artigo)
        if form.is_valid():
            form.save()
            return redirect('artigos:lista_artigos')
    else:
        form = ArtigoForm(instance=artigo)
        
    return render(request, 'artigos/editar_artigo.html', {'form': form, 'artigo': artigo})

# 4. Likes
@login_required
def like_artigo(request, artigo_id):
    artigo = get_object_or_404(Artigo, id=artigo_id)
    if request.user in artigo.likes.all():
        artigo.likes.remove(request.user)
    else:
        artigo.likes.add(request.user)
    return redirect('artigos:lista_artigos')