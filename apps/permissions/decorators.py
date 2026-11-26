from functools import wraps

from django.contrib.auth.decorators import (
    login_required,
    permission_required as django_permission_required,
)
from django.core.exceptions import PermissionDenied


def role_required(*roles):
    """
    Permite acceder únicamente a usuarios autenticados
    que pertenezcan a alguno de los grupos indicados.
    """

    if not roles:
        raise ValueError("Debes indicar al menos un rol.")

    def decorator(view_func):

        @wraps(view_func)
        @login_required
        def wrapped_view(request, *args, **kwargs):

            user = request.user

            if user.is_superuser:
                return view_func(request, *args, **kwargs)

            has_role = user.groups.filter(
                name__in=roles
            ).exists()

            if not has_role:
                raise PermissionDenied

            return view_func(request, *args, **kwargs)

        return wrapped_view

    return decorator


def permission_required(permission):
    """
    Protege una vista mediante un permiso específico de Django.

    Los usuarios no autenticados son redirigidos al login.
    Los usuarios autenticados sin permiso reciben un 403.
    """

    def decorator(view_func):

        protected_view = django_permission_required(
            permission,
            raise_exception=True,
        )(view_func)

        return login_required(protected_view)

    return decorator