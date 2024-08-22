from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

# Cria uma instância do roteador padrão do Django REST Framework
router = DefaultRouter()

# Registra os ViewSets com o roteador para gerar automaticamente as URLs para operações CRUD padrão
router.register(r'clientes', ClienteViewSet)
router.register(r'produtos', ProdutoViewSet)
router.register(r'vendas', VendaViewSet)

# Qualquer uma das urls abaixo iniciam com API devido ao urlpatterns do setup
## Ex: api/cadastrar/
urlpatterns = [
    # Inclui as URLs geradas automaticamente pelo roteador
    path('', include(router.urls)),

    # URLs para operações específicas de cliente
    path('cadastrar/', cadastrar_cliente, name='cadastrar_cliente'),
    path('excluir/<int:cliente_id>/', excluir_cliente, name='excluir_cliente'),
    path('listar/', listar_clientes, name='listar_clientes'),
    path('alterar/<int:cliente_id>/', alterar_cliente, name='alterar_cliente'),

    # URLs para operações específicas de produto
    path('cadastrar_produto/', cadastrar_produto, name='cadastrar_produto'),
    path('excluir_produto/<int:produto_id>/', excluir_produto, name='excluir_produto'),
    path('listar_produto/', listar_produto, name='listar_produto'),
    path('alterar_produto/<int:produto_id>/', alterar_produto, name='alterar_produto'),

    # URLs para operações específicas de venda
    path('cadastrar_venda/', criar_venda, name='cadastrar_venda'),
    path('listar_venda/', listar_vendas, name='listar_vendas'),

    # URLs para operações de consulta de produto
    path('get-produto-preco/<int:produto_id>/', get_produto_preco, name='get_produto_preco'),
    path('get-produtos/', get_produtos, name='get_produtos'),
]
