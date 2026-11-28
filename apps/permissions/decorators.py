from functools import wraps

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
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
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            user = request.user
            if not user.is_authenticated:
                return redirect_to_login(request.get_full_path())
            if user.has_perm(permission):
                return view_func(request, *args, **kwargs)
            if not user.groups.exists():
                return redirect_to_login(
                    request.get_full_path(), "/admin/login/"
                )
            raise PermissionDenied

        return wrapped_view

    return decorator
