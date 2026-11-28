from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from .forms import AcademicGroupForm, AcademicPeriodForm, GroupEnrollmentForm
from .models import AcademicGroup, AcademicPeriod, Course, GroupEnrollment


User = get_user_model()


class AcademicStructureTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("create_roles", verbosity=0)
        cls.coordinator_group = Group.objects.get(name="Coordinador")
        cls.student_group = Group.objects.get(name="Estudiante")
        cls.coordinator = User.objects.create_user("coordinator", password="test-pass-123")
        cls.coordinator.groups.add(cls.coordinator_group)
        cls.student = User.objects.create_user("student", password="test-pass-123")
        cls.student.groups.add(cls.student_group)
        cls.other_user = User.objects.create_user("other", password="test-pass-123")
        cls.course = Course.objects.create(name="Sexto")
        cls.period = AcademicPeriod.objects.create(
            name="2026", start_date=date(2026, 1, 20), end_date=date(2026, 11, 30)
        )

    def test_group_requires_course_and_period(self):
        form = AcademicGroupForm(data={"course": "", "period": "", "name": "A"})
        self.assertFalse(form.is_valid())
        self.assertIn("course", form.errors)
        self.assertIn("period", form.errors)

    def test_duplicate_group_for_same_course_period_is_rejected(self):
        AcademicGroup.objects.create(course=self.course, period=self.period, name="A")
        form = AcademicGroupForm(data={
            "course": self.course.pk, "period": self.period.pk, "name": "A"
        })
        self.assertFalse(form.is_valid())
        self.assertIn("__all__", form.errors)

    def test_period_dates_are_validated(self):
        form = AcademicPeriodForm(data={
            "name": "2027", "start_date": "2027-12-01", "end_date": "2027-01-01"
        })
        self.assertFalse(form.is_valid())
        self.assertIn("end_date", form.errors)

    def test_only_student_role_can_be_enrolled(self):
        group = AcademicGroup.objects.create(course=self.course, period=self.period, name="B")
        form = GroupEnrollmentForm(
            data={"student": self.other_user.pk}, period=self.period
        )
        self.assertFalse(form.is_valid())
        self.assertNotIn(self.other_user, form.fields["student"].queryset)
        enrollment = GroupEnrollment(student=self.other_user, group=group)
        with self.assertRaises(ValidationError):
            enrollment.save()

    def test_student_can_only_belong_to_one_group_in_each_period(self):
        first = AcademicGroup.objects.create(course=self.course, period=self.period, name="C")
        second = AcademicGroup.objects.create(course=self.course, period=self.period, name="D")
        GroupEnrollment.objects.create(student=self.student, group=first)
        form = GroupEnrollmentForm(data={"student": self.student.pk}, period=self.period)
        self.assertFalse(form.is_valid())

    def test_coordinator_can_create_course_and_student_cannot_change_structure(self):
        self.client.force_login(self.coordinator)
        response = self.client.post(reverse("academics:courses"), {"name": "Séptimo"})
        self.assertRedirects(response, reverse("academics:courses"))
        self.assertTrue(Course.objects.filter(name="Séptimo").exists())

        self.client.force_login(self.student)
        denied = self.client.post(reverse("academics:courses"), {"name": "Octavo"})
        self.assertEqual(denied.status_code, 403)
        self.assertFalse(Course.objects.filter(name="Octavo").exists())

    def test_coordinator_can_access_course_period_and_group_management(self):
        self.client.force_login(self.coordinator)

        for route_name in ("academics:courses", "academics:periods", "academics:groups"):
            with self.subTest(route_name=route_name):
                self.assertEqual(self.client.get(reverse(route_name)).status_code, 200)

    def test_coordinator_can_create_student_with_student_role(self):
        self.client.force_login(self.coordinator)
        response = self.client.post(reverse("academics:student_create"), {
            "username": "new_student",
            "first_name": "New",
            "last_name": "Student",
            "email": "new.student@test.com",
            "password1": "StrongStudentPassword123!",
            "password2": "StrongStudentPassword123!",
        })

        self.assertRedirects(response, reverse("academics:student_create"))
        student = User.objects.get(username="new_student")
        self.assertTrue(student.check_password("StrongStudentPassword123!"))
        self.assertTrue(student.groups.filter(name="Estudiante").exists())

    def test_student_cannot_create_students(self):
        self.client.force_login(self.student)

        response = self.client.get(reverse("academics:student_create"))

        self.assertEqual(response.status_code, 403)

    def test_coordinator_can_create_group_and_enroll_student(self):
        self.client.force_login(self.coordinator)
        response = self.client.post(reverse("academics:groups"), {
            "action": "create_group",
            "course": self.course.pk,
            "period": self.period.pk,
            "name": "A",
        })
        self.assertRedirects(response, reverse("academics:groups"))
        group = AcademicGroup.objects.get(course=self.course, period=self.period, name="A")

        page = self.client.get(reverse("academics:groups"))
        self.assertEqual(page.status_code, 200)
        self.assertContains(page, "Sexto")

        response = self.client.post(reverse("academics:groups"), {
            "action": "enroll", "group_id": group.pk, "student": self.student.pk,
        })
        self.assertRedirects(response, reverse("academics:groups"))
        self.assertTrue(GroupEnrollment.objects.filter(student=self.student, group=group).exists())
