from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    AcademicGroupForm,
    AcademicPeriodForm,
    CourseForm,
    GroupEnrollmentForm,
    StudentCreationForm,
)
from .models import AcademicGroup, AcademicPeriod, Course


@permission_required("permissions.manage_courses", raise_exception=True)
def courses(request):
    form = CourseForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Curso creado correctamente.")
        return redirect("academics:courses")
    return render(request, "academics/courses.html", {
        "form": form,
        "courses": Course.objects.prefetch_related("groups"),
    })


@permission_required("permissions.manage_courses", raise_exception=True)
def periods(request):
    form = AcademicPeriodForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Periodo creado correctamente.")
        return redirect("academics:periods")
    return render(request, "academics/periods.html", {
        "form": form,
        "periods": AcademicPeriod.objects.all(),
    })


@permission_required("permissions.manage_courses", raise_exception=True)
def groups(request):
    group_form = AcademicGroupForm()
    enrollment_form = None
    if request.method == "POST" and request.POST.get("action") == "create_group":
        group_form = AcademicGroupForm(request.POST)
        if group_form.is_valid():
            group_form.save()
            messages.success(request, "Grupo creado correctamente.")
            return redirect("academics:groups")
    elif request.method == "POST" and request.POST.get("action") == "enroll":
        group = get_object_or_404(AcademicGroup, pk=request.POST.get("group_id"))
        enrollment_form = GroupEnrollmentForm(request.POST, period=group.period)
        if enrollment_form.is_valid():
            enrollment = enrollment_form.save(commit=False)
            enrollment.group = group
            enrollment.save()
            messages.success(request, "Estudiante inscrito en el grupo.")
            return redirect("academics:groups")

    group_rows = []
    for group in AcademicGroup.objects.select_related("course", "period").prefetch_related(
        "enrollments__student"
    ):
        group_rows.append({
            "group": group,
            "enrollment_form": (
                enrollment_form
                if enrollment_form is not None and str(group.pk) == request.POST.get("group_id")
                else GroupEnrollmentForm(period=group.period)
            ),
        })

    return render(request, "academics/groups.html", {
        "group_form": group_form,
        "group_rows": group_rows,
        "courses": Course.objects.all(),
        "periods": AcademicPeriod.objects.all(),
        "enrollment_form": enrollment_form,
    })


@permission_required("permissions.manage_students", raise_exception=True)
def student_create(request):
    form = StudentCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Estudiante creado correctamente.")
        return redirect("academics:student_create")
    return render(request, "academics/student_create.html", {"form": form})
