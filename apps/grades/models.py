from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.academics.models import GroupEnrollment


class Grade(models.Model):
    """A single assessment grade belonging to one student-period enrollment."""

    enrollment = models.ForeignKey(
        GroupEnrollment,
        on_delete=models.PROTECT,
        related_name="grades",
        verbose_name="inscripción",
    )
    name = models.CharField("evaluación", max_length=100)
    value = models.DecimalField(
        "calificación",
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00")), MaxValueValidator(Decimal("5.00"))],
    )
    is_valid = models.BooleanField("calificación válida", default=True)
    created_at = models.DateTimeField("fecha de registro", auto_now_add=True)

    class Meta:
        verbose_name = "calificación"
        verbose_name_plural = "calificaciones"
        ordering = ("enrollment", "name")
        constraints = [
            models.UniqueConstraint(
                fields=("enrollment", "name"),
                name="grades_unique_assessment_per_enrollment",
            ),
        ]

    def __str__(self):
        return f"{self.enrollment} — {self.name}: {self.value}"

