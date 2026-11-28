from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.db.models import F, Q


class Migration(migrations.Migration):
    initial = True

    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]

    operations = [
        migrations.CreateModel(
            name="AcademicPeriod",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=80, unique=True, verbose_name="periodo")),
                ("start_date", models.DateField(verbose_name="fecha de inicio")),
                ("end_date", models.DateField(verbose_name="fecha de cierre")),
            ],
            options={"ordering": ("-start_date", "name")},
        ),
        migrations.CreateModel(
            name="Course",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=80, unique=True, verbose_name="curso o grado")),
            ],
            options={"ordering": ("name",)},
        ),
        migrations.CreateModel(
            name="AcademicGroup",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=30, verbose_name="grupo o sección")),
                ("course", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="groups", to="academics.course", verbose_name="curso")),
                ("period", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="groups", to="academics.academicperiod", verbose_name="periodo")),
            ],
            options={"ordering": ("period", "course", "name")},
        ),
        migrations.CreateModel(
            name="GroupEnrollment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("enrolled_at", models.DateTimeField(auto_now_add=True, verbose_name="fecha de inscripción")),
                ("period", models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, to="academics.academicperiod")),
                ("group", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="enrollments", to="academics.academicgroup")),
                ("student", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="group_enrollments", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name="academicgroup",
            name="students",
            field=models.ManyToManyField(blank=True, related_name="academic_groups", through="academics.GroupEnrollment", to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name="academicperiod",
            constraint=models.CheckConstraint(condition=Q(("end_date__gte", F("start_date"))), name="academics_period_dates_valid"),
        ),
        migrations.AddConstraint(
            model_name="academicgroup",
            constraint=models.UniqueConstraint(fields=("course", "period", "name"), name="academics_unique_group_per_course_period"),
        ),
        migrations.AddConstraint(
            model_name="groupenrollment",
            constraint=models.UniqueConstraint(fields=("student", "group"), name="academics_unique_student_group"),
        ),
        migrations.AddConstraint(
            model_name="groupenrollment",
            constraint=models.UniqueConstraint(fields=("student", "period"), name="academics_unique_student_period"),
        ),
    ]
