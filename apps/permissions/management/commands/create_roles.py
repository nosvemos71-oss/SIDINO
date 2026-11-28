from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import transaction

from apps.permissions.models import RoleCapability
from apps.permissions.roles import ROLE_PERMISSIONS


class Command(BaseCommand):
    help = "Crea los roles institucionales y asigna sus permisos."

    @transaction.atomic
    def handle(self, *args, **options):

        content_type = ContentType.objects.get_for_model(
            RoleCapability,
            for_concrete_model=False,
        )

        permissions = {}

        # Crear o recuperar los permisos institucionales.
        for codename, description in RoleCapability._meta.permissions:
            permission, created = Permission.objects.get_or_create(
                content_type=content_type,
                codename=codename,
                defaults={"name": description},
            )

            if not created and permission.name != description:
                permission.name = description
                permission.save(update_fields=["name"])

            permissions[codename] = permission

        # Crear los grupos y asignar sus permisos.
        for role_name, permission_codes in ROLE_PERMISSIONS.items():

            group, created = Group.objects.get_or_create(
                name=role_name
            )

            selected_permissions = [
                permissions[codename]
                for codename in permission_codes
            ]

            # add() conserva otros permisos que se hayan asignado.
            group.permissions.add(*selected_permissions)

            status = "creado" if created else "actualizado"

            self.stdout.write(
                self.style.SUCCESS(
                    f"Rol {role_name}: {status}. "
                    f"Permisos configurados: {len(selected_permissions)}"
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Configuración de roles y permisos completada."
            )
        )