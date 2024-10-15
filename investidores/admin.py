from django.contrib import admin
from .models import PropostaInvestimento

@admin.register(PropostaInvestimento)
class AdminPropostaInvestimento(admin.ModelAdmin):
    pass