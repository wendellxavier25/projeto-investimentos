from django.urls import path
from . import views


app_name ="investidores"


urlpatterns = [
    path('sugestão/', views.sugestao, name="sugestao"),
]
