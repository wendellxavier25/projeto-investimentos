from django.contrib import admin
from .models import Empresas, Documento, Metricas

@admin.register(Empresas)
class EmpresasAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cnpj', 'site', 'area', 'publico_alvo', 'valor']
    search_fields = ['nome', 'cnpj', 'site']
    list_filter = ['nome', 'cnpj', 'site']
    list_per_page = 10

@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    pass

@admin.register(Metricas)
class MetricasAdmin(admin.ModelAdmin):
    pass