from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponse

# Função para renderizar a página inicial
def home(request):
    # Verifica se o usuário está autenticado
    if not request.user.is_authenticated:
        # Se o usuário não estiver logado, exibe uma mensagem de erro e redireciona para a página de login
        messages.error(request, "Usuário não logado")
        return redirect('login')

    # Se o usuário estiver autenticado, renderiza a página inicial
    return render(request, 'home/index.html')