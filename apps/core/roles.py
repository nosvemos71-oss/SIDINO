from functools import wraps

from django.core.exceptions import PermissionDenied


ROLE_GROUP_NAMES = {
    "rector": "Rector",
    "administrativo": "Administrativo",
    "coordinador": "Coordinador",
    "docente": "Docente",
    "estudiante": "Estudiante",
    "acudiente": "Acudiente",
}


def get_active_role(user):
    if not user.is_authenticated:
        return None

    assigned_groups = set(
        user.groups.filter(
            name__in=ROLE_GROUP_NAMES.values(),
        ).values_list("name", flat=True)
    )
    if len(assigned_groups) != 1:
        return None

    assigned_group = assigned_groups.pop()
    return next(
        role
        for role, group_name in ROLE_GROUP_NAMES.items()
        if group_name == assigned_group
    )


def role_required(role):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped(request, *args, **kwargs):
            if get_active_role(request.user) != role:
                raise PermissionDenied
            return view_func(request, *args, **kwargs)

        return wrapped

    return decorator


def any_role_required(view_func):
    @wraps(view_func)
    def wrapped(request, *args, **kwargs):
        if get_active_role(request.user) is None:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)

    return wrapped
