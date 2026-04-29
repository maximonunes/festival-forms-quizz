from django import forms
from .models import Concerto, Palco

class ConcertoForm(forms.ModelForm):
    class Meta:
        model = Concerto
        fields = "__all__"  # ALTERADO: Substitui ["hora"] para permitir editar tudo

class PalcoForm(forms.ModelForm):
    class Meta:
        model = Palco
        fields = "__all__"  # ALTERADO: Substitui a lista manual para apanhar o novo campo Booleano