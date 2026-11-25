
from django import forms

from .models import Area, Subject


class AreaForm(forms.ModelForm):

    class Meta:
        model = Area
        fields = [
            "name",
            "description",
            "is_active",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                }
            ),
        }

    def clean_name(self):
        name = self.cleaned_data["name"].strip()

        if not name:
            raise forms.ValidationError(
                "El nombre del área es obligatorio."
            )

        return name


class SubjectForm(forms.ModelForm):

    class Meta:
        model = Subject
        fields = [
            "area",
            "name",
            "code",
            "description",
            "is_active",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "code": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["area"].queryset = Area.objects.filter(
            is_active=True
        )

    def clean_name(self):
        name = self.cleaned_data["name"].strip()

        if not name:
            raise forms.ValidationError(
                "El nombre de la asignatura es obligatorio."
            )

        return name

    def clean_code(self):
        code = self.cleaned_data["code"].strip().upper()

        if not code:
            raise forms.ValidationError(
                "La clave de la asignatura es obligatoria."
            )

        return code
