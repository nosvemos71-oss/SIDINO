"""Control de acceso por rol de SIDINO.

CONTRATO CON EL LOGIN (lo implementa el otro desarrollador):
    al autenticar correctamente basta con hacer
        request.session[SESSION_KEY] = usuario.id_usuario
    y al cerrar sesión: request.session.flush().
Todo lo demás (qué dashboard ver, qué URLs abrir) se resuelve aquí.
"""
from functools import wraps

from django.conf import settings
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

from .models import Usuario

SESSION_KEY = "usuario_id"

# slug -> (nombre visible, descripción corta)
ROLE_LABELS = {
    "rector": ("Rectoría", "Dirección institucional"),
    "coordinador": ("Coordinación", "Coordinación académica"),
    "administrativo": ("Administrativo", "Gestión administrativa"),
    "docente": ("Docente", "Área de enseñanza"),
    "estudiante": ("Estudiante", "Portal estudiantil"),
    "acudiente": ("Acudiente", "Seguimiento familiar"),
}


def get_usuario(request):
    """Usuario de la sesión (o None). Se consulta una sola vez por petición."""
    if not hasattr(request, "_sidino_usuario"):
        usuario = None
        uid = request.session.get(SESSION_KEY)
        if uid:
            usuario = Usuario.objects.select_related("rol").filter(pk=uid).first()
            if usuario is None:  # sesión apunta a un usuario que ya no existe
                request.session.flush()
        request._sidino_usuario = usuario
    return request._sidino_usuario


def dashboard_name(slug):
    return f"dashboard_{slug}"


def role_required(*allowed, kwarg=None):
    """Protege una vista.

    @role_required("docente")        -> solo docentes
    @role_required("rector", "coordinador")
    @role_required()                 -> cualquier usuario autenticado
    @role_required(kwarg="role")     -> el rol permitido viene en la URL (panel_module)

    Sin sesión -> redirige al login. Con otro rol -> 403.
    """

    def decorator(view):
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            usuario = get_usuario(request)
            if usuario is None:
                return redirect_to_login(request.get_full_path(), settings.LOGIN_URL)
            permitidos = {kwargs[kwarg]} if kwarg else set(allowed)
            if permitidos and usuario.slug not in permitidos:
                raise PermissionDenied
            return view(request, *args, **kwargs)

        return wrapper

    return decorator


def redirect_to_own_dashboard(request):
    usuario = get_usuario(request)
    if usuario is None:
        return redirect_to_login(request.get_full_path(), settings.LOGIN_URL)
    if usuario.slug not in ROLE_LABELS:
        raise PermissionDenied
    return redirect(dashboard_name(usuario.slug))
