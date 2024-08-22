from django.urls import path
from .views import home

# URLs para operações específicas de home
## Direito com o home http://localhost:8000/home/
urlpatterns = [
    path('', home, name='home'),
]
