# Generated by Django 5.1.1 on 2024-10-15 11:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('empresarios', '0004_remove_metricas_arquivo_metricas_valor'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='metricas',
            options={'verbose_name': 'metrica', 'verbose_name_plural': 'metricas'},
        ),
    ]
