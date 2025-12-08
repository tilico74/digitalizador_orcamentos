from django.shortcuts import render
from django.http import HttpResponse
from .models import Orcamento

def home(request):
    return render(request, "core/index.html")


# orcamentos/views.py
def orc_listar(request):
    orcamentos = Orcamento.objects.order_by('-id_orc')[:30]
    return render(request, "core/orc_listar.html", {"orcamentos": orcamentos})

def teste_orcamentos(request):
    orcamentos = Orcamento.objects.all()
    return render(request, "core/teste.html", {"orcamentos": orcamentos})
