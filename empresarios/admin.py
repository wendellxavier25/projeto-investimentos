from django.contrib import admin
from .models import Empresas, Documento

@admin.register(Empresas)
class EmpresasAdmin(admin.ModelAdmin):
    pass

@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    pass