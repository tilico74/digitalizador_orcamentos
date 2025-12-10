from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponse
from .models import Orcamento

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
