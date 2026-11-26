
from django.urls import path
from . import views

urlpatterns = [
    # Dashboard principal
    path("inicio/", views.dashboard, name="dashboard"),

    # Dashboards de roles
    path(
    "dashboard/rector/",
    views.dashboard_rector,
    name="dashboard_rector",
    ),
    path(
        "dashboard/administrativo/",
        views.dashboard_administrativo,
        name="dashboard_administrativo",
    ),
    path(
        "dashboard/coordinador/",
        views.dashboard_coordinador,
        name="dashboard_coordinador",
    ),
    path(
        "dashboard/docente/",
        views.dashboard_docente,
        name="dashboard_docente",
    ),
    path(
        "dashboard/estudiante/",
        views.dashboard_estudiante,
        name="dashboard_estudiante",
    ),
    path(
        "dashboard/acudiente/",
        views.dashboard_acudiente,
        name="dashboard_acudiente",
    ),

    # Módulos del Rector
    path(
        "dashboard/rector/materias/",
        views.rector_materias,
        name="rector_materias",
    ),
    path(
        "dashboard/rector/cursos/",
        views.rector_cursos,
        name="rector_cursos",
    ),
    path(
        "dashboard/rector/salones/",
        views.rector_salones,
        name="rector_salones",
    ),
    path(
        "dashboard/rector/horarios/",
        views.rector_horarios,
        name="rector_horarios",
    ),
    path(
        "dashboard/rector/periodos/",
        views.rector_periodos,
        name="rector_periodos",
    ),
    path(
        "dashboard/rector/asignaciones/",
        views.rector_asignaciones,
        name="rector_asignaciones",
    ),
    path(
        "dashboard/rector/matriculas/",
        views.rector_matriculas,
        name="rector_matriculas",
    ),
    path(
        "dashboard/rector/acudientes/",
        views.rector_acudientes,
        name="rector_acudientes",
    ),
    path(
        "dashboard/rector/historial/",
        views.rector_historial,
        name="rector_historial",
    ),
    path(
        "dashboard/rector/reportes/",
        views.rector_reportes,
        name="rector_reportes",
    ),

# ADMINISTRATIVO
path(
    "dashboard/administrativo/estudiantes/",
    views.panel_module,
    {"role": "administrativo", "module": "estudiantes"},
    name="administrativo_estudiantes",
),
path(
    "dashboard/administrativo/boletines/",
    views.panel_module,
    {"role": "administrativo", "module": "boletines"},
    name="administrativo_boletines",
),
path(
    "dashboard/administrativo/historial/",
    views.panel_module,
    {"role": "administrativo", "module": "historial"},
    name="administrativo_historial",
),

# COORDINADOR
path(
    "dashboard/coordinador/observaciones/",
    views.panel_module,
    {"role": "coordinador", "module": "observaciones"},
    name="coordinador_observaciones",
),
path(
    "dashboard/coordinador/citaciones/",
    views.panel_module,
    {"role": "coordinador", "module": "citaciones"},
    name="coordinador_citaciones",
),
path(
    "dashboard/coordinador/docentes/",
    views.panel_module,
    {"role": "coordinador", "module": "docentes"},
    name="coordinador_docentes",
),
path(
    "dashboard/coordinador/reportes/",
    views.panel_module,
    {"role": "coordinador", "module": "reportes"},
    name="coordinador_reportes",
),
path(
    "dashboard/coordinador/historial/",
    views.panel_module,
    {"role": "coordinador", "module": "historial"},
    name="coordinador_historial",
),

# ======================================
# DOCENTE
# ======================================
path("dashboard/docente/clases/", views.panel_module,
     {"role": "docente", "module": "clases"}, name="docente_clases"),

path("dashboard/docente/notas/", views.panel_module,
     {"role": "docente", "module": "notas"}, name="docente_notas"),

path("dashboard/docente/observaciones/", views.panel_module,
     {"role": "docente", "module": "observaciones"}, name="docente_observaciones"),

path("dashboard/docente/contenido/", views.panel_module,
     {"role": "docente", "module": "contenido"}, name="docente_contenido"),

path("dashboard/docente/historial/", views.panel_module,
     {"role": "docente", "module": "historial"}, name="docente_historial"),


# ======================================
# ESTUDIANTE
# ======================================
path("dashboard/estudiante/notas/", views.panel_module,
     {"role": "estudiante", "module": "notas"}, name="estudiante_notas"),

path("dashboard/estudiante/horarios/", views.panel_module,
     {"role": "estudiante", "module": "horarios"}, name="estudiante_horarios"),

path("dashboard/estudiante/boletines/", views.panel_module,
     {"role": "estudiante", "module": "boletines"}, name="estudiante_boletines"),

path("dashboard/estudiante/observaciones/", views.panel_module,
     {"role": "estudiante", "module": "observaciones"}, name="estudiante_observaciones"),

path("dashboard/estudiante/historial/", views.panel_module,
     {"role": "estudiante", "module": "historial"}, name="estudiante_historial"),


# ======================================
# ACUDIENTE
# ======================================
path("dashboard/acudiente/notas/", views.panel_module,
     {"role": "acudiente", "module": "notas"}, name="acudiente_notas"),

path("dashboard/acudiente/observaciones/", views.panel_module,
     {"role": "acudiente", "module": "observaciones"}, name="acudiente_observaciones"),

path("dashboard/acudiente/citaciones/", views.panel_module,
     {"role": "acudiente", "module": "citaciones"}, name="acudiente_citaciones"),

path("dashboard/acudiente/boletines/", views.panel_module,
     {"role": "acudiente", "module": "boletines"}, name="acudiente_boletines"),

path(
    "dashboard/configuracion/",
    views.configuracion,
    name="configuracion",
),
]
