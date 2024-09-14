from django.http import HttpRequest, HttpResponse
from django.contrib import auth
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import LoginForms
from .forms import Cadastro
import re
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from django.shortcuts import render, redirect
from django.contrib import messages


# View para o login de usuários
def login(request: HttpRequest) -> HttpResponse:
    form = LoginForms()
    
    if request.method == "POST": 
        form = LoginForms(request.POST)
        
        if form.is_valid(): 
            nome: str = form.cleaned_data['nome_login']  # Use cleaned_data para obter valores validados
            senha: str = form.cleaned_data['senha']

            # Autentica o usuário com o nome e senha fornecidos
            usuario = auth.authenticate(
                request,
                username=nome,
                password=senha
            )

            if usuario is not None: 
                auth.login(request, usuario)
                messages.success(request, f'{nome} logado com sucesso!')
                return redirect('home')
            else:
                messages.error(request, 'Erro ao efetuar login! Credenciais inválidas!')
                return redirect('login')
    
    return render(request, 'usuarios/login.html', {'form': form})

#View para redefinição de senha

def esqueci_a_senha(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(
                request=request,
                use_https=request.is_secure(),
                token_generator=default_token_generator,
                from_email=None,
                email_template_name='password_reset_email.html',
                subject_template_name='password_reject_subject.txt',
                html_email_template_name='password_reset_email.html',                
            )
            messages.success(request, 'Um e-mail foi enviado com instruções para redefinir sua senha.')
            return redirect('password_reset_done')
        else:
            form = PasswordResetForm() 
        return render(request, 'usuarios/password_reset.html', {'form':form})


# View para o cadastro de novos usuários
def validar_senha(senha: str) -> bool:
    """Valida se a senha atende aos critérios de segurança."""
    if len(senha) < 10:
        return False
    if not re.search(r"[A-Z]", senha):  # Verifica se contém letras maiúsculas
        return False
    if not re.search(r"[a-z]", senha):  # Verifica se contém letras minúsculas
        return False
    if not re.search(r"[0-9]", senha):  # Verifica se contém números
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", senha):  # Verifica se contém símbolos
        return False
    if re.search(r"(.)\1{2,}", senha):  # Verifica se há caracteres repetidos
        return False
    return True

def cadastro(request):
    form = Cadastro()
    
    if request.method == "POST": 
        form = Cadastro(request.POST)
        
        if form.is_valid():
            # Verifica se as senhas inseridas são iguais
            senha_um = form['senha_um'].value()
            senha_dois = form['senha_dois'].value()

            if senha_um != senha_dois:
                messages.error(request, 'As senhas não correspondem')
                return redirect('cadastro')
            
            # Valida a complexidade da senha
            if not validar_senha(senha_um):
                messages.error(request, 'A senha deve ter pelo menos 16 caracteres, incluir letras maiúsculas, minúsculas, números e símbolos.')
                return redirect('cadastro')
            
            nome = form['nome_cadastro'].value()
            email = form['email'].value()
            
            if User.objects.filter(username=nome).exists():
                messages.error(request, 'Usuário já existente!')
                return redirect('cadastro')
            
            usuario = User.objects.create_user(
                username=nome,
                email=email,
                password=senha_um
            )
            
            usuario.save()
            
            messages.success(request, f'Cadastro efetuado com sucesso! Seja bem-vindo {nome}')
            return redirect('login')
        
    return render(request, 'usuarios/cadastro.html', {'form': form})

# View para deslogar o usuário
def logout(request):
    messages.success(request, 'Deslogado com sucesso!')
    auth.logout(request)
    return redirect('login')