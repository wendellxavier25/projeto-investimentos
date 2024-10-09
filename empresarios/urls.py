from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'empresas'


urlpatterns = [
    path('cadastrar_empresa/', views.cadastrar_empresa, name="cadastrar_empresa"),
    path('listar_empresas/', views.listar_empresas, name="listar_empresas"),
    path('empresa/<int:id>', views.empresa, name="empresa"),
    path('add_doc/<int:id>', views.add_doc, name="add_doc")

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
