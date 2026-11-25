"""Rutas principales de SIDINO."""
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("academics/", include("apps.academics.urls") ),
]
