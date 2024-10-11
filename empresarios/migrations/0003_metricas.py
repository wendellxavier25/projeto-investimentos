# Generated by Django 5.1.1 on 2024-10-10 18:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empresarios', '0002_alter_empresas_options_documento'),
    ]

    operations = [
        migrations.CreateModel(
            name='Metricas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=30)),
                ('arquivo', models.FileField(upload_to='documentos')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='empresarios.empresas')),
            ],
        ),
    ]