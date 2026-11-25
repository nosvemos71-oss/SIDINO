
from io import StringIO

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management import call_command
from django.db.models import ProtectedError
from django.test import TestCase, override_settings

from apps.academics.models import Area, Subject
from apps.academics.forms import SubjectForm


User = get_user_model()


@override_settings(
    ROOT_URLCONF="apps.academics.tests.urls"
)
class AcademicTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        call_command("create_roles", stdout=StringIO())

        cls.area = Area.objects.create(
            name="Ciencias Naturales",
            description="Área de ciencias.",
        )

        cls.coordinator = User.objects.create_user(
            username="coordinator_test",
            password="Test-password-123",
        )

        coordinator_group = Group.objects.get(
            name="Coordinador"
        )

        cls.coordinator.groups.add(coordinator_group)

        cls.student = User.objects.create_user(
            username="student_test",
            password="Test-password-123",
        )

        student_group = Group.objects.get(
            name="Estudiante"
        )

        cls.student.groups.add(student_group)

    def test_create_area(self):
        area = Area.objects.create(
            name="Matemáticas",
        )

        self.assertEqual(area.name, "Matemáticas")
        self.assertTrue(area.is_active)

    def test_create_subject_with_area(self):
        subject = Subject.objects.create(
            area=self.area,
            name="Biología",
            code="BIO-01",
        )

        self.assertEqual(subject.area, self.area)
        self.assertEqual(self.area.subjects.count(), 1)

    def test_subject_name_must_be_unique_in_area(self):
        Subject.objects.create(
            area=self.area,
            name="Biología",
            code="BIO-01",
        )

        form = SubjectForm(
            data={
                "area": self.area.pk,
                "name": "Biología",
                "code": "BIO-02",
                "description": "",
                "is_active": True,
            }
        )

        self.assertFalse(form.is_valid())

    def test_subject_code_must_be_unique_in_area(self):
        Subject.objects.create(
            area=self.area,
            name="Biología",
            code="BIO-01",
        )

        form = SubjectForm(
            data={
                "area": self.area.pk,
                "name": "Química",
                "code": "BIO-01",
                "description": "",
                "is_active": True,
            }
        )

        self.assertFalse(form.is_valid())

    def test_same_code_can_exist_in_different_areas(self):
        another_area = Area.objects.create(
            name="Ciencias Exactas",
        )

        Subject.objects.create(
            area=self.area,
            name="Matemáticas",
            code="MAT-01",
        )

        subject = Subject.objects.create(
            area=another_area,
            name="Matemáticas",
            code="MAT-01",
        )

        self.assertEqual(subject.code, "MAT-01")

    def test_area_cannot_be_deleted_if_it_has_subjects(self):
        Subject.objects.create(
            area=self.area,
            name="Biología",
            code="BIO-01",
        )

        with self.assertRaises(ProtectedError):
            self.area.delete()

    def test_coordinator_can_consult_areas(self):
        self.client.force_login(self.coordinator)

        response = self.client.get("/areas/")

        self.assertEqual(response.status_code, 200)

    def test_student_cannot_manage_areas(self):
        self.client.force_login(self.student)

        response = self.client.get("/areas/")

        self.assertEqual(response.status_code, 403)
        
    def test_anonymous_user_cannot_manage_areas(self):
        response = self.client.get("/areas/")
        self.assertEqual(response.status_code, 403)

    def test_coordinator_can_register_area(self):
        self.client.force_login(self.coordinator)

        response = self.client.post(
            "/areas/crear/",
            {
                "name": "Matemáticas",
                "description": "Área de matemáticas.",
                "is_active": True,
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Area.objects.filter(name="Matemáticas").exists()
        )

    def test_coordinator_can_register_subject(self):
        self.client.force_login(self.coordinator)

        response = self.client.post(
            "/asignaturas/crear/",
            {
                "area": self.area.pk,
                "name": "Biología",
                "code": "BIO-01",
                "description": "Asignatura de biología.",
                "is_active": True,
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Subject.objects.filter(
                area=self.area,
                code="BIO-01",
            ).exists()
        )
