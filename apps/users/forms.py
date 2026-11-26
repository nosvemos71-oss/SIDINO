
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from apps.permissions.roles import ROLE_NAMES


User = get_user_model()


class InstitutionalUserForm(forms.ModelForm):
    role = forms.ChoiceField(
        choices=[(role, role) for role in ROLE_NAMES],
        label="Rol institucional",
    )

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
        ]
        labels = {
            "username": "Nombre de usuario",
            "first_name": "Nombres",
            "last_name": "Apellidos",
            "email": "Correo electrónico",
        }
        widgets = {
            "username": forms.TextInput(
                attrs={"placeholder": "Nombre de usuario"}
            ),
            "first_name": forms.TextInput(
                attrs={"placeholder": "Nombres"}
            ),
            "last_name": forms.TextInput(
                attrs={"placeholder": "Apellidos"}
            ),
            "email": forms.EmailInput(
                attrs={"placeholder": "correo@institucion.edu.co"}
            ),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

        for field in ("username", "first_name", "last_name", "email"):
            self.fields[field].required = True

        if self.instance and self.instance.pk:
            current_roles = self.instance.groups.filter(
                name__in=ROLE_NAMES
            ).values_list("name", flat=True)

            self.fields["role"].initial = next(
                iter(current_roles),
                "",
            )

            # Evita que un administrador cambie accidentalmente
            # su propio rol y pierda el acceso a la administración.
            if (
                self.request
                and self.request.user.pk == self.instance.pk
            ):
                self.fields["role"].disabled = True

    def clean_username(self):
        username = self.cleaned_data["username"].strip()

        existing = User.objects.filter(
            username__iexact=username
        )

        if self.instance and self.instance.pk:
            existing = existing.exclude(pk=self.instance.pk)

        if existing.exists():
            raise forms.ValidationError(
                "Este nombre de usuario ya está registrado."
            )

        return username

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()

        existing = User.objects.filter(email__iexact=email)

        if self.instance and self.instance.pk:
            existing = existing.exclude(pk=self.instance.pk)

        if existing.exists():
            raise forms.ValidationError(
                "Este correo electrónico ya está registrado."
            )

        return email

    def clean_first_name(self):
        value = self.cleaned_data["first_name"].strip()

        if not value:
            raise forms.ValidationError(
                "Los nombres son obligatorios."
            )

        return value

    def clean_last_name(self):
        value = self.cleaned_data["last_name"].strip()

        if not value:
            raise forms.ValidationError(
                "Los apellidos son obligatorios."
            )

        return value

    def save(self, commit=True):
        user = super().save(commit=False)

        if commit:
            user.save()

            selected_role = self.cleaned_data["role"]

            if selected_role:
                group, _ = Group.objects.get_or_create(
                    name=selected_role
                )

                # Cada cuenta tendrá un único rol institucional.
                user.groups.remove(
                    *user.groups.filter(
                        name__in=ROLE_NAMES
                    )
                )
                user.groups.add(group)

        return user


class InstitutionalUserCreationForm(InstitutionalUserForm):
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput,
        strip=False,
    )

    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput,
        strip=False,
    )

    class Meta(InstitutionalUserForm.Meta):
        fields = InstitutionalUserForm.Meta.fields + [
            "password1",
            "password2",
        ]

    def clean(self):
        cleaned_data = super().clean()

        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error(
                "password2",
                "Las contraseñas no coinciden.",
            )

        if password1:
            from django.contrib.auth.password_validation import (
                validate_password,
            )

            try:
                validate_password(password1)
            except forms.ValidationError as error:
                self.add_error("password1", error)

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()

            selected_role = self.cleaned_data["role"]
            group, _ = Group.objects.get_or_create(
                name=selected_role
            )
            user.groups.add(group)

        return user
