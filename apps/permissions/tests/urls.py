from django.http import HttpResponse
from django.urls import path

from apps.permissions.decorators import (
    permission_required,
    role_required,
)


@permission_required("permissions.view_own_grades")
def protected_grades(request):
    return HttpResponse("DATO_PROTEGIDO")


@role_required("Coordinador")
def coordinator_view(request):
    return HttpResponse("AREA_COORDINACION")


urlpatterns = [
    path("protected/", protected_grades),
    path("coordinator/", coordinator_view),
]