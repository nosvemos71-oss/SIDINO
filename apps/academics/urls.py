
from django.urls import path

from . import views


app_name = "academics"

urlpatterns = [
    path(
        "areas/",
        views.area_list,
        name="area-list",
    ),
    path(
        "areas/crear/",
        views.area_create,
        name="area-create",
    ),
    path(
        "areas/<int:pk>/",
        views.area_detail,
        name="area-detail",
    ),
    path(
        "asignaturas/",
        views.subject_list,
        name="subject-list",
    ),
    path(
        "asignaturas/crear/",
        views.subject_create,
        name="subject-create",
    ),
]
