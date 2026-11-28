from django.urls import path

from . import views

app_name = "academics"

urlpatterns = [
    path("courses/", views.courses, name="courses"),
    path("periods/", views.periods, name="periods"),
    path("groups/", views.groups, name="groups"),
    path("students/create/", views.student_create, name="student_create"),
]
