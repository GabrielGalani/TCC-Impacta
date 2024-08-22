from django.apps import AppConfig


class HomeConfig(AppConfig):
    # Define o campo automático padrão para o modelo
    # 'django.db.models.BigAutoField' é usado para criar identificadores únicos para os modelos
    default_auto_field = 'django.db.models.BigAutoField'

    # Define o nome do aplicativo dentro do projeto Django
    # O caminho é relativo ao diretório 'apps', que é a estrutura de diretórios onde o app está localizado
    name = 'apps.home'
