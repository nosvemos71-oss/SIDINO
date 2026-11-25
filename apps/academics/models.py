
from django.db import models


class Area(models.Model):
    name = models.CharField(
        max_length=120,
        unique=True,
        verbose_name="Nombre",
    )

    description = models.TextField(
        blank=True,
        verbose_name="Descripción",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Activa",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha de actualización",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Área"
        verbose_name_plural = "Áreas"

    def __str__(self):
        return self.name


class Subject(models.Model):
    area = models.ForeignKey(
        Area,
        on_delete=models.PROTECT,
        related_name="subjects",
        verbose_name="Área",
    )

    name = models.CharField(
        max_length=120,
        verbose_name="Nombre",
    )

    code = models.CharField(
        max_length=30,
        verbose_name="Clave",
    )

    description = models.TextField(
        blank=True,
        verbose_name="Descripción",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Activa",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha de actualización",
    )

    class Meta:
        ordering = ["area__name", "name"]
        verbose_name = "Asignatura"
        verbose_name_plural = "Asignaturas"

        constraints = [
            models.UniqueConstraint(
                fields=["area", "name"],
                name="uniq_subject_name_per_area",
            ),
            models.UniqueConstraint(
                fields=["area", "code"],
                name="uniq_subject_code_per_area",
            ),
        ]

    def __str__(self):
        return f"{self.name} ({self.area.name})"
