# core/forms.py
from django import forms
from .models import *

class DescricaoForm(forms.ModelForm):
    class Meta:
        model = Descricao
        fields = ["descricao"]
        labels = {
            "descricao": "Descrição"
        }
        widgets = {
            "descricao": forms.TextInput({'class': 'w-full rounded bg-white ring-1 ring-gray-300 px-2 pt-1 pb-1 text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500/40 focus:border-blue-500 transition duration-200',
            'placeholder': 'Digite a descrição...'}),
        }

    def clean_descricao(self):
        valor = self.cleaned_data["descricao"]
        return valor.capitalize()



class PesquisaDescricaoForm(forms.Form):
    termo = forms.CharField(
        label="Pesquisar",
        required=True,
        widget=forms.TextInput(attrs={
            "class": "w-full rounded bg-white ring-1 ring-gray-300 px-2 pt-1 pb-1 text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500/40 focus:border-blue-500 transition duration-200",
            "placeholder": "Digite parte da descrição..."
        })
    )

#****Formulario de Cadastro de endereço****#

# lista de estados brasileiros
UF_CHOICES = [ ("AC", "AC"), ("AL", "AL"), ("AP", "AP"), ("AM", "AM"), ("BA", "BA"), ("CE", "CE"), ("DF", "DF"), ("ES", "ES"), ("GO", "GO"), ("MA", "MA"), ("MT", "MT"), ("MS", "MS"), ("MG", "MG"), ("PA", "PA"), ("PB", "PB"), ("PR", "PR"), ("PE", "PE"), ("PI", "PI"), ("RJ", "RJ"), ("RN", "RN"), ("RS", "RS"), ("RO", "RO"), ("RR", "RR"), ("SC", "SC"), ("SP", "SP"), ("SE", "SE"), ("TO", "TO"), ]

class EnderecoForm(forms.ModelForm):

    uf = forms.ChoiceField( 
        choices=UF_CHOICES,
        initial="SC", # valor padrão 
        widget=forms.Select(
             attrs={ "class": "w-full rounded bg-white ring-1 ring-gray-300 px-2 pt-1 pb-1 text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500/40 focus:border-blue-500 transition duration-200", "placeholder": "UF"}
               ),
                label="UF"
    )


    class Meta:
        model = Endereco
        # escolha os campos que deseja expor no cadastro
        fields = [
            "tipo", "nome", "endereco", "numero",
            "municipio", "bairro", "uf", "cep",
            "contato", "email", "fone1", "fone2"
        ]
        labels = {
            "tipo": "Tipo",
            "nome": "Condomínio",
            "endereco": "Endereço",
            "numero": "Número",
            "municipio": "Município",
            "bairro": "Bairro",            
            "cep": "CEP",
            "contato": "Contato",
            "email": "E-mail",
            "fone1": "Fone",
            "fone2": "Fone",
        }
        widgets = { 
            "tipo": forms.HiddenInput(),           
            "nome": forms.TextInput(attrs={"class": "w-full rounded bg-white ring-1 ring-gray-300 px-2 pt-1 pb-1 text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500/40 focus:border-blue-500 transition duration-200", "placeholder": "Condomínio...","required": True, "id": "id_nome_condominio"}),
            "endereco": forms.TextInput(attrs={"class": "w-full rounded bg-white ring-1 ring-gray-300 px-2 pt-1 pb-1 text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500/40 focus:border-blue-500 transition duration-200", "placeholder": "Endereço..."}),
            "numero": forms.TextInput(attrs={"class": "w-full rounded bg-white ring-1 ring-gray-300 px-2 pt-1 pb-1 text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500/40 focus:border-blue-500 transition duration-200", "placeholder": "Número..."}),
            "municipio": forms.TextInput(attrs={"class": "w-full rounded bg-white ring-1 ring-gray-300 px-2 pt-1 pb-1 text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500/40 focus:border-blue-500 transition duration-200", "placeholder": "Município..."}),
            "bairro": forms.TextInput(attrs={"class": "w-full rounded bg-white ring-1 ring-gray-300 px-2 pt-1 pb-1 text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500/40 focus:border-blue-500 transition duration-200", "placeholder": "Bairro..."}),
            "cep": forms.TextInput(attrs={"class": "w-full rounded bg-white ring-1 ring-gray-300 px-2 pt-1 pb-1 text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500/40 focus:border-blue-500 transition duration-200 mask_cep", "placeholder": "00000-000"}),
            "contato": forms.TextInput(attrs={"class": "w-full rounded bg-white ring-1 ring-gray-300 px-2 pt-1 pb-1 text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500/40 focus:border-blue-500 transition duration-200", "placeholder": "Contato..."}),
            "email": forms.EmailInput(attrs={"class": "w-full rounded bg-white ring-1 ring-gray-300 px-2 pt-1 pb-1 text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500/40 focus:border-blue-500 transition duration-200", "placeholder": "seu_email@email.com..."}),
            "fone1": forms.TextInput(attrs={"class": "w-full rounded bg-white ring-1 ring-gray-300 px-2 pt-1 pb-1 text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500/40 focus:border-blue-500 transition duration-200 mask_fone", "placeholder": "(00) 0000-0000"}),
            "fone2": forms.TextInput(attrs={"class": "w-full rounded bg-white ring-1 ring-gray-300 px-2 pt-1 pb-1 text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500/40 focus:border-blue-500 transition duration-200 mask_fone",  "placeholder": "(00) 0000-0000"}),
        }

    def __init__(self, *args, **kwargs): # parâmetro extra para decidir se o campo tipo será escondido 
        tipo_fixo = kwargs.pop("tipo_fixo", None)
        super().__init__(*args, **kwargs)
        
        if tipo_fixo: # se foi passado um valor fixo, esconde o campo e define o valor 
            self.fields["tipo"].widget = forms.HiddenInput()
            self.fields["tipo"].initial = tipo_fixo

    def clean_nome(self):
        valor = self.cleaned_data["nome"]
        return valor.title()
    
    def clean_endereco(self):
        valor = self.cleaned_data["endereco"]
        return valor.title()
    
    def clean_municipio(self):
        valor = self.cleaned_data["municipio"]
        return valor.title()
    
    def clean_bairro(self):
        valor = self.cleaned_data["bairro"]
        return valor.title()
    
    def clean_contato(self):
        valor = self.cleaned_data.get("contato")
        if valor:  # só aplica title se não for None ou vazio
            return valor.title()
        return valor


