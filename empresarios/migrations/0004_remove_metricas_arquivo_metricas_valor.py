# Generated by Django 5.1.1 on 2024-10-11 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empresarios', '0003_metricas'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='metricas',
            name='arquivo',
        ),
        migrations.AddField(
            model_name='metricas',
            name='valor',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
    ]
