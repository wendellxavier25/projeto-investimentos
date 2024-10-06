from django.urls import path
from . import views

app_name = 'empresas'


urlpatterns = [
    path('cadastrar_empresa/', views.cadastrar_empresa, name="cadastrar_empresa"),
]