class OrcamentoForm(forms.ModelForm):
    class Meta:
        model = Orcamento
        fields = [
            "nome", "complemento", "email",
            "fone1", "fone2", "obs", "data", "desconto"
        ]
        labels = {            
            "nome": "Nome",
            "complemento": "Complemento",
            "email": "E-mail",
            "fone1": "Fone",
            "fone2": "Fone",
            "obs": "Observações",
            "data": "Data",
            "desconto": "Desconto",
        }
        widgets = {            
            "nome": forms.TextInput(attrs={
                "class": "w-full rounded bg-white ring-1 ring-gray-300 px-2 pt-2 pb-1 "
                         "text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500/40 "
                         "focus:border-blue-500 transition duration-200",
                "placeholder": "Nome do cliente..."
            }),
            "complemento": forms.TextInput(attrs={
                "class": "w-full rounded bg-white ring-1 ring-gray-300 px-2 pt-2 pb-1 "
                         "text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500/40 "
                         "focus:border-blue-500 transition duration-200",
                "placeholder": "Complemento..."
            }),
            "email": forms.EmailInput(attrs={
                "class": "w-full rounded bg-white ring-1 ring-gray-300 px-2 pt-2 pb-1 "
                         "text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500/40 "
                         "focus:border-blue-500 transition duration-200",
                "placeholder": "email@cliente.com"
            }),
            "fone1": forms.TextInput(attrs={
                "class": "w-full rounded bg-white ring-1 ring-gray-300 px-2 pt-2 pb-1 "
                         "text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500/40 "
                         "focus:border-blue-500 transition duration-200 mask_fone",
                "placeholder": "(00) 0000-0000"
            }),
            "fone2": forms.TextInput(attrs={
                "class": "w-full rounded bg-white ring-1 ring-gray-300 px-2 pt-2 pb-1 "
                         "text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500/40 "
                         "focus:border-blue-500 transition duration-200 mask_fone",
                "placeholder": "(00) 0000-0000"
            }),
            "obs": forms.TextInput(attrs={
                "class": "w-full rounded bg-white ring-1 ring-gray-300 px-2 pt-2 pb-1 "
                         "text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500/40 "
                         "focus:border-blue-500 transition duration-200",
                "rows": 3,
                "placeholder": "Observações..."
            }),
            "data": forms.DateInput(attrs={
                "class": "w-full rounded bg-white ring-1 ring-gray-300 px-2 pt-2 pb-1 "
                         "text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500/40 "
                         "focus:border-blue-500 transition duration-200",
                "type": "date"
            }),
            "desconto": forms.NumberInput(attrs={
                "class": "w-full rounded bg-white ring-1 ring-gray-300 px-2 pt-2 pb-1 "
                         "text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500/40 "
                         "focus:border-blue-500 transition duration-200 text-right",
                "placeholder": "0,00"
            }),
        }

    def clean_nome(self):
        valor = self.cleaned_data["nome"]
        return valor.title()

    def clean_complemento(self):
        valor = self.cleaned_data.get("complemento")
        if valor:
            return valor.title()
        return valor

    def clean_obs(self):
        valor = self.cleaned_data.get("obs")
        if valor:
            return valor.capitalize()
        return valor

