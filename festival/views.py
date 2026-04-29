from django.shortcuts import get_object_or_404, redirect, render
from .models import Dia, Palco, Concerto               
from .forms import ConcertoForm, PalcoForm


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
    concerto = Concerto.objects.get(id=concerto_id)

    context = {'concerto': concerto}

    return render(request, 'festival/concerto.html', context)


def editar_concerto_view(request, concerto_id):
    concerto = get_object_or_404(Concerto, id=concerto_id)

    if request.method == 'POST':
        form = ConcertoForm(request.POST, instance=concerto)
        if form.is_valid():
            form.save()
            return redirect('concerto', concerto_id=concerto.id)
    else:
        form = ConcertoForm(instance=concerto)

    context = {
        'concerto': concerto,
        'form': form,
    }

    return render(request, 'festival/editar_concerto.html', context)


# ... (deixa estar o resto do código existente para cima)

def criar_concerto_view(request):
    if request.method == 'POST':
        form = ConcertoForm(request.POST)
        if form.is_valid():
            form.save()
            # Assumindo que a tua rota principal se chama 'dias' ou 'index'
            return redirect('dias') 
    else:
        form = ConcertoForm()
    
    context = {'form': form}
    return render(request, 'festival/criar_concerto.html', context)


def apagar_concerto_view(request, concerto_id):
    concerto = get_object_or_404(Concerto, id=concerto_id)
    
    if request.method == 'POST':
        concerto.delete()
        # Após apagar, volta à página de dias
        return redirect('dias') 
        
    # Se alguém tentar aceder via GET (escrevendo o URL), mandamos de volta para o concerto
    return redirect('concerto', concerto_id=concerto.id)


def editar_palco_view(request, palco_id):
    palco = get_object_or_404(Palco, id=palco_id)
    
    if request.method == 'POST':
        # NOTA: request.FILES é obrigatório porque o Palco tem um ImageField!
        form = PalcoForm(request.POST, request.FILES, instance=palco)
        if form.is_valid():
            form.save()
            return redirect('palcos')
    else:
        form = PalcoForm(instance=palco)
        
    context = {
        'form': form, 
        'palco': palco
    }
    return render(request, 'festival/editar_palco.html', context)