
from django.urls import path

from . import views


app_name = "users"

urlpatterns = [
    path("", views.user_list, name="list"),
    path("crear/", views.user_create, name="create"),
    path("<int:pk>/", views.user_detail, name="detail"),
    path("<int:pk>/editar/", views.user_update, name="update"),
    path(
        "<int:pk>/cambiar-estado/",
        views.user_toggle_active,
        name="toggle_active",
    ),
]
