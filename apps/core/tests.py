from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase

from .roles import ROLE_GROUP_NAMES


class AuthenticationTests(TestCase):
    def setUp(self):
        self.username = "institution-admin"
        self.password = "A-secure-test-password-2026"
        self.user = get_user_model().objects.create_user(
            username=self.username,
            password=self.password,
        )

    def assign_role(self, role, user=None):
        group = Group.objects.get(name=ROLE_GROUP_NAMES[role])
        (user or self.user).groups.add(group)

    def test_login_page_is_public_and_has_no_registration_link(self):
        response = self.client.get("/login/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="password"')
        self.assertNotContains(response, "Crear cuenta")
        self.assertEqual(self.client.get("/register/").status_code, 404)

    def test_site_root_always_shows_login_form(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="password"')

    def test_root_still_shows_login_when_user_has_an_active_session(self):
        self.client.login(username=self.username, password=self.password)

        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="password"')

    def test_valid_credentials_log_in(self):
        response = self.client.post(
            "/",
            {"username": self.username, "password": self.password},
        )

        self.assertRedirects(response, "/inicio/", fetch_redirect_response=False)

    def test_logout_ends_session(self):
        self.client.login(username=self.username, password=self.password)

        response = self.client.post("/logout/")

        self.assertIn("no-store", response.headers["Cache-Control"])
        self.assertRedirects(response, "/login/", fetch_redirect_response=False)
        self.assertRedirects(
            self.client.get("/dashboard/rector/"),
            "/login/?next=/dashboard/rector/",
            fetch_redirect_response=False,
        )

    def test_authenticated_page_is_not_cached(self):
        self.client.login(username=self.username, password=self.password)

        response = self.client.get("/dashboard/rector/")

        self.assertIn("no-store", response.headers["Cache-Control"])

    def test_invalid_credentials_do_not_log_in(self):
        response = self.client.post(
            "/login/",
            {"username": self.username, "password": "incorrecta"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Usuario o contraseña incorrectos")

    def test_dashboard_requires_authentication(self):
        response = self.client.get("/dashboard/rector/")

        self.assertRedirects(
            response,
            "/login/?next=/dashboard/rector/",
            fetch_redirect_response=False,
        )

    def test_dashboard_redirects_to_the_assigned_role(self):
        self.assign_role("docente")
        self.client.force_login(self.user)

        response = self.client.get("/inicio/")

        self.assertRedirects(
            response,
            "/dashboard/docente/",
            fetch_redirect_response=False,
        )

    def test_dashboard_is_forbidden_without_one_active_role(self):
        self.client.force_login(self.user)
        self.assertEqual(self.client.get("/inicio/").status_code, 403)

        self.assign_role("docente")
        self.assign_role("estudiante")
        self.assertEqual(self.client.get("/inicio/").status_code, 403)

    def test_role_dashboard_shows_only_its_navigation(self):
        self.assign_role("docente")
        self.client.force_login(self.user)

        response = self.client.get("/dashboard/docente/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "/dashboard/docente/notas/")
        self.assertNotContains(response, "/dashboard/estudiante/notas/")

    def test_rector_user_management_link_is_admin_only(self):
        self.assign_role("rector")
        self.client.force_login(self.user)

        response = self.client.get("/dashboard/rector/")

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "/dashboard/rector/usuarios/")

    def test_staff_without_user_admin_permission_cannot_open_user_management(self):
        self.assign_role("rector")
        self.user.is_staff = True
        self.user.save(update_fields=["is_staff"])
        self.client.force_login(self.user)

        self.assertEqual(
            self.client.get("/dashboard/rector/usuarios/").status_code,
            403,
        )

    def test_role_cannot_open_another_roles_dashboard_or_module(self):
        self.assign_role("docente")
        self.client.force_login(self.user)

        self.assertEqual(self.client.get("/dashboard/docente/notas/").status_code, 200)
        self.assertEqual(self.client.get("/dashboard/estudiante/").status_code, 403)
        self.assertEqual(
            self.client.get("/dashboard/estudiante/notas/").status_code,
            403,
        )

    def test_each_role_can_open_only_its_own_dashboard(self):
        self.client.force_login(self.user)

        for role in ROLE_GROUP_NAMES:
            with self.subTest(role=role):
                self.user.groups.clear()
                self.assign_role(role)

                own_response = self.client.get(f"/dashboard/{role}/")
                self.assertEqual(own_response.status_code, 200)

                for other_role in ROLE_GROUP_NAMES:
                    if other_role == role:
                        continue
                    response = self.client.get(f"/dashboard/{other_role}/")
                    self.assertEqual(response.status_code, 403)

    def test_configuration_returns_only_to_the_active_role_dashboard(self):
        self.assign_role("acudiente")
        self.client.force_login(self.user)

        response = self.client.get("/dashboard/configuracion/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "/dashboard/acudiente/")
        self.assertNotContains(response, "/dashboard/docente/")

    def test_unassigned_superuser_is_sent_to_admin(self):
        admin = get_user_model().objects.create_superuser(
            username="unassigned-admin",
            password="Another-secure-test-password-2026",
        )
        self.client.force_login(admin)

        self.assertRedirects(
            self.client.get("/inicio/"),
            "/admin/",
            fetch_redirect_response=False,
        )

    def test_admin_login_is_available_without_authentication(self):
        response = self.client.get("/admin/login/")

        self.assertEqual(response.status_code, 200)

    def test_regular_user_cannot_manage_accounts(self):
        self.client.login(username=self.username, password=self.password)

        response = self.client.get("/dashboard/rector/usuarios/")

        self.assertRedirects(
            response,
            "/admin/login/?next=/dashboard/rector/usuarios/",
            fetch_redirect_response=False,
        )

    def test_admin_user_management_opens_django_admin(self):
        admin = get_user_model().objects.create_superuser(
            username="sidino-superuser",
            password="Another-secure-test-password-2026",
        )
        self.assign_role("rector", admin)
        self.client.force_login(admin)

        response = self.client.get("/dashboard/rector/usuarios/")

        self.assertRedirects(
            response,
            "/admin/auth/user/",
            fetch_redirect_response=False,
        )
