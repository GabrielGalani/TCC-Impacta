# Generated by Django 5.0.8 on 2024-08-19 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastro', '0002_cliente_ativo'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='cnpj',
            field=models.CharField(default='000.000.000/001-11', max_length=50),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='endereco',
            field=models.CharField(max_length=225),
        ),
    ]
