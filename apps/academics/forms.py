from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password

from .models import AcademicGroup, AcademicPeriod, Course, GroupEnrollment

User = get_user_model()


class StudentCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")
        labels = {
            "username": "Nombre de usuario",
            "first_name": "Nombres",
            "last_name": "Apellidos",
            "email": "Correo electrónico",
        }

    def clean_username(self):
        username = self.cleaned_data["username"].strip()
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya está registrado.")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está registrado.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            self.add_error("password2", "Las contraseñas no coinciden.")
        if password1:
            try:
                validate_password(password1, self.instance)
            except forms.ValidationError as error:
                self.add_error("password1", error)
        return cleaned_data

    def save(self, commit=True):
        student = super().save(commit=False)
        student.set_password(self.cleaned_data["password1"])
        if commit:
            student.save()
            student.groups.set([Group.objects.get_or_create(name="Estudiante")[0]])
        return student


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ("name",)


class AcademicPeriodForm(forms.ModelForm):
    class Meta:
        model = AcademicPeriod
        fields = ("name", "start_date", "end_date")
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }


class AcademicGroupForm(forms.ModelForm):
    class Meta:
        model = AcademicGroup
        fields = ("course", "period", "name")


class GroupEnrollmentForm(forms.ModelForm):
    class Meta:
        model = GroupEnrollment
        fields = ("student",)

    def __init__(self, *args, period=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["student"].queryset = User.objects.filter(
            is_active=True,
            groups__name="Estudiante",
        ).order_by("last_name", "first_name", "username").distinct()
        self.period = period

    def clean_student(self):
        student = self.cleaned_data["student"]
        if self.period and GroupEnrollment.objects.filter(
            student=student, period=self.period
        ).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(
                "El estudiante ya pertenece a un grupo en este periodo."
            )
        return student

    def save(self, commit=True):
        enrollment = super().save(commit=False)
        if self.period:
            enrollment.period = self.period
        if commit:
            enrollment.save()
        return enrollment
