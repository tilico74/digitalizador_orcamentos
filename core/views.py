from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .models import *
from .forms import *


def home(request):
    return render(request, "core/index.html")


#****************************** orcamentos/views.py****************
def orc_listar(request):
    orcamentos = Orcamento.objects.order_by('-id_orc')[:30]
    return render(request, "core/orc_listar.html", {"orcamentos": orcamentos})

def orc_insere_index(request):
    return render(request, "core/orc_insere_index.html")



def orc_insere(request, tipo=None):
    ItemFormSet = inlineformset_factory(
        Orcamento,
        Item,
        form=ItemForm,
        extra=1,
        can_delete=True
    )

    if request.method == "POST":
        form_orc = OrcamentoForm(request.POST)
        form_end = EnderecoForm(request.POST, tipo_fixo=tipo)
        formset = ItemFormSet(request.POST, queryset=Item.objects.none())

        if form_orc.is_valid() and form_end.is_valid() and formset.is_valid():
            endereco = form_end.save()
            orcamento = form_orc.save(commit=False)
            orcamento.endereco = endereco
            orcamento.save()

            formset.instance = orcamento  # vincula itens ao orçamento
            formset.save()

            return redirect("orc_listar")
    else:
        form_orc = OrcamentoForm()
        form_end = EnderecoForm(tipo_fixo=tipo)
        formset = ItemFormSet(queryset=Item.objects.none())

    return render(
        request,
        "core/orc_insere.html",
        {
            "form_orc": form_orc,
            "form_end": form_end,
            "formset": formset,
            "tipo": tipo,
        }
    )


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




#****************************************************descricao/views.py **************
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


def desc_pesquisar(request):
    form = PesquisaDescricaoForm(request.GET or None)
    descricoes = Descricao.objects.none()  # começa vazio

    if form.is_valid():
        termo = form.cleaned_data.get("termo")
        if termo:  # só busca se houver termo
            descricoes = Descricao.objects.filter(descricao__icontains=termo)

    # limpa o form depois da pesquisa
    form = PesquisaDescricaoForm()

    return render(request, "core/desc_pesquisar.html", {
        "form": form,
        "descricoes": descricoes
    })

#**************Condomínios views.py**********************
def cond_listar(request):
    # pega últimos 30 registros tipo "cond"
    condominios = Endereco.objects.filter(tipo="cond").order_by("-id_end")[:30]

    # normaliza os nomes conforme regras
    substituicoes = {
        "Condomínio": "Cond.",
        "Condominio": "Cond.",
        "Edifício": "Edif.",
        "Edificio": "Edif.",
        "Residencial": "Resid."
    }

    lista_condominios = []
    for c in condominios:
        nome = c.nome or ""
        for termo, abreviado in substituicoes.items():
            nome = nome.replace(termo, abreviado)
        # cria um atributo extra para usar no template
        c.nome_formatado = nome
        lista_condominios.append(c)

    return render(request, "core/cond_listar.html", {
        "condominios": lista_condominios
    })

def cond_insere(request):
    if request.method == "POST":
        form = EnderecoForm(request.POST, tipo_fixo="cond")
        if form.is_valid():
            form.save()
            return redirect("cond_listar")
    else:
        form = EnderecoForm(tipo_fixo="cond")
    return render(request, "core/cond_insere.html", {"form": form})


def cond_excluir(request, id_cond):
    """
    GET: renderiza a página de confirmação/visualização do condomínio id_end.
    POST: exclui o condomínio e redireciona para a listagem.
    """
    condominio = get_object_or_404(Endereco, id_end=id_cond)

    if request.method == 'POST':
        try:
            condominio.delete()
            messages.success(request, 'Condomínio excluído com sucesso.')
            return redirect(reverse('cond_listar'))
        except Exception as e:
            messages.error(request, f'Erro ao excluir o condomínio: {e}')
            # continua para re-renderizar a página com a mensagem de erro

    context = {
        'condominio': condominio,   # no template usamos `condominio` para exibir os dados
    }
    return render(request, "core/cond_excluir.html", context)
 

def cond_editar(request, id_cond):
    cond = get_object_or_404(Endereco, pk=id_cond)
    if request.method == "POST":
        form = EnderecoForm(request.POST, instance=cond, tipo_fixo="cond")
        if form.is_valid():
            form.save()
            return redirect("cond_listar")
    else:
        form = EnderecoForm(instance=cond, tipo_fixo="cond")
    return render(request, "core/cond_editar.html", {"form": form})


def cond_pesquisar(request):
    condominios = []
    form = PesquisaCondominioForm(request.GET or None)

    if form.is_valid():
        nome = form.cleaned_data.get('nome')
        endereco = form.cleaned_data.get('endereco')
        bairro = form.cleaned_data.get('bairro')
        municipio = form.cleaned_data.get('municipio')

        qs = Endereco.objects.filter(tipo='cond')

        if nome:
            qs = qs.filter(nome__icontains=nome)
        if endereco:
            qs = qs.filter(endereco__icontains=endereco)
        if bairro:
            qs = qs.filter(bairro__icontains=bairro)
        if municipio:
            qs = qs.filter(municipio__icontains=municipio)

        condominios = qs

        # limpa o form depois da pesquisa
        form = PesquisaCondominioForm()

    return render(request, "core/cond_pesquisar.html", {
        "form": form,
        "condominios": condominios,
    })