#Formulario de Itens do Orçamento
GANCHO_CHOICES = [
    ("", "Não Informado"),
    ("Zincados", "Zincados"),
    ("Inox", "Inox"),
]

COR_CHOICES = [
    ("", "Não Informada"),
    ("Bege", "Bege"),
    ("Cristal", "Cristal"),
    ("Marrom", "Marrom"),
    ("Preta", "Preta"),
]

class ItemForm(forms.ModelForm):
    descricao = forms.ChoiceField(    
    required=False,
    widget=forms.Select(attrs={
        "class": "w-full rounded bg-white ring-1 ring-blue-300 px-2 py-1 text-gray-700 focus:ring-2 focus:ring-blue-500/40"
    }),
    label="Descrição"
    )

    gancho = forms.ChoiceField(
        choices=GANCHO_CHOICES,
        required=False,
        widget=forms.Select(
            attrs={
                "class": "w-full rounded bg-white ring-1 ring-blue-300 px-2 py-1 text-gray-700 focus:ring-2 focus:ring-blue-500/40"
                         "focus:border-blue-500 transition duration-200"
            }
        ),
        label="Gancho"
    )

    cor = forms.ChoiceField(
        choices=COR_CHOICES,
        required=False,
        widget=forms.Select(
            attrs={
                "class": "w-full rounded bg-white ring-1 ring-blue-300 px-2 py-1 text-gray-700 focus:ring-2 focus:ring-blue-500/40 text-center"
            }
        ),
        label="Cor"
    )

    class Meta:
        model = Item
        fields = ["comprimento", "largura", "descricao", "gancho", "cor", "preco"]
        labels = {
            "comprimento": "Comprimento",
            "largura": "Largura",
            "preco": "Preço",
        }
        widgets = {
            "comprimento": forms.NumberInput(attrs={
                "class": "w-full rounded bg-white ring-1 ring-blue-300 px-2 py-1 text-gray-700 focus:ring-2 focus:ring-blue-500/40 text-center mask_number",
                "placeholder": "0.00"
            }),
            "largura": forms.NumberInput(attrs={
                "class": "w-full rounded bg-white ring-1 ring-blue-300 px-2 py-1 text-gray-700 focus:ring-2 focus:ring-blue-500/40 text-center mask_number",
                "placeholder": "0.00"
            }),
            "preco": forms.NumberInput(attrs={
                "class": "w-full rounded bg-white ring-1 ring-blue-300 px-2 py-1 text-gray-700 focus:ring-2 focus:ring-blue-500/40 text-center mask_number",
                "placeholder": "0.00"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["descricao"].choices = [
            (d.descricao, d.descricao)
            for d in Descricao.objects.all()
        ]



class PesquisaCondominioForm(forms.Form):
    nome = forms.CharField(
        label="Nome",
        required=False,
        widget=forms.TextInput(attrs={
            "class": "w-full rounded bg-white ring-1 ring-gray-300 px-2 pt-1 pb-1 text-gray-700 "
                     "focus:outline-none focus:ring-2 focus:ring-blue-500/40 focus:border-blue-500 transition duration-200",
            "placeholder": "Digite parte do nome..."
        })
    )

    endereco = forms.CharField(
        label="Endereço",
        required=False,
        widget=forms.TextInput(attrs={
            "class": "w-full rounded bg-white ring-1 ring-gray-300 px-2 pt-1 pb-1 text-gray-700 "
                     "focus:outline-none focus:ring-2 focus:ring-blue-500/40 focus:border-blue-500 transition duration-200",
            "placeholder": "Digite parte do endereço..."
        })
    )

    bairro = forms.CharField(
        label="Bairro",
        required=False,
        widget=forms.TextInput(attrs={
            "class": "w-full rounded bg-white ring-1 ring-gray-300 px-2 pt-1 pb-1 text-gray-700 "
                     "focus:outline-none focus:ring-2 focus:ring-blue-500/40 focus:border-blue-500 transition duration-200",
            "placeholder": "Digite parte do bairro..."
        })
    )

    municipio = forms.CharField(
        label="Município",
        required=False,
        widget=forms.TextInput(attrs={
            "class": "w-full rounded bg-white ring-1 ring-gray-300 px-2 pt-1 pb-1 text-gray-700 "
                     "focus:outline-none focus:ring-2 focus:ring-blue-500/40 focus:border-blue-500 transition duration-200",
            "placeholder": "Digite parte do município..."
        })
    )
