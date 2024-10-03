# TCC-Impacta

Este README fornece as instruções para configurar e rodar o projeto **TCC-Impacta**.

## 1. Iniciar o repositório na pasta desejada
```
git init
```
## 2.Clonar o repositório do GitHub
```
git clone https://github.com/GabrielGalani/TCC-Impacta.git
```

## 3.Mover-se para dentro do projeto
```
cd .\TCC-Impacta\
```

## 4.Criar um ambiente virtual
```
python -m venv .venv
```
 
## 5. Ativar o ambiente virtual
```
.\.venv\Scripts\activate
```

## 6. Instalar os requerimentos do projeto
```
pip install -r .\requirements.txt
```

## 7. Abrir o VS Code
```
code .
```

# Banco de Dados
## Utilizando SQLite (Padrão)
## 8.1 No arquivo settings.py (TCC-Impacta\Tcc_impacta\settings.py):
8.1.1 Encontre as configurações de banco de dados pesquisando por Database.
8.1.2 Para manter o SQLite como banco de dados de testes (recomendado), retire os comentários do seguinte bloco de configurações:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```
8.1.3 No arquivo manage.py, comentar o bloco da imagem:
![Imagem 8.1.3](https://github.com/GabrielGalani/TCC-Impacta/blob/main/imagem_tela/tela_4.png)

## Utilizando Outro Banco de Dados para Produção (SQL Server como Exemplo)
### Observação: siga os mesmos passos de 8.1 e 8.1.1.
8.2.1 Para trocar o banco de dados, comente o bloco:

```
# DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': BASE_DIR / 'db.sqlite3',
#   }
# }
```

8.2.2 Faça as configurações do seu banco de dados nesse bloco. No caso do SQL Server:
```
DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': 'seu_banco_de_dados',
        'USER': 'seu_usuario_de_banco',
        'PASSWORD': 'seu_password_de_login',
        'HOST': 'seu_host_de_banco_de_dados',
        'PORT': 'sua_porta_de_banco',
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
            'trusted_connection': 'yes',
        },
    }
}
```

8.2.2 Case tenha feito a alteração no arquivo manage.py, conforme item 8.1.3, você terá que desfazer todas as alterações. 

8.2.3 Com seu banco de dados já instalado, crie o banco de dados, no caso foi criado como exemplo o banco de dados DW, cujo host é GABGALANI, conforme as imagens abaixo:
---- Imagem Host
![Imagem host](https://github.com/GabrielGalani/TCC-Impacta/blob/main/imagem_tela/tela_5.png)

---- Imagem banco de dados criado
![Imagem banco de dados](https://github.com/GabrielGalani/TCC-Impacta/blob/main/imagem_tela/tela_6.png)


### 8.2.3 Instale as dependências necessárias. No caso do SQL Server, foi utilizado o ODBC 17. Se necessário, você pode fazer o download do driver [aqui](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver16).


### 8.2.4 No passo 8.2.2 foi solicitado para descomentar umm bloco de código, agora que temos nosso banco criado, devemos preencher aquele bloco da seguinte forma, baseando-se nas configurações do banco criado.
```
DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': 'DW',
        'USER': '', # Deixar em branco caso seja login com autenticação do windows ou preencher com seu usuário de banco de dados
        'PASSWORD': '', # Deixar em branco caso seja login com autenticação do windows ou preencher com sua senha de banco de dados
        'HOST': 'GABGALANI', # Nome do seu host vide foto acima
        'PORT': '', # Deixar em branco para porta default, ou configurar uma porta de saida
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server', # Driver sendo usado
            'trusted_connection': 'yes', # Conexão segura
        },
    }
}
```

### Agora, basta seguir os passos abaixo normalmente.

# Rodando e Testando o Projeto
## 9.1 Criar o Banco de Dados Físico e Migrar as Dependências
Certifique-se de estar em seu ambiente virtual e na pasta do projeto, e faça as migrações:

```
python .\manage.py makemigrations
```
```
python .\manage.py migrate
```

## 10.1 Rodar o Projeto em Ambiente Local
Após fazer as migrações, rode o projeto:
```
python .\manage.py runserver
```
Você deverá ver algo parecido com isso em seu terminal.
![Imagem terminal](https://github.com/GabrielGalani/TCC-Impacta/blob/main/imagem_tela/tela%201.png)


## 10.2 Acessar o Software
Para acessar o software, no seu navegador digite:
```
http://localhost:8000/
```
Você deverá acessar o seguinte sistema.

![Imagem Software login](https://github.com/GabrielGalani/TCC-Impacta/blob/main/imagem_tela/tela_2.png)

## 11.1 Criando super usuário (admin) para primeiro acesso:

### 11.1.1 No terminal do VsCode, rodar o comando abaixo para criação do usuário e seguir os passos de configuração
```
 python .\manage.py createsuperuser  
```
![Imagem create superuser](https://github.com/GabrielGalani/TCC-Impacta/blob/main/imagem_tela/tela_7.png)

### 11.1.2 Após a configuração do super usuário, você está apto para primeiro acesso como administrador do sistema, seja muito bem vindo!
![Imagem Software home page](https://github.com/GabrielGalani/TCC-Impacta/blob/main/imagem_tela/tela_9.png)



## Observações:
Como utilizei o SQLite, o banco foi criado na pasta do meu projeto. Caso queira ver as alterações e migrações, utilize o visualizador de SQLite (extensão do VS Code) ou o site [SQLite Viewer](https://inloop.github.io/sqlite-viewer/).


O banco de dados pode ser encontrado na pasta do projeto.
![Imagem banco](https://github.com/GabrielGalani/TCC-Impacta/blob/main/imagem_tela/Tela%203%20.png)


# Esse projeto foi desenvolvido por: 
### Augusto Vieira Bonfim - augusto.bonfim@aluno.faculdadeimpacta.com.br;
### Dylberth Romullo Pinheiro Santana - dylberth.santana@aluno.faculdadeimpacta.com.br;
### Gabriel Galani Silva - gabriel.galani@aluno.faculdadeimpacta.com.br;
### Renan Queiroz Eliziario - renan.eliziario@aluno.faculdadeimpacta.com.br.



