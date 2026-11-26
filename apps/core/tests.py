
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase


class AuthenticationTests(TestCase):
    def setUp(self):
        self.username = "institution-admin"
        self.password = "A-secure-test-password-2026"

        self.user = get_user_model().objects.create_user(
            username=self.username,
            password=self.password,
        )

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

    def test_admin_login_is_available_without_authentication(self):
        response = self.client.get("/admin/login/")

        self.assertEqual(response.status_code, 200)

    def test_regular_user_cannot_manage_accounts(self):
        self.client.force_login(self.user)

        response = self.client.get("/dashboard/rector/usuarios/")

        self.assertEqual(response.status_code, 403)

    def test_admin_user_management_opens_django_admin(self):
        rector_group, _ = Group.objects.get_or_create(name="Rector")
        self.user.groups.add(rector_group)

        self.client.force_login(self.user)

        response = self.client.get("/dashboard/rector/usuarios/")

        self.assertRedirects(
            response,
            "/usuarios/",
            fetch_redirect_response=False,
        )
