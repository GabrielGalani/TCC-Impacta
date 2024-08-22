#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import pyodbc


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Tcc_impacta.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


def create_database_if_not_exists():
    # Conectando ao SQL Server usando autenticação do Windows
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=localhost;'
        'Trusted_Connection=yes;'
        'TrustServerCertificate=yes;'
    )
    conn.autocommit = True
    cursor = conn.cursor()

    # Verificando se o banco de dados DW existe, caso contrário, crie-o
    cursor.execute("IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'DW') CREATE DATABASE DW")
    cursor.close()
    conn.close()

# Chama a função para garantir que o banco de dados seja criado
create_database_if_not_exists()


if __name__ == '__main__':
    main()
