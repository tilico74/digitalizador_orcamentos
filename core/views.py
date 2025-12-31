from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponse
from .models import Orcamento
from .models import Descricao
from .forms import DescricaoForm


def home(request):
    return render(request, "core/index.html")


# orcamentos/views.py
def orc_listar(request):
    orcamentos = Orcamento.objects.order_by('-id_orc')[:30]
    return render(request, "core/orc_listar.html", {"orcamentos": orcamentos})

def orc_insere  (request):
    return render(request, "core/orc_insere.html")

def orc_excluir(request, id_orc):
    """
    GET: renderiza a página de confirmação/visualização do orçamento id_orc.
    POST: exclui o orçamento e redireciona para a listagem.
    """
    orc = get_object_or_404(Orcamento, id_orc=id_orc)
    items = orc.itens.all()

    if request.method == 'POST':
        # opcional: verificar token CSRF (o template deve ter {% csrf_token %})
        try:
            orc.delete()
            messages.success(request, 'Orçamento excluído com sucesso.')
            return redirect(reverse('orc_listar'))
        except Exception as e:
            messages.error(request, f'Erro ao excluir o orçamento: {e}')
            # continua para re-renderizar a página com a mensagem de erro

    context = {
        'orcamento': orc,   # no template usamos `descr` para os campos do orçamento
        'items': items, # lista de itens para exibir a tabela
    }    
    return render(request, "core/orc_excluir.html", context)

def orc_editar(request):
    return render(request, "core/orc_editar.html")

def orc_pdf(request):
    return render(request, "core/orc_pdf.html")




#descricao/views.py
def desc_listar(request):
    descricoes = Descricao.objects.order_by('-id_desc')
    return render(request, "core/desc_listar.html", {"descricoes": descricoes})

def desc_insere  (request):
    if request.method == "POST": 
        form = DescricaoForm(request.POST) 
        if form.is_valid(): 
            form.save() 
            return redirect("desc_listar") # redireciona para a lista 
    else: 
        form = DescricaoForm() 
        
    return render(request, "core/desc_insere.html", {"form": form})    


def desc_excluir(request, id_desc):
    """
    GET: renderiza a página de confirmação/visualização da descrição id_desc.
    POST: exclui a descrição e redireciona para a listagem.
    """
    descricao = get_object_or_404(Descricao, id_desc=id_desc)

    if request.method == 'POST':
        # opcional: verificar token CSRF (o template deve ter {% csrf_token %})
        try:
            descricao.delete()
            messages.success(request, 'Descrição excluída com sucesso.')
            return redirect(reverse('desc_listar'))
        except Exception as e:
            messages.error(request, f'Erro ao excluir a descrição: {e}')
            # continua para re-renderizar a página com a mensagem de erro

    context = {
        'descricao': descricao,   # no template usamos `descr` para os campos da descrição
    }    
    return render(request, "core/desc_excluir.html", context)

# descricao/views.py
def desc_editar(request, id_desc):
    descricao = get_object_or_404(Descricao, pk=id_desc)

    if request.method == "POST":
        form = DescricaoForm(request.POST, instance=descricao)
        if form.is_valid():
            form.save()
            return redirect("desc_listar")  # volta para a lista
    else:
        form = DescricaoForm(instance=descricao)

    return render(request, "core/desc_editar.html", {"form": form})
