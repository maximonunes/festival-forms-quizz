from django import forms
from .models import Artigo

class ArtigoForm(forms.ModelForm):
    class Meta:
        model = Artigo
        fields = ['titulo', 'texto', 'fotografia', 'link_externo']
        widgets = {
            'texto': forms.Textarea(attrs={'rows': 5}),
        }