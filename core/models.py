from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from decimal import Decimal

#Classe Usuário
class UsuarioPerfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    apelido = models.CharField(max_length=45, blank=True, null=True)
    fone = models.CharField(max_length=15, blank=True, null=True)

    # Somente se quiser manter o conceito antigo
    # 0 = usuário normal
    # 1 = administrador do sistema
    previlegio = models.IntegerField(default=0)

    class Meta:
        db_table = 'usuario_moderno'  # evitar conflito com tabela antiga
        ordering = ['user__username']

    def __str__(self):
        return self.apelido or self.user.username


#Classe Orçamento
class Orcamento(models.Model):
    id_orc = models.AutoField(primary_key=True, db_column='id_orc')
    endereco = models.ForeignKey(
        'Endereco',
        on_delete=models.PROTECT,
        db_column='endereco_id_end'  # coluna correta no banco legado
    )
    nome = models.CharField(max_length=160)
    complemento = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=160, blank=True, null=True)
    fone1 = models.CharField(max_length=15, blank=True, null=True)
    fone2 = models.CharField(max_length=15, blank=True, null=True)
    obs = models.CharField(max_length=200, blank=True, null=True)
    data = models.DateField(default=timezone.now)
    desconto = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        ordering = ['-id_orc']
        managed = False  # importante para não tentar alterar tabela existente
        db_table = 'orcamento'

    @property
    def m2(self):
        return round(self.comprimento * self.largura, 3)
    

    @property
    def total_m2(self):
        return sum(item.m2 for item in self.itens.all())

    @property
    def subtotal(self):
        return sum(item.subtotal for item in self.itens.all())

    @property
    def total(self):
        return self.subtotal - self.desconto

    def __str__(self):
        return f'Orçamento #{self.id_orc} - {self.nome}'


    


#Classe Endereço
class Endereco(models.Model):
    id_end = models.AutoField(primary_key=True)

    tipo = models.CharField(max_length=10)
    nome = models.CharField(max_length=160, blank=True, null=True)
    endereco = models.CharField(max_length=200)
    numero = models.CharField(max_length=45)

    municipio = models.CharField(max_length=160)
    bairro = models.CharField(max_length=160)
    uf = models.CharField(max_length=2)
    cep = models.CharField(max_length=9)

    contato = models.CharField(max_length=160, blank=True, null=True)
    email = models.EmailField(max_length=160, blank=True, null=True)
    fone1 = models.CharField(max_length=15, blank=True, null=True)
    fone2 = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'endereco'
        ordering = ['municipio', 'bairro', 'endereco']

    def __str__(self):
        nome = self.nome or self.contato or "Sem nome"
        return f"{nome} - {self.endereco}, {self.numero} - {self.bairro} ({self.municipio}/{self.uf})"



#Classe Itens do Orçamento
class Item(models.Model):
    id_iten = models.AutoField(primary_key=True)  # Agora Django sabe qual é a PK
    orcamento = models.ForeignKey(
        Orcamento,
        related_name='itens',
        db_column='orcamento_id_orc',  # Mapeia o nome da coluna real
        on_delete=models.CASCADE
    )
    comprimento = models.DecimalField(max_digits=10, decimal_places=2)
    largura = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.CharField(max_length=120, blank=True, null=True)
    gancho = models.CharField(max_length=45, blank=True, null=True)
    cor = models.CharField(max_length=45, blank=True, null=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'iten'

       

    @property
    def m2(self):
        return round(self.comprimento * self.largura, 3)    
           
    @property
    def subtotal(self):
        return round(self.m2 * self.preco, 2)

    def __str__(self):
        return f'Item {self.descricao or ""} ({self.m2} m²)'

#Classe Descrição sever de apoio padronização do atribulto descricao da classe Item.


class Descricao(models.Model):
    id_desc = models.AutoField(primary_key=True)
    descricao = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'descricao'
        ordering = ['descricao']

    def __str__(self):
        return self.descricao or f"Descrição #{self.id_desc}"
    

