from django.contrib import admin
from .models import Cliente, Produto, Venda

# Registro do modelo Cliente com a interface administrativa do Django
@admin.register(Cliente)
class CadastroClienteAdmin(admin.ModelAdmin):
    # Define quais campos serão exibidos na lista de registros no painel admin
    list_display = ('id', 'nome', 'email')
    
    # Define quais campos serão pesquisáveis no painel admin
    search_fields = ('nome', 'email')
    
    # Define quais campos serão usados como filtros na lista de registros
    list_filter = ('nome',)

# Registro do modelo Produto com a interface administrativa do Django
@admin.register(Produto)
class CadastroProdutoAdmin(admin.ModelAdmin):
    # Define quais campos serão exibidos na lista de registros no painel admin
    list_display = ('id', 'nome', 'preco')
    
    # Define quais campos serão pesquisáveis no painel admin
    search_fields = ('nome',)
    
    # Define quais campos serão usados como filtros na lista de registros
    list_filter = ('nome',)


# Notas:
## É aqui onde trazemos os modelos para aparecer no painel administrativo do django http://localhost:8000/admin