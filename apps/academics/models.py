from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F, Q


class AcademicPeriod(models.Model):
    name = models.CharField("periodo", max_length=80, unique=True)
    start_date = models.DateField("fecha de inicio")
    end_date = models.DateField("fecha de cierre")

    class Meta:
        ordering = ("-start_date", "name")
        constraints = [
            models.CheckConstraint(
                condition=Q(end_date__gte=F("start_date")),
                name="academics_period_dates_valid",
            ),
        ]

    def clean(self):
        super().clean()
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValidationError({"end_date": "La fecha de cierre debe ser posterior al inicio."})

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField("curso o grado", max_length=80, unique=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


class AcademicGroup(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.PROTECT, related_name="groups", verbose_name="curso"
    )
    period = models.ForeignKey(
        AcademicPeriod, on_delete=models.PROTECT, related_name="groups", verbose_name="periodo"
    )
    name = models.CharField("grupo o sección", max_length=30)
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="GroupEnrollment",
        related_name="academic_groups",
        blank=True,
    )

    class Meta:
        ordering = ("period", "course", "name")
        constraints = [
            models.UniqueConstraint(
                fields=("course", "period", "name"),
                name="academics_unique_group_per_course_period",
            ),
        ]

    def __str__(self):
        return f"{self.course} {self.name} — {self.period}"


class GroupEnrollment(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="group_enrollments"
    )
    group = models.ForeignKey(
        AcademicGroup, on_delete=models.PROTECT, related_name="enrollments"
    )
    period = models.ForeignKey(AcademicPeriod, on_delete=models.PROTECT, editable=False)
    enrolled_at = models.DateTimeField("fecha de inscripción", auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("student", "group"), name="academics_unique_student_group"
            ),
            models.UniqueConstraint(
                fields=("student", "period"), name="academics_unique_student_period"
            ),
        ]

    def clean(self):
        super().clean()
        if self.student_id and not self.student.groups.filter(name="Estudiante").exists():
            raise ValidationError({"student": "Solo se pueden inscribir usuarios con rol Estudiante."})
        if self.group_id and self.period_id != self.group.period_id:
            raise ValidationError({"group": "El periodo de inscripción debe coincidir con el del grupo."})

    def save(self, *args, **kwargs):
        if self.group_id:
            self.period_id = self.group.period_id
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student} — {self.group}"
