from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('cadastrar/', views.cadastrar, name='cadastrar'),
    path('login/', views.login_view, name='login')
]
