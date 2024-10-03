from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from rest_framework import viewsets
from .models import Cliente, Produto, Venda, Venda
from .serializers import ClienteSerializer, ProdutoSerializer, VendaSerializer
from .forms import *
from django.http import JsonResponse
from django.db import transaction
import uuid


# ViewSet para o modelo Cliente
class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()  # Define a consulta para obter todos os clientes
    serializer_class = ClienteSerializer

# ViewSet para o modelo Produto
class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()  # Define a consulta para obter todos os produtos
    serializer_class = ProdutoSerializer

# ViewSet para o modelo Venda
class VendaViewSet(viewsets.ModelViewSet):
    queryset = Venda.objects.all()  # Define a consulta para obter todas as vendas
    serializer_class = VendaSerializer

# Função para cadastrar um novo cliente (Usa o formulário)
def cadastrar_cliente(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado")
        return redirect('login')
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ClienteForm()
    return render(request, 'cadastro/cadastrar_clientes.html', {'form': form})

# Função para excluir (desativar) um cliente (Muda a flag no banco de dados)
def excluir_cliente(request, cliente_id):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado")
        return redirect('login')
    cliente = get_object_or_404(Cliente, id=cliente_id)
    # if request.method == 'POST':
        # cliente.delete()
    # return redirect('home')
    cliente.ativo = False
    cliente.save()
    return redirect('listar_clientes')
    # return render(request, 'cadastro/excluir_cliente.html', {'cliente': cliente})

# Função para listar todos os clientes ativos (Usa o formulário)
def listar_clientes(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado")
        return redirect('login')
    
    if request.user.is_superuser:
        clientes = Cliente.objects.all()
    else:
        clientes = Cliente.objects.filter(ativo=True)
    
    return render(request, 'cadastro/listar_clientes.html', {'clientes': clientes})

# Função para alterar os dados de um cliente
def alterar_cliente(request, cliente_id):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado")
        return redirect('login')

    cliente = get_object_or_404(Cliente, id=cliente_id)
    
    if request.method == 'POST':
        form = ClienteAlterForm(request.POST, instance=cliente, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente atualizado com sucesso!')
            return redirect('listar_clientes')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = ClienteAlterForm(instance=cliente, user=request.user)

        if not cliente_id:
            form = ClienteAlterForm(user=request.user)
    
    return render(request, 'cadastro/alterar_cliente.html', {'form': form})

## PRODUTOS

# Função para cadastrar um novo produto (Usa o formulário)
def cadastrar_produto(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado")
        return redirect('login')
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProdutoForm()
    return render(request, 'produtos/cadastro_produto.html', {'form': form})

# Função para excluir (desativar) um produto (Muda a flag do modelo)
def excluir_produto(request, produto_id):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado")
        return redirect('login')
    produto = get_object_or_404(Produto, id=produto_id)
    # if request.method == 'POST':
        # cliente.delete()
    # return redirect('home')
    produto.ativo = False
    produto.save()
    return redirect('listar_produto')
    # return render(request, 'cadastro/excluir_cliente.html', {'cliente': cliente})


# Função para listar todos os produtos ativos (Usa o formulário)
def listar_produto(request):

    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado")
        return redirect('login')
    
    # clientes = Cliente.objects.all()
    if request.user.is_superuser:
        produtos = Produto.objects.all()
    else:
        produtos = Produto.objects.filter(ativo=True)
    return render(request, 'produtos/listar_produtos.html', {'produtos': produtos})


# Função para alterar os dados de um produto
def alterar_produto(request, produto_id):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado")
        return redirect('login')
    
    produto = get_object_or_404(Produto, id=produto_id)

    if request.method == 'POST':
        form = ProdutoAlterForm(request.POST, instance=produto, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto atualizado com sucesso!')
            return redirect('listar_produto')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = ProdutoAlterForm(instance=produto, user=request.user)

        if not produto_id:
            form = ProdutoAlterForm(user=request.user)

    return render(request, 'produtos/alterar_produto.html', {'form': form})




## Vendas

# Função para criar uma nova venda (Usa formulário)
def criar_venda(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado")
        return redirect('login')

    if request.method == "POST":
        form = VendaForm(request.POST)
        formset = ItemVendaFormSet(request.POST)
        
        print("Form válido:", form.is_valid())
        print("Formset válido:", formset.is_valid())
        print("Form erros:", form.errors)
        print("Formset erros:", formset.errors)

        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                # Cria a nota fiscal
                nota_fiscal = NotaFiscal.objects.create(
                    numero=str(uuid.uuid4())[:8]
                )
                venda = form.save(commit=False)
                venda.usuario = request.user
                venda.nota_fiscal = nota_fiscal
                venda.save()

                total_venda = 0
                for form in formset:
                    item = form.save(commit=False)
                    item.venda = venda
                    item.valor_unitario = item.produto.preco
                    item.save()

                    # Subtrai a quantidade vendida do estoque
                    produto = item.produto
                    produto.estoque -= item.quantidade
                    produto.save()

                    total_venda += item.quantidade * item.valor_unitario
                
                venda.valor_total = total_venda
                venda.save()

            messages.success(request, 'Venda cadastrada com sucesso!')
            return redirect('listar_vendas')
    else:
        form = VendaForm()
        formset = ItemVendaFormSet()

    return render(request, 'cadastro/criar_venda.html', {'form': form, 'formset': formset})

# Função para listar todas as vendas
def listar_vendas(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado")
        return redirect('login')
    vendas = Venda.objects.all()  # Obtém todas as vendas do banco de dados
    return render(request, 'cadastro/listar_vendas.html', {'vendas': vendas})

# Função para obter o preço de um produto específico em formato JSON
def get_produto_preco(request, produto_id):
    try:
        produto = get_object_or_404(Produto, id=produto_id)
        return JsonResponse({'valor_unitario': produto.preco})
    except Produto.DoesNotExist:
        return JsonResponse({'error': 'Produto não encontrado'}, status=404)
    
# Função para listar os detalhes de uma venda específica
def listar_venda_detalhes(request, venda_id):
    venda = Venda.objects.filter(id=venda_id).prefetch_related('itens').first()
    if venda:
        itens = venda.itens.all()
        total_venda = venda.valor_total
        return render(request, 'cadastro/listar_venda_detalhes.html', {
            'venda': venda,
            'itens': itens,
            'total_venda': total_venda
        })
    else:
        messages.error(request, "Venda não encontrada")
        return redirect('listar_vendas')
    
# Função para obter todos os produtos em formato JSON
def get_produtos(request):
    produtos = Produto.objects.all()
    produtos_data = [{'id': p.id, 'nome': p.nome} for p in produtos]
    return JsonResponse({'produtos': produtos_data})



#Backup
# def criar_venda(request):
#     if not request.user.is_authenticated:
#         messages.error(request, "Usuário não logado")
#         return redirect('login')

#     if request.method == "POST":
#         form = VendaForm(request.POST)
#         formset = ItemVendaFormSet(request.POST)

#         if form.is_valid() and formset.is_valid():
#             with transaction.atomic():
#                 nota_fiscal = NotaFiscal.objects.create(
#                     numero=str(uuid.uuid4())[:8]  # Gera um número único para a nota
#                 )
#                 venda = form.save(commit=False)
#                 venda.usuario = request.user
#                 venda.nota_fiscal = nota_fiscal
#                 venda.save()

#                 total_venda = 0
#                 for form in formset:
#                     item = form.save(commit=False)
#                     item.venda = venda
#                     item.valor_unitario = item.produto.preco
#                     item.save()
#                     total_venda += item.quantidade * item.valor_unitario
                
#                 venda.valor_total = total_venda
#                 venda.save()

#             messages.success(request, 'Venda cadastrada com sucesso!')
#             return redirect('listar_vendas')
#     else:
#         form = VendaForm()
#         formset = ItemVendaFormSet()

#     return render(request, 'cadastro/criar_venda.html', {'form': form, 'formset': formset})