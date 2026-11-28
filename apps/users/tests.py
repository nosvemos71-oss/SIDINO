
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.urls import reverse

from apps.permissions.roles import (
    ROLE_ADMINISTRATIVO,
    ROLE_COORDINADOR,
    ROLE_RECTOR,
)


User = get_user_model()


class InstitutionalUserTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.admin_group, _ = Group.objects.get_or_create(
            name=ROLE_ADMINISTRATIVO
        )

        cls.coordinator_group, _ = Group.objects.get_or_create(
            name=ROLE_COORDINADOR
        )

        cls.rector_group, _ = Group.objects.get_or_create(
            name=ROLE_RECTOR
        )

        content_type = ContentType.objects.get(
            app_label="permissions",
            model="rolecapability",
        )

        cls.manage_users_permission, _ = (
            Permission.objects.get_or_create(
                codename="manage_users",
                content_type=content_type,
                defaults={
                    "name": "Puede administrar usuarios institucionales"
                },
            )
        )

        cls.admin_group.permissions.add(
            cls.manage_users_permission
        )

        cls.rector_group.permissions.add(
            cls.manage_users_permission
        )

        cls.administrative_user = User.objects.create_user(
            username="administrativo_test",
            password="TestPassword123!",
            email="admin@test.com",
            first_name="Usuario",
            last_name="Administrativo",
        )

        cls.administrative_user.groups.add(cls.admin_group)

        cls.coordinator = User.objects.create_user(
            username="coordinador_test",
            password="TestPassword123!",
            email="coordinador@test.com",
        )

        cls.coordinator.groups.add(cls.coordinator_group)

        cls.target_user = User.objects.create_user(
            username="usuario_objetivo",
            password="TestPassword123!",
            email="objetivo@test.com",
        )

    def setUp(self):
        self.client.force_login(self.administrative_user)

    def test_administrative_can_view_user_list(self):
        response = self.client.get(
            reverse("users:list")
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "usuario_objetivo")

    def test_administrative_can_search_users(self):
        response = self.client.get(
            reverse("users:list"),
            {"q": "objetivo"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "usuario_objetivo")

    def test_administrative_can_create_user(self):
        response = self.client.post(
            reverse("users:create"),
            {
                "username": "nuevo_usuario",
                "first_name": "Nuevo",
                "last_name": "Usuario",
                "email": "nuevo@test.com",
                "role": ROLE_COORDINADOR,
                "password1": "AnotherStrongPassword123!",
                "password2": "AnotherStrongPassword123!",
            },
        )

        self.assertEqual(response.status_code, 302)

        created_user = User.objects.get(
            username="nuevo_usuario"
        )

        self.assertTrue(
            created_user.check_password(
                "AnotherStrongPassword123!"
            )
        )

        self.assertTrue(
            created_user.groups.filter(
                name=ROLE_COORDINADOR
            ).exists()
        )

    def test_creation_rejects_duplicate_username(self):
        response = self.client.post(
            reverse("users:create"),
            {
                "username": "usuario_objetivo",
                "first_name": "Nuevo",
                "last_name": "Usuario",
                "email": "otro@test.com",
                "role": ROLE_COORDINADOR,
                "password1": "AnotherStrongPassword123!",
                "password2": "AnotherStrongPassword123!",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "nombre de usuario ya está registrado",
        )

    def test_creation_rejects_duplicate_email(self):
        response = self.client.post(
            reverse("users:create"),
            {
                "username": "otro_usuario",
                "first_name": "Nuevo",
                "last_name": "Usuario",
                "email": "objetivo@test.com",
                "role": ROLE_COORDINADOR,
                "password1": "AnotherStrongPassword123!",
                "password2": "AnotherStrongPassword123!",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "correo electrónico ya está registrado",
        )

    def test_creation_rejects_different_passwords(self):
        response = self.client.post(
            reverse("users:create"),
            {
                "username": "otro_usuario",
                "first_name": "Nuevo",
                "last_name": "Usuario",
                "email": "otro@test.com",
                "role": ROLE_COORDINADOR,
                "password1": "AnotherStrongPassword123!",
                "password2": "DifferentPassword123!",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            User.objects.filter(
                username="otro_usuario"
            ).exists()
        )

    def test_administrative_can_update_user(self):
        response = self.client.post(
            reverse(
                "users:update",
                args=[self.target_user.pk],
            ),
            {
                "username": "usuario_objetivo",
                "first_name": "Nombre actualizado",
                "last_name": "Apellido actualizado",
                "email": "actualizado@test.com",
                "role": ROLE_COORDINADOR,
            },
        )

        self.assertEqual(response.status_code, 302)

        self.target_user.refresh_from_db()

        self.assertEqual(
            self.target_user.first_name,
            "Nombre actualizado",
        )

        self.assertEqual(
            self.target_user.email,
            "actualizado@test.com",
        )

    def test_administrative_can_deactivate_user(self):
        response = self.client.post(
            reverse(
                "users:toggle_active",
                args=[self.target_user.pk],
            )
        )

        self.assertEqual(response.status_code, 302)

        self.target_user.refresh_from_db()

        self.assertFalse(self.target_user.is_active)

        self.assertTrue(
            User.objects.filter(
                pk=self.target_user.pk
            ).exists()
        )

    def test_administrative_can_reactivate_user(self):
        self.target_user.is_active = False
        self.target_user.save()

        response = self.client.post(
            reverse(
                "users:toggle_active",
                args=[self.target_user.pk],
            )
        )

        self.assertEqual(response.status_code, 302)

        self.target_user.refresh_from_db()

        self.assertTrue(self.target_user.is_active)

    def test_user_cannot_deactivate_own_account(self):
        response = self.client.post(
            reverse(
                "users:toggle_active",
                args=[self.administrative_user.pk],
            )
        )

        self.assertEqual(response.status_code, 302)

        self.administrative_user.refresh_from_db()

        self.assertTrue(self.administrative_user.is_active)

    def test_coordinator_cannot_manage_users(self):
        self.client.force_login(self.coordinator)

        response = self.client.get(
            reverse("users:list")
        )

        self.assertEqual(response.status_code, 403)

    def test_user_without_permission_cannot_create_users(self):
        self.client.force_login(self.coordinator)

        response = self.client.get(
            reverse("users:create")
        )

        self.assertEqual(response.status_code, 403)

    def test_user_without_permission_cannot_update_users(self):
        self.client.force_login(self.coordinator)

        response = self.client.get(
            reverse(
                "users:update",
                args=[self.target_user.pk],
            )
        )

        self.assertEqual(response.status_code, 403)

    def test_user_without_permission_cannot_deactivate_users(self):
        self.client.force_login(self.coordinator)

        response = self.client.post(
            reverse(
                "users:toggle_active",
                args=[self.target_user.pk],
            )
        )

        self.assertEqual(response.status_code, 403)

    def test_deactivated_user_cannot_login(self):
        self.target_user.is_active = False
        self.target_user.save()

        self.client.logout()

        login_successful = self.client.login(
            username="usuario_objetivo",
            password="TestPassword123!",
        )

        self.assertFalse(login_successful)
