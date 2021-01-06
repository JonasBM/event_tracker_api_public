# Generated by Django 3.1.3 on 2020-12-17 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventapp', '0011_auto_20201217_1446'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imovel',
            name='codigo',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='imovel',
            name='codigo_lote',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='imovel',
            name='inscricao_imobiliaria',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
