from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from apps.permissions.decorators import permission_required

from .forms import (
    InstitutionalUserCreationForm,
    InstitutionalUserForm,
)


User = get_user_model()


@permission_required("permissions.manage_users")
def user_list(request):
    if request.user.is_superuser:
        return redirect(reverse("admin:auth_user_changelist"))

    search = request.GET.get("q", "").strip()

    users = User.objects.prefetch_related("groups").order_by(
        "last_name",
        "first_name",
    )

    if search:
        users = users.filter(
            username__icontains=search
        ) | users.filter(
            first_name__icontains=search
        ) | users.filter(
            last_name__icontains=search
        ) | users.filter(
            email__icontains=search
        )

    paginator = Paginator(users.distinct(), 10)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "users/user_list.html",
        {
            "page_obj": page_obj,
            "search": search,
        },
    )


@permission_required("permissions.manage_users")
def user_detail(request, pk):
    institutional_user = get_object_or_404(
        User.objects.prefetch_related("groups"),
        pk=pk,
    )

    return render(
        request,
        "users/user_detail.html",
        {
            "institutional_user": institutional_user,
        },
    )


@permission_required("permissions.manage_users")
def user_create(request):
    if request.method == "POST":
        form = InstitutionalUserCreationForm(
            request.POST,
            request=request,
        )

        if form.is_valid():
            institutional_user = form.save()

            messages.success(
                request,
                "El usuario institucional fue creado correctamente.",
            )

            return redirect(
                "users:detail",
                pk=institutional_user.pk,
            )
    else:
        form = InstitutionalUserCreationForm(request=request)

    return render(
        request,
        "users/user_form.html",
        {
            "form": form,
            "title": "Crear usuario institucional",
            "is_creation": True,
        },
    )


@permission_required("permissions.manage_users")
def user_update(request, pk):
    institutional_user = get_object_or_404(User, pk=pk)

    if request.method == "POST":
        form = InstitutionalUserForm(
            request.POST,
            instance=institutional_user,
            request=request,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Los datos del usuario fueron actualizados.",
            )

            return redirect(
                "users:detail",
                pk=institutional_user.pk,
            )
    else:
        form = InstitutionalUserForm(
            instance=institutional_user,
            request=request,
        )

    return render(
        request,
        "users/user_form.html",
        {
            "form": form,
            "title": "Actualizar usuario institucional",
            "is_creation": False,
            "institutional_user": institutional_user,
        },
    )


@permission_required("permissions.manage_users")
def user_toggle_active(request, pk):
    institutional_user = get_object_or_404(User, pk=pk)

    if request.method == "POST":
        if institutional_user.pk == request.user.pk:
            messages.error(
                request,
                "No puedes desactivar tu propia cuenta.",
            )
            return redirect(
                "users:detail",
                pk=institutional_user.pk,
            )

        institutional_user.is_active = (
            not institutional_user.is_active
        )
        institutional_user.save(update_fields=["is_active"])

        if institutional_user.is_active:
            messages.success(
                request,
                "La cuenta fue activada correctamente.",
            )
        else:
            messages.success(
                request,
                "La cuenta fue desactivada correctamente.",
            )

        return redirect(
            "users:detail",
            pk=institutional_user.pk,
        )

    return render(
        request,
        "users/user_confirm_toggle.html",
        {
            "institutional_user": institutional_user,
        },
    )
