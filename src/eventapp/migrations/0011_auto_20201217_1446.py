# Generated by Django 3.1.3 on 2020-12-17 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventapp', '0010_imovel_codigo_lote'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imovel',
            name='codigo_lote',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
