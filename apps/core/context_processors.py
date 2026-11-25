from django.urls import reverse

from .access import ROLE_LABELS, dashboard_name, get_usuario


def sidino_user(request):
    """Expone en TODAS las plantillas: usuario, rol_nombre, rol_descripcion, dashboard_url."""
    usuario = get_usuario(request)
    if usuario is None or usuario.slug not in ROLE_LABELS:
        return {"usuario": usuario}
    nombre, descripcion = ROLE_LABELS[usuario.slug]
    return {
        "usuario": usuario,
        "rol_nombre": nombre,
        "rol_descripcion": descripcion,
        "dashboard_url": reverse(dashboard_name(usuario.slug)),
    }
