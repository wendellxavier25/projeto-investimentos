from django.urls import path
from . import views


app_name ="investidores"


urlpatterns = [
    path('sugestão/', views.sugestao, name="sugestao"),
    path('ver_empresa/<int:id>', views.ver_empresa, name="ver_empresa"),
    path('realizar_proposta/<int:id>', views.realizar_proposta, name="realizar_proposta"),
    path('assinar_contrato/<int:id>', views.assinar_contrato, name="assinar_contrato")
]
