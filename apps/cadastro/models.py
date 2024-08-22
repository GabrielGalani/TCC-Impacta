from django.db import models
from django.contrib.auth.models import User

# Modelo que representa um cliente
class Cliente(models.Model):
    # Nome do cliente
    nome = models.CharField(max_length=255)
    # Email do cliente, deve ser único
    email = models.EmailField(unique=True)
    # Número de telefone do cliente
    telefone = models.CharField(max_length=15)
    # Endereço do cliente
    endereco = models.CharField(max_length=225)
    # CNPJ do cliente, com um valor padrão
    cnpj = models.CharField(max_length=50, default="000.000.000/001-11")
    # Indica se o cliente está ativo ou inativo, ao exluir apenas mudar a flag
    ativo = models.BooleanField(default=True)

    def __str__(self):
        # Retorna o nome do cliente como representação textual do objeto
        return self.nome

# Modelo que representa um produto
class Produto(models.Model):
    # Nome do produto
    nome = models.CharField(max_length=255)
    # Preço do produto, com duas casas decimais
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    # Quantidade em estoque
    estoque = models.IntegerField()
    # Indica se o produto está ativo, ao excluir apenas mudar a flag
    ativo = models.BooleanField(default=True)

    def __str__(self):
        # Retorna o nome do produto como representação textual do objeto
        return self.nome

# Modelo que representa uma nota fiscal
class NotaFiscal(models.Model):
    # Número único da nota fiscal
    numero = models.CharField(max_length=20, unique=True)
    # Data e hora de emissão da nota fiscal, preenchido automaticamente
    data_emissao = models.DateTimeField(auto_now_add=True)

# Modelo que representa uma venda
class Venda(models.Model):
    # Referência ao usuário que fez a venda (Vendedor)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    # Referência ao cliente associado à venda
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    # Referência à nota fiscal associada à venda
    nota_fiscal = models.ForeignKey(NotaFiscal, on_delete=models.CASCADE)
    # Data e hora da venda, preenchido automaticamente
    data_venda = models.DateTimeField(auto_now_add=True)
    # Valor total da venda
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

# Modelo que representa um item em uma venda
class ItemVenda(models.Model):
    # Referência à venda à qual este item pertence
    venda = models.ForeignKey(Venda, related_name='itens', on_delete=models.CASCADE)
    # Referência ao produto vendido
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    # Quantidade do produto vendido
    quantidade = models.IntegerField()
    # Valor unitário do produto na venda
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2)
