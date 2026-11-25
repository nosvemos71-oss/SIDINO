
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import Area, Subject
from .forms import AreaForm, SubjectForm


@permission_required(
    "permissions.manage_subjects",
    raise_exception=True,
)
def area_list(request):
    areas = Area.objects.all()

    return render(
        request,
        "academics/area_list.html",
        {"areas": areas},
    )


@permission_required(
    "permissions.manage_subjects",
    raise_exception=True,
)
def area_create(request):
    if request.method == "POST":
        form = AreaForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("academics:area-list")
    else:
        form = AreaForm()

    return render(
        request,
        "academics/area_form.html",
        {"form": form},
    )


@permission_required(
    "permissions.manage_subjects",
    raise_exception=True,
)
def area_detail(request, pk):
    area = get_object_or_404(Area, pk=pk)

    subjects = area.subjects.all()

    return render(
        request,
        "academics/area_detail.html",
        {
            "area": area,
            "subjects": subjects,
        },
    )


@permission_required(
    "permissions.manage_subjects",
    raise_exception=True,
)
def subject_list(request):
    subjects = Subject.objects.select_related("area").all()

    return render(
        request,
        "academics/subject_list.html",
        {"subjects": subjects},
    )


@permission_required(
    "permissions.manage_subjects",
    raise_exception=True,
)
def subject_create(request):
    if request.method == "POST":
        form = SubjectForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("academics:subject-list")
    else:
        form = SubjectForm()

    return render(
        request,
        "academics/subject_form.html",
        {"form": form},
    )
