# core/forms.py
from django import forms
from .models import Descricao

class DescricaoForm(forms.ModelForm):
    class Meta:
        model = Descricao
        fields = ["descricao"]
        labels = {
            "descricao": "Descrição"
        }
        widgets = {
            "descricao": forms.TextInput({'class': 'w-full rounded bg-white ring-1 ring-gray-300 px-2 pt-1 pb-1 text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500/40 focus:border-blue-500 transition duration-200', 'placeholder': 'Digite a descrição...'}),
        }

    def clean_descricao(self):
        valor = self.cleaned_data["descricao"]
        return valor.capitalize()

