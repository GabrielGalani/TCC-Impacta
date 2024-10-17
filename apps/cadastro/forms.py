from django import forms
from django.forms import inlineformset_factory, modelformset_factory
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from .models import Cliente, Produto, Venda, ItemVenda, NotaFiscal
import re 

# Formulário para o modelo Cliente
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        # Define os campos que serão incluídos no formulário
        fields = ['nome', 'email', 'telefone', 'endereco', 'cnpj']

# Fomrulário para alterar clientes
class ClienteAlterForm(forms.ModelForm): 
    class Meta:
        model = Cliente
        # Campos do formulário
        fields = ['nome', 'email', 'telefone', 'endereco', 'ativo']
        # Atributos de cada campo do formulário
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Digite um nome válido'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Digite um e-mail válido'}),
            'telefone': forms.TextInput(attrs={'placeholder': 'O numero de telefone deve seguir op padrao ddd9xxxxxxxx'}),
            'endereco': forms.TextInput(attrs={'placeholder': 'Digite um endereço válido'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

    # Verificando se o usuário logado é um administrador que poderá ativar um cliente excluido
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and not user.is_superuser:
            self.fields.pop('ativo')
        else:
            self.fields['ativo'].widget.attrs.update({'class': 'form-check-input'})

    def clean_telefone(self): 
        #validação de telefone real
        telefone = self.cleaned_data.get('telefone')
        
        if not re.match(r'^\d{10,15}$', telefone):
            raise ValidationError('Número de telefone inválido. Deve conter entre 10 e 15 dígitos.')
        return telefone

# Formulário para o modelo Produto
class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        # Define os campos que serão incluídos no formulário
        fields = ['nome', 'preco', 'estoque']


class ProdutoAlterForm(forms.ModelForm): 
    class Meta:
        model = Produto
        # Campos do formulário
        fields = ['nome', 'preco', 'estoque', 'ativo']
        # Atributos de cada campo do formulário
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Digite um nome válido'}),
            'preco': forms.NumberInput(attrs={'step': '0.01'}),
            'estoque': forms.NumberInput(attrs={'min': '0'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

    # Verificando se o usuário logado é um administrador que poderá ativar um cliente excluido
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and not user.is_superuser:
            self.fields.pop('ativo')
        else:
            self.fields['ativo'].widget.attrs.update({'class': 'form-check-input'})


# Formulário para o modelo Venda
class VendaForm(forms.ModelForm):
    class Meta:
        model = Venda
        # Remove o campo 'data_venda', pois não pode ser editado
        fields = ['cliente']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cliente'].queryset = Cliente.objects.all()

# Formulário para o modelo ItemVenda
class ItemVendaForm(forms.ModelForm):
    class Meta:
        model = ItemVenda
        fields = ['venda','produto', 'quantidade', 'valor_unitario']  # Remover valor_total
        
# Cria um formset para o modelo ItemVenda relacionado à Venda
# Um formset é uma coleção de formulários do mesmo tipo
ItemVendaFormSet = modelformset_factory(ItemVenda, form=ItemVendaForm, extra=1)

class NotaFiscalForm(forms.ModelForm):
    class Meta:
        model = NotaFiscal
        fields = ['numero']
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