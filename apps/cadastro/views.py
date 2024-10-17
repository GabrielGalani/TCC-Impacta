from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from django.contrib import messages
from rest_framework import viewsets
from .models import Cliente, Produto, Venda, Venda, NotaFiscal, ExclusaoVenda
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
            messages.success(request, "Cadastrado com sucesso")
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
    produtos = Produto.objects.all()  # Lista de produtos
    if request.method == "POST":
        data = request.POST
        form = VendaForm(request.POST)
        formset = ItemVendaFormSet(request.POST)

        # Criação da nota fiscal apenas uma vez
        nota_fiscal = NotaFiscal.objects.create(
            numero=str(uuid.uuid4())[:8]  # Gera um número único para a nota fiscal
        )

        cliente = request.POST.get('cliente')
        valor_total_venda = request.POST.get('valor_total_venda')

        # Obter os produtos e quantidades
        produtos_venda = request.POST.getlist('form-0-produto')
        quantidade_produtos = request.POST.getlist('form-0-quantidade')
        valor_unitario = request.POST.getlist('form-0-valor_unitario')

        # Salvar a venda apenas uma vez
        venda_usuario = request.user  # Coletar o usuário logado
        venda_cliente = Cliente.objects.get(id=cliente)  # Obter o cliente pelo id
        venda_nota_fiscal = nota_fiscal  # Associar a nota fiscal à venda
        venda_valor_total = valor_total_venda

        with transaction.atomic():  # Garante que todas as operações sejam atômicas
            # Salvar a venda
            venda = Venda.objects.create(
                usuario=venda_usuario,
                cliente=venda_cliente,
                nota_fiscal=venda_nota_fiscal,
                valor_total=venda_valor_total
            )

            # Iterar sobre os produtos e suas quantidades para salvar os itens da venda
            for i in range(len(produtos_venda)):
                item_venda_produto = Produto.objects.get(id=produtos_venda[i])
                item_venda_quantidade = quantidade_produtos[i]
                item_venda_valor_unitario = valor_unitario[i]

                # Salvar no modelo ItemVenda
                ItemVenda.objects.create(
                    venda=venda,  # Associar o item à venda
                    produto=item_venda_produto,
                    quantidade=item_venda_quantidade,
                    valor_unitario=item_venda_valor_unitario
                )

        messages.success(request, 'Venda cadastrada com sucesso!')
        return redirect('listar_vendas')  # Redireciona após salvar
    else:
        form = VendaForm()
        formset = ItemVendaFormSet(queryset=ItemVenda.objects.none())  # Formset vazio

    return render(request, 'cadastro/criar_venda.html', {
        'form': form,
        'formset': formset,
        'produtos': produtos  # Adiciona a lista de produtos ao contexto
    })

# Função para listar todas as vendas
def listar_vendas(request):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado")
        return redirect('login')
    
    # Executa a consulta SQL e obtém os resultados
    if request.user.is_superuser:
        condicao = "v.valida in (1, 0)"
    else:
        condicao = "v.valida = 1"

        # Consulta SQL para obter as vendas conforme a lógica desejada
    sql_query = f"""
                    select 
                        v.id,
                        c.nome AS cliente_nome,
                        NULL AS produto,
                        qtd.quantidade AS quantidade,
                        v.data_venda,
                        v.valor_total,
                        v.valida
                    from [dbo].[cadastro_venda] v 
                    inner join [dbo].[cadastro_notafiscal] nf ON (nf.id = v.nota_fiscal_id)
                    inner join [dbo].[cadastro_cliente] c ON (c.id = v.cliente_id)
                    inner join (
                        select 
                            i.venda_id,
                            sum(i.quantidade) AS quantidade
                        from [dbo].[cadastro_produto] p
                        inner join [dbo].[cadastro_itemvenda] i ON (i.produto_id = p.id)
                        group by
                            i.venda_id
                    ) qtd on (qtd.venda_id = v.id)
                    where 
                        {condicao}
                    """
    
    with connection.cursor() as cursor:
        cursor.execute(sql_query)
        vendas = cursor.fetchall()

    # Transforma os resultados em uma lista de dicionários para o contexto do template
    vendas_context = []
    for venda in vendas:
        vendas_context.append({
            'id': venda[0],
            'cliente_nome': venda[1],
            'produto': venda[2],
            'quantidade': venda[3],
            'data_venda': venda[4],
            'valor_total': venda[5],
            'valida': venda[6]
        })

    return render(request, 'cadastro/listar_vendas.html', {'vendas': vendas_context})


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


