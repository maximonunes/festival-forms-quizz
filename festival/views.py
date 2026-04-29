from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required # Import necessário
from .models import Dia, Palco, Concerto               
from .forms import ConcertoForm, PalcoForm

# Helper function para verificar se é gestor (evita repetir código)
def e_gestor(user):
    return user.groups.filter(name='gestor-portfolio').exists()

def index_view(request):
    return render(request, 'festival/index.html')

def dias_view(request):
    dias = Dia.objects.all()
    context = {'dias': dias}
    return render(request, 'festival/dias.html', context)

def palcos_view(request):
    palcos = Palco.objects.all() 
    context = {'palcos': palcos}
    return render(request, 'festival/palcos.html', context)

def concerto_view(request, concerto_id):
    concerto = get_object_or_404(Concerto, id=concerto_id)
    context = {'concerto': concerto}
    return render(request, 'festival/concerto.html', context)

# --- VIEWS PROTEGIDAS (CRUD) ---

@login_required
def editar_concerto_view(request, concerto_id):
    # Requisito: Apenas gestor-portfolio pode editar
    if not e_gestor(request.user):
        return redirect('index')

    concerto = get_object_or_404(Concerto, id=concerto_id)
    if request.method == 'POST':
        form = ConcertoForm(request.POST, instance=concerto)
        if form.is_valid():
            form.save()
            return redirect('concerto', concerto_id=concerto.id)
    else:
        form = ConcertoForm(instance=concerto)

    context = {'concerto': concerto, 'form': form}
    return render(request, 'festival/editar_concerto.html', context)

@login_required
def criar_concerto_view(request):
    if not e_gestor(request.user):
        return redirect('index')

    if request.method == 'POST':
        form = ConcertoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dias') 
    else:
        form = ConcertoForm()
    
    return render(request, 'festival/criar_concerto.html', {'form': form})

@login_required
def apagar_concerto_view(request, concerto_id):
    if not e_gestor(request.user):
        return redirect('index')

    concerto = get_object_or_404(Concerto, id=concerto_id)
    if request.method == 'POST':
        concerto.delete()
        return redirect('dias') 
    return redirect('concerto', concerto_id=concerto.id)

@login_required
def editar_palco_view(request, palco_id):
    if not e_gestor(request.user):
        return redirect('index')

    palco = get_object_or_404(Palco, id=palco_id)
    if request.method == 'POST':
        form = PalcoForm(request.POST, request.FILES, instance=palco)
        if form.is_valid():
            form.save()
            return redirect('palcos')
    else:
        form = PalcoForm(instance=palco)
        
    context = {'form': form, 'palco': palco}
    return render(request, 'festival/editar_palco.html', context)