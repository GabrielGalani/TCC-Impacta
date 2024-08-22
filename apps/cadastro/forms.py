from django import forms
from django.forms import inlineformset_factory
from .models import Cliente, Produto, Venda, ItemVenda

# Formulário para o modelo Cliente
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        # Define os campos que serão incluídos no formulário
        fields = ['nome', 'email', 'telefone', 'endereco', 'cnpj']

# Formulário para o modelo Produto
class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        # Define os campos que serão incluídos no formulário
        fields = ['nome', 'preco', 'estoque']

# Formulário para o modelo Venda
class VendaForm(forms.ModelForm):
    class Meta:
        model = Venda
        # Define os campos que serão incluídos no formulário
        fields = ['cliente']
    
    def __init__(self, *args, **kwargs):
        # Chama o construtor da classe pai para inicializar o formulário
        super().__init__(*args, **kwargs)
        # Define a queryset do campo 'cliente' para incluir todos os clientes
        self.fields['cliente'].queryset = Cliente.objects.all()

# Formulário para o modelo ItemVenda
class ItemVendaForm(forms.ModelForm):
    class Meta:
        model = ItemVenda
        # Define os campos que serão incluídos no formulário
        fields = ['produto', 'quantidade', 'valor_unitario']

# Cria um formset para o modelo ItemVenda relacionado à Venda
# Um formset é uma coleção de formulários do mesmo tipo
ItemVendaFormSet = inlineformset_factory(Venda, ItemVenda, form=ItemVendaForm, extra=1)

#Notas
## É aqui onde devem ser criados os modelos de formulários tanto para alterações como para inclusões!
### Atualmente estão sendo usados os mesmos formulários para criar e alterar itens


## Classe antiga que foi usada para o primeiro formulário, está de backup
# class VendaForm(forms.ModelForm):
#     class Meta:
#         model = Venda
#         fields = ['cliente', 'produto', 'quantidade']
    
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['cliente'].queryset = Cliente.objects.all()
#         self.fields['produto'].queryset = Produto.objects.all()