def get_produto_preco(request, produto_id):
    try:
        produto = Produto.objects.get(id=produto_id)
        return JsonResponse({'preco': produto.preco})
    except Produto.DoesNotExist:
        return JsonResponse({'error': 'Produto não encontrado'}, status=404)

def listar_itens_venda(request, venda_id):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado")
        return redirect('login')
    
    # Consulta SQL para obter os itens da venda
    sql_query = """
                select 
                    i.venda_id,
                    c.nome as Cliente,
                    p.nome,
                    p.preco,
                    i.quantidade,
                    i.quantidade * p.preco as Valor_total
                from [dbo].[cadastro_produto] p
                inner join [dbo].[cadastro_itemvenda] i on (i.produto_id = p.id)
                inner join [dbo].[cadastro_venda] v on (v.id = i.venda_id)
                inner join [dbo].[cadastro_cliente] c on (c.id = v.cliente_id)
                where v.id = %s
    """
    
    with connection.cursor() as cursor:
        cursor.execute(sql_query, [venda_id])
        itens = cursor.fetchall()

    # Transformando resultados em uma lista de dicionários
    itens_context = []
    for item in itens:
        itens_context.append({
            'venda_id': item[0],
            'cliente': item[1],
            'produto': item[2],
            'preco': item[3],
            'quantidade': item[4],
            'valor_total': item[5],
        })

    return render(request, 'cadastro/listar_itens_venda.html', {'itens': itens_context})


def excluir_venda(request, venda_id):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado")
        return redirect('login')

    venda = get_object_or_404(Venda, id=venda_id)

    if request.method == 'POST':
        justificativa = request.POST.get('justificativa')
        comentario = request.POST.get('comentario')
        
        # Criar registro de exclusão
        ExclusaoVenda.objects.create(
            venda=venda,
            justificativa=justificativa,
            comentario=comentario,
            usuario=request.user
        )
        
        # Marcar a venda como não válida
        venda.valida = False  # Certifique-se de que o campo `valida` existe no modelo
        venda.save()

        messages.success(request, "Venda excluída com sucesso.")
        return redirect('listar_vendas')

    return render(request, 'cadastro/excluir_venda.html', {'venda': venda})

# View para exibir o formulário de exclusão
def excluir_venda_form(request, venda_id):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado")
        return redirect('login')
    
    venda = get_object_or_404(Venda, id=venda_id)
    
    return render(request, 'cadastro/excluir_venda.html', {'venda': venda})

# View para processar a exclusão
def excluir_venda(request, venda_id):
    if not request.user.is_authenticated:
        messages.error(request, "Usuário não logado")
        return redirect('login')

    venda = get_object_or_404(Venda, id=venda_id)

    if request.method == 'POST':
        justificativa = request.POST.get('justificativa')
        comentario = request.POST.get('comentario')

        # Criar registro de exclusão
        ExclusaoVenda.objects.create(
            venda=venda,
            justificativa=justificativa,
            comentario=comentario,
            usuario=request.user
        )

        # Marcar a venda como não válida (valida = False)
        venda.valida = False
        venda.save()

        messages.success(request, "Venda excluída com sucesso.")
        return redirect('listar_vendas')

    return redirect('listar_vendas')


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



        # # Obter os produtos e quantidades
        # produtos_venda = request.POST.getlist('form-0-produto')
        # quantidade_produtos = request.POST.getlist('form-0-quantidade')
        # valor_unitario = request.POST.getlist('form-0-valor_unitario')


        # # Iterar sobre os produtos e suas quantidades
        # for i in range(len(produtos_venda)):
        #     print(f'Nota fiscal: {nota_fiscal} - '
        #           f'Cliente id: {cliente} - '
        #           f'valor_total_venda: {valor_total_venda} - '
        #           f'produtos_venda: {produtos_venda[i]} - '
        #           f'quantidade_produtos: {quantidade_produtos[i]} - '
        #           f'valor_unitario: {valor_unitario[i]} -'
        #           f'Valor_total_venda: {valor_total_venda}')

        #     # Salvar no model ItemVenda
        #     item_venda_nota = nota_fiscal
        #     item_venda_produto = produtos_venda[i]
        #     item_venda_quantidade = quantidade_produtos[i]
        #     item_venda_valor_unitario = valor_unitario[i]

        
        # # Salvar no Model Notas Fiscais
        # nota_fical_numero = nota_fiscal

        # # Salvar no model Venda
        # venda_usuario = request.user # Tem que coletar o usuario logado
        # venda_cliente = cliente
        # venda_nota_fiscal = nota_fiscal
        # venda_valor_total = valor_total_venda