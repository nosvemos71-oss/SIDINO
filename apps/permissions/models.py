from django.db import models

from django.contrib.auth.models import Group

from .roles import PERMISSION_DEFINITIONS


class RoleCapability(Group):
    """
    Modelo proxy para registrar permisos institucionales
    dentro del sistema de autorización de Django.

    No crea una tabla nueva: utiliza los grupos existentes
    de Django.
    """

    class Meta:
        proxy = True
        default_permissions = ()
        permissions = PERMISSION_DEFINITIONS
        verbose_name = "Catálogo de permisos institucionales"
        verbose_name_plural = "Catálogo de permisos institucionales"
