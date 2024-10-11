from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('usuarios/', include('usuarios.urls')),
    path('empresarios/', include('empresarios.urls')),
    path('', lambda request: redirect('/empresarios/cadstrar_empresa'))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
