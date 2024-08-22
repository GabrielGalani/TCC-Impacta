"""
URL configuration for Tcc_impacta project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Rota para o painel administrativo do Django
    path('admin/', admin.site.urls),

    # Rota para as URLs do app de cadastro
    path('api/', include('apps.cadastro.urls')),

    # Rota para as URLs do app home
    path('home/', include('apps.home.urls')),

    # Rota para as URLs do app de usuários, padrão para a raiz do site
    path('', include('apps.usuarios.urls')),
]