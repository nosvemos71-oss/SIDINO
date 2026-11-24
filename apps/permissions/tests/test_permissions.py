from io import StringIO

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management import call_command
from django.test import TestCase, override_settings

from apps.permissions.roles import (
    ROLE_NAMES,
    ROLE_PERMISSIONS,
    ALL_PERMISSIONS,
)


User = get_user_model()


@override_settings(
    ROOT_URLCONF="apps.permissions.tests.urls"
)
class RolePermissionTests(TestCase):

    @classmethod
    def setUpTestData(cls):

        # Crear los grupos y permisos necesarios.
        call_command(
            "create_roles",
            stdout=StringIO(),
        )

        # Crear un usuario de prueba para cada rol.
        cls.users = {}

        for index, role in enumerate(ROLE_NAMES):

            user = User.objects.create_user(
                username=f"test_{index}",
                password="Test-password-123",
            )

            group = Group.objects.get(name=role)
            user.groups.add(group)

            cls.users[role] = user

    def test_all_six_roles_exist(self):

        groups = set(
            Group.objects.filter(
                name__in=ROLE_NAMES
            ).values_list("name", flat=True)
        )

        self.assertSetEqual(groups, set(ROLE_NAMES))

    def test_permissions_are_correctly_assigned(self):

        for role, user in self.users.items():

            expected = set(ROLE_PERMISSIONS[role])

            for codename in ALL_PERMISSIONS:

                with self.subTest(
                    role=role,
                    permission=codename,
                ):
                    self.assertEqual(
                        user.has_perm(
                            f"permissions.{codename}"
                        ),
                        codename in expected,
                    )

    def test_student_can_access_own_grades(self):

        user = self.users["Estudiante"]
        self.client.force_login(user)

        response = self.client.get("/protected/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "DATO_PROTEGIDO")
        
    def test_administrative_cannot_access_own_grades_view(self):
        user = self.users["Administrativo"]
        self.client.force_login(user)
        
        response = self.client.get("/protected/")
        
        self.assertEqual(response.status_code, 403)
        self.assertNotIn(b"DATO_PROTEGIDO", response.content)

    def test_anonymous_user_cannot_access_protected_view(self):

        response = self.client.get("/protected/")

        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_coordinator_can_access_coordinator_view(self):

        user = self.users["Coordinador"]
        self.client.force_login(user)

        response = self.client.get("/coordinator/")

        self.assertEqual(response.status_code, 200)
        
    def test_student_cannot_access_coordinator_view(self):
        user = self.users["Estudiante"]
        self.client.force_login(user)
        
        response = self.client.get("/coordinator/")
        
        self.assertEqual(response.status_code, 403)
        self.assertNotIn(b"AREA_COORDINACION", response.content)

    def test_superuser_can_access_protected_view(self):

        admin_user = User.objects.create_superuser(
            username="test_superuser",
            email="superuser@sidino.local",
            password="Test-password-123",
        )

        self.client.force_login(admin_user)

        response = self.client.get("/protected/")

        self.assertEqual(response.status_code, 200)