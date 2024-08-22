from django.urls import path
from .views import login, cadastro, logout

# URLs para operações específicas de usuarios
## Direito  http://localhost:8000/cadastro/
urlpatterns = [
    path('', login, name='login'),
    path('cadastro/', cadastro, name='cadastro',),
    path('logout/', logout, name='logout')
    
]