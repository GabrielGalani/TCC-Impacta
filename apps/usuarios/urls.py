from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('logout/', views.logout, name='logout'),
    path('password-reset/', views.esqueci_a_senha, name='password_reset'),
    # Adicione outras URLs conforme necessário
]
