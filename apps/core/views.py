from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render

from .roles import (
    ROLE_GROUP_NAMES,
    any_role_required,
    get_active_role,
    role_required,
)


def dashboard(request):
    role = get_active_role(request.user)
    if role is None:
        if request.user.is_staff:
            return redirect("admin:index")
        raise PermissionDenied
    return redirect(f"dashboard_{role}")


@role_required("rector")
def dashboard_rector(request):
    return render(request, "dashboard_preview.html")


@role_required("administrativo")
def dashboard_administrativo(request):
    return render(request, "dashboards/administrativo.html")


@role_required("coordinador")
def dashboard_coordinador(request):
    return render(request, "dashboards/coordinador.html")


@role_required("docente")
def dashboard_docente(request):
    return render(request, "dashboards/docente.html")


@role_required("estudiante")
def dashboard_estudiante(request):
    return render(request, "dashboards/estudiante.html")


@role_required("acudiente")
def dashboard_acudiente(request):
    return render(request, "dashboards/acudiente.html")

RECTOR_MODULES = {
    "usuarios": {
        "title": "Gestión de usuarios",
        "subtitle": "Administra los usuarios de la institución y sus roles de acceso.",
        "icon": "fa-users",
        "button": "Nuevo usuario",
        "stats": [
            {"label": "Usuarios registrados", "value": "248", "icon": "fa-users"},
            {"label": "Administrativos", "value": "12", "icon": "fa-user-tie"},
            {"label": "Docentes", "value": "32", "icon": "fa-chalkboard-user"},
            {"label": "Estudiantes", "value": "196", "icon": "fa-graduation-cap"},
        ],
        "columns": ["Nombre", "Correo", "Rol", "Estado"],
        "rows": [
            ["Laura Méndez", "laura@sidino.edu.co", "Docente", "Activo"],
            ["Carlos Rodríguez", "carlos@sidino.edu.co", "Coordinador", "Activo"],
            ["María Torres", "maria@sidino.edu.co", "Administrativo", "Activo"],
            ["Andrés Gómez", "andres@sidino.edu.co", "Estudiante", "Activo"],
            ["Paula Ramírez", "paula@sidino.edu.co", "Acudiente", "Activo"],
        ],
        "fields": ["Nombre completo", "Correo electrónico", "Documento", "Rol", "Teléfono"],
    },

    "materias": {
        "title": "Gestión de materias",
        "subtitle": "Organiza las asignaturas que forman parte del plan académico.",
        "icon": "fa-book",
        "button": "Nueva materia",
        "stats": [
            {"label": "Total materias", "value": "18", "icon": "fa-book"},
            {"label": "Área básica", "value": "8", "icon": "fa-book-open"},
            {"label": "Área complementaria", "value": "6", "icon": "fa-puzzle-piece"},
            {"label": "Otras áreas", "value": "4", "icon": "fa-layer-group"},
        ],
        "columns": ["Materia", "Área", "Intensidad horaria", "Estado"],
        "rows": [
            ["Matemáticas", "Ciencias exactas", "5 horas", "Activa"],
            ["Lengua castellana", "Humanidades", "4 horas", "Activa"],
            ["Ciencias naturales", "Ciencias naturales", "3 horas", "Activa"],
            ["Inglés", "Idiomas", "3 horas", "Activa"],
            ["Tecnología", "Tecnología", "2 horas", "Activa"],
        ],
        "fields": ["Nombre de la materia", "Área", "Intensidad horaria", "Descripción"],
    },

    "cursos": {
        "title": "Gestión de cursos",
        "subtitle": "Administra los grados, grupos y cursos de la institución.",
        "icon": "fa-graduation-cap",
        "button": "Nuevo curso",
        "stats": [
            {"label": "Cursos registrados", "value": "12", "icon": "fa-graduation-cap"},
            {"label": "Primaria", "value": "5", "icon": "fa-child"},
            {"label": "Secundaria", "value": "5", "icon": "fa-school"},
            {"label": "Media", "value": "2", "icon": "fa-user-graduate"},
        ],
        "columns": ["Curso", "Grado", "Grupo", "Director de grupo", "Estado"],
        "rows": [
            ["Primero A", "1°", "A", "Laura Méndez", "Activo"],
            ["Segundo A", "2°", "A", "Carlos Pérez", "Activo"],
            ["Sexto A", "6°", "A", "Ana Gómez", "Activo"],
            ["Séptimo B", "7°", "B", "María Torres", "Activo"],
            ["Décimo A", "10°", "A", "Andrés Ruiz", "Activo"],
        ],
        "fields": ["Grado", "Grupo", "Director de grupo", "Jornada", "Año lectivo"],
    },

    "salones": {
        "title": "Gestión de salones",
        "subtitle": "Consulta y organiza los espacios físicos de la institución.",
        "icon": "fa-door-open",
        "button": "Nuevo salón",
        "stats": [
            {"label": "Salones registrados", "value": "20", "icon": "fa-door-open"},
            {"label": "Disponibles", "value": "5", "icon": "fa-check-circle"},
            {"label": "En uso", "value": "13", "icon": "fa-school"},
            {"label": "Especializados", "value": "2", "icon": "fa-computer"},
        ],
        "columns": ["Salón", "Capacidad", "Tipo", "Ubicación", "Estado"],
        "rows": [
            ["Aula 101", "35", "Académico", "Bloque A", "Disponible"],
            ["Aula 102", "30", "Académico", "Bloque A", "Disponible"],
            ["Laboratorio 1", "25", "Informática", "Bloque B", "En uso"],
            ["Aula 201", "40", "Académico", "Bloque B", "Disponible"],
            ["Laboratorio 2", "20", "Especializado", "Bloque C", "En uso"],
        ],
        "fields": ["Nombre del salón", "Capacidad", "Tipo de salón", "Ubicación", "Descripción"],
    },

    "horarios": {
        "title": "Gestión de horarios",
        "subtitle": "Organiza la distribución de clases, docentes, cursos y salones.",
        "icon": "fa-calendar",
        "button": "Nuevo horario",
        "stats": [
            {"label": "Horarios creados", "value": "86", "icon": "fa-calendar"},
            {"label": "Jornada mañana", "value": "48", "icon": "fa-sun"},
            {"label": "Jornada tarde", "value": "38", "icon": "fa-cloud-sun"},
            {"label": "Conflictos", "value": "2", "icon": "fa-triangle-exclamation"},
        ],
        "columns": ["Curso", "Materia", "Docente", "Día", "Hora", "Salón"],
        "rows": [
            ["6° A", "Matemáticas", "Laura Méndez", "Lunes", "7:00 - 8:00", "Aula 101"],
            ["6° A", "Inglés", "Carlos Pérez", "Lunes", "8:00 - 9:00", "Aula 102"],
            ["7° B", "Ciencias", "Ana Gómez", "Martes", "9:00 - 10:00", "Laboratorio 1"],
            ["10° A", "Tecnología", "Andrés Ruiz", "Miércoles", "10:00 - 11:00", "Laboratorio 2"],
        ],
        "fields": ["Curso", "Materia", "Docente", "Día", "Hora de inicio", "Hora de finalización", "Salón"],
    },

    "periodos": {
        "title": "Periodos académicos",
        "subtitle": "Administra los periodos, fechas y etapas del calendario escolar.",
        "icon": "fa-calendar-days",
        "button": "Nuevo periodo",
        "stats": [
            {"label": "Periodos del año", "value": "4", "icon": "fa-calendar"},
            {"label": "Periodo actual", "value": "II", "icon": "fa-clock"},
            {"label": "Finalizados", "value": "1", "icon": "fa-check-circle"},
            {"label": "Pendientes", "value": "2", "icon": "fa-hourglass"},
        ],
        "columns": ["Periodo", "Fecha de inicio", "Fecha de finalización", "Estado"],
        "rows": [
            ["Periodo I", "20/01/2026", "27/03/2026", "Finalizado"],
            ["Periodo II", "06/04/2026", "19/06/2026", "Activo"],
            ["Periodo III", "06/07/2026", "11/09/2026", "Pendiente"],
            ["Periodo IV", "14/09/2026", "27/11/2026", "Pendiente"],
        ],
        "fields": ["Nombre del periodo", "Fecha de inicio", "Fecha de finalización", "Descripción"],
    },

    "asignaciones": {
        "title": "Asignaciones académicas",
        "subtitle": "Consulta la distribución de docentes, materias y cursos.",
        "icon": "fa-clipboard-list",
        "button": "Nueva asignación",
        "stats": [
            {"label": "Asignaciones", "value": "64", "icon": "fa-clipboard-list"},
            {"label": "Docentes", "value": "32", "icon": "fa-chalkboard-user"},
            {"label": "Materias", "value": "18", "icon": "fa-book"},
            {"label": "Cursos", "value": "12", "icon": "fa-graduation-cap"},
        ],
        "columns": ["Docente", "Materia", "Curso", "Horas semanales", "Estado"],
        "rows": [
            ["Laura Méndez", "Matemáticas", "6° A", "5", "Activa"],
            ["Carlos Pérez", "Inglés", "6° A", "3", "Activa"],
            ["Ana Gómez", "Ciencias naturales", "7° B", "4", "Activa"],
            ["Andrés Ruiz", "Tecnología", "10° A", "2", "Activa"],
            ["María Torres", "Lengua castellana", "8° A", "4", "Activa"],
        ],
        "fields": ["Docente", "Materia", "Curso", "Horas semanales", "Periodo"],
    },

    "matriculas": {
        "title": "Gestión de matrículas",
        "subtitle": "Consulta los procesos de matrícula y registro de estudiantes.",
        "icon": "fa-file-lines",
        "button": "Nueva matrícula",
        "stats": [
            {"label": "Matrículas", "value": "196", "icon": "fa-users"},
            {"label": "Matriculados", "value": "184", "icon": "fa-check-circle"},
            {"label": "En proceso", "value": "8", "icon": "fa-clock"},
            {"label": "Pendientes", "value": "4", "icon": "fa-file-circle-exclamation"},
        ],
        "columns": ["Estudiante", "Documento", "Curso", "Fecha de matrícula", "Estado"],
        "rows": [
            ["Andrés Gómez", "1001234567", "6° A", "20/01/2026", "Matriculado"],
            ["Sofía Ramírez", "1002345678", "7° B", "21/01/2026", "Matriculado"],
            ["Juan Martínez", "1003456789", "8° A", "22/01/2026", "En proceso"],
            ["Valentina López", "1004567890", "10° A", "23/01/2026", "Matriculado"],
        ],
        "fields": ["Nombre del estudiante", "Documento", "Curso", "Fecha", "Acudiente", "Estado"],
    },

    "acudientes": {
        "title": "Gestión de acudientes",
        "subtitle": "Administra la información de responsables y vínculos familiares.",
        "icon": "fa-user-group",
        "button": "Nuevo acudiente",
        "stats": [
            {"label": "Acudientes", "value": "173", "icon": "fa-users"},
            {"label": "Registrados", "value": "160", "icon": "fa-check-circle"},
            {"label": "Pendientes", "value": "13", "icon": "fa-clock"},
            {"label": "Estudiantes vinculados", "value": "196", "icon": "fa-graduation-cap"},
        ],
        "columns": ["Acudiente", "Documento", "Estudiante", "Parentesco", "Teléfono"],
        "rows": [
            ["Paula Ramírez", "52345678", "Andrés Gómez", "Madre", "3001234567"],
            ["Carlos López", "80123456", "Sofía Ramírez", "Padre", "3102345678"],
            ["María Torres", "52345679", "Juan Martínez", "Madre", "3203456789"],
            ["Pedro Gómez", "80123457", "Valentina López", "Padre", "3154567890"],
        ],
        "fields": ["Nombre completo", "Documento", "Teléfono", "Correo", "Parentesco", "Estudiante"],
    },

    "historial": {
        "title": "Historial institucional",
        "subtitle": "Consulta el registro de actividades y movimientos del sistema.",
        "icon": "fa-clock-rotate-left",
        "button": "",
        "stats": [
            {"label": "Movimientos", "value": "1.248", "icon": "fa-clock"},
            {"label": "Hoy", "value": "36", "icon": "fa-calendar"},
            {"label": "Usuarios activos", "value": "18", "icon": "fa-users"},
            {"label": "Eventos registrados", "value": "100%", "icon": "fa-shield"},
        ],
        "columns": ["Usuario", "Actividad", "Módulo", "Fecha", "Estado"],
        "rows": [
            ["Carol Trujillo", "Creación de usuario", "Usuarios", "25/11/2026 08:30", "Registrado"],
            ["Laura Méndez", "Actualización de horario", "Horarios", "25/11/2026 09:10", "Registrado"],
            ["Carlos Rodríguez", "Consulta de reporte", "Reportes", "25/11/2026 10:15", "Registrado"],
            ["María Torres", "Registro de matrícula", "Matrículas", "25/11/2026 11:00", "Registrado"],
        ],
        "fields": [],
    },

    "reportes": {
        "title": "Reportes institucionales",
        "subtitle": "Visualiza información general y estadísticas académicas.",
        "icon": "fa-chart-column",
        "button": "Generar reporte",
        "stats": [
            {"label": "Estudiantes", "value": "196", "icon": "fa-graduation-cap"},
            {"label": "Docentes", "value": "32", "icon": "fa-chalkboard-user"},
            {"label": "Cursos", "value": "12", "icon": "fa-school"},
            {"label": "Materias", "value": "18", "icon": "fa-book"},
        ],
        "columns": ["Reporte", "Categoría", "Descripción", "Disponibilidad"],
        "rows": [
            ["Reporte de estudiantes", "Académico", "Listado general de estudiantes", "Disponible"],
            ["Reporte de docentes", "Personal", "Información del cuerpo docente", "Disponible"],
            ["Reporte de matrículas", "Administrativo", "Estado de matrículas", "Disponible"],
            ["Reporte de cursos", "Académico", "Distribución de cursos y grupos", "Disponible"],
            ["Reporte de horarios", "Académico", "Distribución de horarios", "Disponible"],
        ],
        "fields": ["Tipo de reporte", "Periodo", "Curso", "Fecha"],
    },
}


@role_required("rector")
def rector_module(request, module):
    data = RECTOR_MODULES.get(module)

    if data is None:
        return render(request, "404.html", status=404)

    context = {
        "module_key": module,
        "module": data,
    }

    return render(
        request,
        "dashboards/modules/rector/module.html",
        context,
    )


@staff_member_required
@role_required("rector")
def rector_usuarios(request):
    if not (
        request.user.is_superuser
        or request.user.has_perm("auth.view_user")
        or request.user.has_perm("auth.change_user")
    ):
        raise PermissionDenied
    return redirect("admin:auth_user_changelist")


def rector_materias(request):
    return rector_module(request, "materias")


def rector_cursos(request):
    return rector_module(request, "cursos")


def rector_salones(request):
    return rector_module(request, "salones")


def rector_horarios(request):
    return rector_module(request, "horarios")


def rector_periodos(request):
    return rector_module(request, "periodos")


def rector_asignaciones(request):
    return rector_module(request, "asignaciones")


def rector_matriculas(request):
    return rector_module(request, "matriculas")


def rector_acudientes(request):
    return rector_module(request, "acudientes")


def rector_historial(request):
    return rector_module(request, "historial")


def rector_reportes(request):
    return rector_module(request, "reportes")


# ==========================================
# MÓDULOS ADMINISTRATIVO Y COORDINADOR
# ==========================================

PANEL_MODULES = {
    "administrativo": {
        "role": "Administrativo",
        "role_description": "Gestión administrativa",
        "navigation": [
            ("Inicio", "/dashboard/administrativo/", "fa-house"),
            ("Estudiantes", "/dashboard/administrativo/estudiantes/", "fa-user-graduate"),
            ("Boletines", "/dashboard/administrativo/boletines/", "fa-file-lines"),
            ("Historial", "/dashboard/administrativo/historial/", "fa-clock-rotate-left"),
        ],
        "modules": {
            "estudiantes": {
                "title": "Gestión de estudiantes",
                "description": "Consulta y administra la información de los estudiantes.",
                "stats": [("Estudiantes registrados", "120"), ("Activos", "115"), ("Inactivos", "5")],
                "columns": ["Código", "Nombre", "Documento", "Curso", "Estado"],
                "rows": [
                    ["EST001", "Laura Gómez", "1001001001", "10-A", "Activo"],
                    ["EST002", "Andrés Pérez", "1001001002", "9-B", "Activo"],
                    ["EST003", "Sofía Rodríguez", "1001001003", "8-A", "Activo"],
                    ["EST004", "Daniel Martínez", "1001001004", "11-A", "Inactivo"],
                ],
            },
            "boletines": {
                "title": "Gestión de boletines",
                "description": "Consulta el estado de los boletines académicos.",
                "stats": [("Boletines generados", "95"), ("Pendientes", "12"), ("Periodos", "4")],
                "columns": ["Estudiante", "Curso", "Periodo", "Fecha", "Estado"],
                "rows": [
                    ["Laura Gómez", "10-A", "Primero", "20/03/2026", "Generado"],
                    ["Andrés Pérez", "9-B", "Primero", "20/03/2026", "Pendiente"],
                    ["Sofía Rodríguez", "8-A", "Primero", "21/03/2026", "Generado"],
                ],
            },
            "historial": {
                "title": "Historial administrativo",
                "description": "Consulta los movimientos realizados en el área administrativa.",
                "stats": [("Movimientos", "28"), ("Usuarios", "8"), ("Hoy", "3")],
                "columns": ["Actividad", "Usuario", "Fecha", "Descripción"],
                "rows": [
                    ["Registro", "Administrativo", "25/11/2026", "Registro de estudiante"],
                    ["Boletín", "Administrativo", "24/11/2026", "Generación de boletín"],
                    ["Actualización", "Administrativo", "23/11/2026", "Actualización de datos"],
                ],
            },
        },
    },

    "coordinador": {
        "role": "Coordinador",
        "role_description": "Coordinación académica",
        "navigation": [
            ("Inicio", "/dashboard/coordinador/", "fa-house"),
            ("Observaciones", "/dashboard/coordinador/observaciones/", "fa-comment-dots"),
            ("Citaciones", "/dashboard/coordinador/citaciones/", "fa-calendar-check"),
            ("Docentes", "/dashboard/coordinador/docentes/", "fa-chalkboard-user"),
            ("Reportes", "/dashboard/coordinador/reportes/", "fa-chart-pie"),
            ("Historial", "/dashboard/coordinador/historial/", "fa-clock-rotate-left"),
        ],
        "modules": {
            "observaciones": {
                "title": "Observaciones académicas",
                "description": "Registra y consulta observaciones de estudiantes.",
                "stats": [("Observaciones", "32"), ("Pendientes", "8"), ("Atendidas", "24")],
                "columns": ["Estudiante", "Curso", "Docente", "Observación", "Estado"],
                "rows": [
                    ["Laura Gómez", "10-A", "Carlos Ruiz", "Seguimiento académico", "Pendiente"],
                    ["Andrés Pérez", "9-B", "Ana Torres", "Mejora en convivencia", "Atendida"],
                    ["Sofía Rodríguez", "8-A", "Luis Díaz", "Refuerzo académico", "Pendiente"],
                ],
            },
            "citaciones": {
                "title": "Citaciones",
                "description": "Consulta y organiza las citaciones institucionales.",
                "stats": [("Citaciones", "18"), ("Programadas", "10"), ("Realizadas", "8")],
                "columns": ["Estudiante", "Acudiente", "Motivo", "Fecha", "Estado"],
                "rows": [
                    ["Laura Gómez", "María Gómez", "Seguimiento académico", "28/11/2026", "Programada"],
                    ["Andrés Pérez", "Juan Pérez", "Convivencia", "29/11/2026", "Programada"],
                    ["Sofía Rodríguez", "Diana Rodríguez", "Rendimiento", "20/11/2026", "Realizada"],
                ],
            },
            "docentes": {
                "title": "Gestión de docentes",
                "description": "Consulta la información del equipo docente.",
                "stats": [("Docentes", "24"), ("Activos", "23"), ("Áreas", "8")],
                "columns": ["Código", "Nombre", "Área", "Correo", "Estado"],
                "rows": [
                    ["DOC001", "Carlos Ruiz", "Matemáticas", "carlos@sidino.edu", "Activo"],
                    ["DOC002", "Ana Torres", "Ciencias", "ana@sidino.edu", "Activo"],
                    ["DOC003", "Luis Díaz", "Lenguaje", "luis@sidino.edu", "Activo"],
                ],
            },
            "reportes": {
                "title": "Reportes académicos",
                "description": "Consulta los reportes generales de coordinación.",
                "stats": [("Reportes", "15"), ("Académicos", "9"), ("Convivencia", "6")],
                "columns": ["Reporte", "Categoría", "Fecha", "Responsable", "Estado"],
                "rows": [
                    ["Rendimiento por curso", "Académico", "22/11/2026", "Coordinador", "Disponible"],
                    ["Seguimiento docente", "Docentes", "23/11/2026", "Coordinador", "Disponible"],
                    ["Convivencia escolar", "Convivencia", "24/11/2026", "Coordinador", "Disponible"],
                ],
            },
            "historial": {
                "title": "Historial de coordinación",
                "description": "Consulta las actividades realizadas por coordinación.",
                "stats": [("Movimientos", "42"), ("Esta semana", "12"), ("Hoy", "4")],
                "columns": ["Actividad", "Responsable", "Fecha", "Descripción"],
                "rows": [
                    ["Observación", "Coordinador", "25/11/2026", "Registro de observación"],
                    ["Citación", "Coordinador", "24/11/2026", "Programación de citación"],
                    ["Reporte", "Coordinador", "23/11/2026", "Consulta de reporte"],
                ],
            },
        },
    },
}


def panel_module(request, role, module):
    panel = PANEL_MODULES.get(role)

    if not panel:
        from django.http import Http404
        raise Http404("Módulo no encontrado")

    if get_active_role(request.user) != role:
        raise PermissionDenied

    if module not in panel["modules"]:
        from django.http import Http404
        raise Http404("Módulo no encontrado")

    data = panel["modules"][module]

    return render(request, "dashboards/modules/shared/module.html", {
        "role": panel["role"],
        "role_description": panel["role_description"],
        "navigation": panel["navigation"],
        "module": data,
        "module_key": module,
        "active_url": request.path,
    })

# ==========================================
# MÓDULOS DOCENTE, ESTUDIANTE Y ACUDIENTE
# ==========================================

PANEL_MODULES.update({

    # ======================================
    # DOCENTE
    # ======================================
    "docente": {
        "role": "Docente",
        "role_description": "Gestión académica docente",
        "navigation": [
            ("Inicio", "/dashboard/docente/", "fa-house"),
            ("Mis clases", "/dashboard/docente/clases/", "fa-chalkboard"),
            ("Notas", "/dashboard/docente/notas/", "fa-clipboard-list"),
            ("Observaciones", "/dashboard/docente/observaciones/", "fa-comment-dots"),
            ("Contenido", "/dashboard/docente/contenido/", "fa-book-open"),
            ("Historial", "/dashboard/docente/historial/", "fa-clock-rotate-left"),
        ],
        "modules": {
            "clases": {
                "title": "Mis clases",
                "description": "Consulta los cursos y asignaturas que tienes asignados.",
                "stats": [
                    ("Clases asignadas", "8"),
                    ("Cursos", "4"),
                    ("Estudiantes", "120"),
                ],
                "columns": ["Asignatura", "Curso", "Horario", "Salón", "Estado"],
                "rows": [
                    ["Matemáticas", "10-A", "Lunes 7:00 AM", "101", "Activa"],
                    ["Matemáticas", "10-B", "Martes 8:00 AM", "102", "Activa"],
                    ["Álgebra", "9-A", "Miércoles 9:00 AM", "103", "Activa"],
                ],
            },
            "notas": {
                "title": "Gestión de notas",
                "description": "Consulta las calificaciones registradas por asignatura y curso.",
                "stats": [
                    ("Notas registradas", "180"),
                    ("Estudiantes", "120"),
                    ("Periodos", "4"),
                ],
                "columns": ["Estudiante", "Curso", "Asignatura", "Calificación", "Periodo"],
                "rows": [
                    ["Laura Gómez", "10-A", "Matemáticas", "4.5", "Primero"],
                    ["Andrés Pérez", "10-A", "Matemáticas", "3.8", "Primero"],
                    ["Sofía Rodríguez", "10-B", "Matemáticas", "4.2", "Primero"],
                ],
            },
            "observaciones": {
                "title": "Observaciones de estudiantes",
                "description": "Registra y consulta observaciones académicas y de convivencia.",
                "stats": [
                    ("Observaciones", "25"),
                    ("Pendientes", "7"),
                    ("Atendidas", "18"),
                ],
                "columns": ["Estudiante", "Curso", "Tipo", "Descripción", "Estado"],
                "rows": [
                    ["Laura Gómez", "10-A", "Académica", "Buen desempeño", "Registrada"],
                    ["Andrés Pérez", "10-A", "Convivencia", "Debe mejorar la participación", "Pendiente"],
                    ["Sofía Rodríguez", "10-B", "Académica", "Requiere refuerzo", "Registrada"],
                ],
            },
            "contenido": {
                "title": "Contenido académico",
                "description": "Consulta los materiales y recursos de tus asignaturas.",
                "stats": [
                    ("Recursos", "18"),
                    ("Asignaturas", "3"),
                    ("Publicados", "15"),
                ],
                "columns": ["Contenido", "Asignatura", "Tipo", "Fecha", "Estado"],
                "rows": [
                    ["Introducción al álgebra", "Matemáticas", "Documento", "20/11/2026", "Publicado"],
                    ["Ejercicios de ecuaciones", "Matemáticas", "Actividad", "22/11/2026", "Publicado"],
                    ["Guía de funciones", "Álgebra", "PDF", "24/11/2026", "Borrador"],
                ],
            },
            "historial": {
                "title": "Historial docente",
                "description": "Consulta las actividades realizadas dentro del sistema.",
                "stats": [
                    ("Actividades", "35"),
                    ("Esta semana", "12"),
                    ("Hoy", "3"),
                ],
                "columns": ["Actividad", "Curso", "Fecha", "Descripción"],
                "rows": [
                    ["Registro de notas", "10-A", "25/11/2026", "Actualización de calificaciones"],
                    ["Observación", "10-B", "24/11/2026", "Registro de observación"],
                    ["Contenido", "9-A", "23/11/2026", "Publicación de material"],
                ],
            },
        },
    },

    # ======================================
    # ESTUDIANTE
    # ======================================
    "estudiante": {
        "role": "Estudiante",
        "role_description": "Portal académico estudiantil",
        "navigation": [
            ("Inicio", "/dashboard/estudiante/", "fa-house"),
            ("Mis notas", "/dashboard/estudiante/notas/", "fa-clipboard-list"),
            ("Horarios", "/dashboard/estudiante/horarios/", "fa-calendar-days"),
            ("Boletines", "/dashboard/estudiante/boletines/", "fa-file-lines"),
            ("Observaciones", "/dashboard/estudiante/observaciones/", "fa-comment-dots"),
            ("Historial", "/dashboard/estudiante/historial/", "fa-clock-rotate-left"),
        ],
        "modules": {
            "notas": {
                "title": "Mis notas",
                "description": "Consulta tus calificaciones por asignatura y periodo.",
                "stats": [
                    ("Promedio general", "4.2"),
                    ("Asignaturas", "8"),
                    ("Periodo actual", "Segundo"),
                ],
                "columns": ["Asignatura", "Docente", "Nota", "Periodo", "Estado"],
                "rows": [
                    ["Matemáticas", "Carlos Ruiz", "4.5", "Primero", "Aprobada"],
                    ["Ciencias", "Ana Torres", "3.8", "Primero", "Aprobada"],
                    ["Lenguaje", "Luis Díaz", "4.2", "Primero", "Aprobada"],
                ],
            },
            "horarios": {
                "title": "Mi horario académico",
                "description": "Consulta tus clases, horarios y salones asignados.",
                "stats": [
                    ("Asignaturas", "8"),
                    ("Días de clase", "5"),
                    ("Jornada", "Mañana"),
                ],
                "columns": ["Día", "Asignatura", "Hora", "Salón", "Docente"],
                "rows": [
                    ["Lunes", "Matemáticas", "7:00 - 8:00 AM", "101", "Carlos Ruiz"],
                    ["Martes", "Ciencias", "8:00 - 9:00 AM", "102", "Ana Torres"],
                    ["Miércoles", "Lenguaje", "9:00 - 10:00 AM", "103", "Luis Díaz"],
                ],
            },
            "boletines": {
                "title": "Mis boletines",
                "description": "Consulta el estado de tus boletines académicos.",
                "stats": [
                    ("Boletines", "2"),
                    ("Disponibles", "1"),
                    ("Pendientes", "1"),
                ],
                "columns": ["Periodo", "Fecha", "Promedio", "Estado"],
                "rows": [
                    ["Primero", "20/03/2026", "4.2", "Disponible"],
                    ["Segundo", "Pendiente", "—", "En proceso"],
                ],
            },
            "observaciones": {
                "title": "Mis observaciones",
                "description": "Consulta las observaciones registradas sobre tu proceso académico.",
                "stats": [
                    ("Observaciones", "3"),
                    ("Académicas", "2"),
                    ("Convivencia", "1"),
                ],
                "columns": ["Fecha", "Docente", "Tipo", "Descripción", "Estado"],
                "rows": [
                    ["20/11/2026", "Carlos Ruiz", "Académica", "Buen desempeño", "Registrada"],
                    ["22/11/2026", "Ana Torres", "Académica", "Participación en clase", "Registrada"],
                    ["24/11/2026", "Luis Díaz", "Convivencia", "Recomendación de mejora", "Registrada"],
                ],
            },
            "historial": {
                "title": "Mi historial académico",
                "description": "Consulta el registro de tus actividades académicas.",
                "stats": [
                    ("Registros", "12"),
                    ("Este mes", "5"),
                    ("Año lectivo", "2026"),
                ],
                "columns": ["Actividad", "Asignatura", "Fecha", "Descripción"],
                "rows": [
                    ["Calificación", "Matemáticas", "25/11/2026", "Consulta de nota"],
                    ["Boletín", "General", "20/11/2026", "Boletín disponible"],
                    ["Observación", "Ciencias", "18/11/2026", "Nueva observación"],
                ],
            },
        },
    },

    # ======================================
    # ACUDIENTE
    # ======================================
    "acudiente": {
        "role": "Acudiente",
        "role_description": "Seguimiento académico familiar",
        "navigation": [
            ("Inicio", "/dashboard/acudiente/", "fa-house"),
            ("Notas de mi hijo", "/dashboard/acudiente/notas/", "fa-clipboard-list"),
            ("Observaciones", "/dashboard/acudiente/observaciones/", "fa-comment-dots"),
            ("Citaciones", "/dashboard/acudiente/citaciones/", "fa-calendar-check"),
            ("Boletines", "/dashboard/acudiente/boletines/", "fa-file-lines"),
        ],
        "modules": {
            "notas": {
                "title": "Notas de mi hijo",
                "description": "Consulta las calificaciones y el rendimiento académico.",
                "stats": [
                    ("Promedio general", "4.2"),
                    ("Asignaturas", "8"),
                    ("Periodo actual", "Segundo"),
                ],
                "columns": ["Asignatura", "Docente", "Calificación", "Periodo", "Estado"],
                "rows": [
                    ["Matemáticas", "Carlos Ruiz", "4.5", "Primero", "Aprobada"],
                    ["Ciencias", "Ana Torres", "3.8", "Primero", "Aprobada"],
                    ["Lenguaje", "Luis Díaz", "4.2", "Primero", "Aprobada"],
                ],
            },
            "observaciones": {
                "title": "Observaciones",
                "description": "Consulta las observaciones académicas y de convivencia.",
                "stats": [
                    ("Observaciones", "3"),
                    ("Académicas", "2"),
                    ("Convivencia", "1"),
                ],
                "columns": ["Fecha", "Docente", "Tipo", "Descripción", "Estado"],
                "rows": [
                    ["20/11/2026", "Carlos Ruiz", "Académica", "Buen desempeño", "Registrada"],
                    ["22/11/2026", "Ana Torres", "Académica", "Requiere refuerzo", "Registrada"],
                    ["24/11/2026", "Luis Díaz", "Convivencia", "Recomendación de mejora", "Registrada"],
                ],
            },
            "citaciones": {
                "title": "Citaciones",
                "description": "Consulta las reuniones y citaciones programadas por la institución.",
                "stats": [
                    ("Citaciones", "3"),
                    ("Pendientes", "2"),
                    ("Realizadas", "1"),
                ],
                "columns": ["Motivo", "Fecha", "Hora", "Responsable", "Estado"],
                "rows": [
                    ["Seguimiento académico", "28/11/2026", "8:00 AM", "Coordinación", "Programada"],
                    ["Reunión con docente", "30/11/2026", "9:00 AM", "Carlos Ruiz", "Programada"],
                    ["Convivencia escolar", "20/11/2026", "10:00 AM", "Coordinación", "Realizada"],
                ],
            },
            "boletines": {
                "title": "Boletines académicos",
                "description": "Consulta los boletines y resultados de cada periodo escolar.",
                "stats": [
                    ("Boletines", "2"),
                    ("Disponibles", "1"),
                    ("Pendientes", "1"),
                ],
                "columns": ["Periodo", "Fecha", "Promedio", "Estado"],
                "rows": [
                    ["Primero", "20/03/2026", "4.2", "Disponible"],
                    ["Segundo", "Pendiente", "—", "En proceso"],
                ],
            },
        },
    },

})

# ==========================================
# CONFIGURACIÓN GENERAL SIDINO
# ==========================================

@any_role_required
def configuracion(request):
    role = get_active_role(request.user)
    return render(request, "dashboards/modules/shared/configuracion.html", {
        "dashboard_url": f"/dashboard/{role}/",
        "dashboard_role": ROLE_GROUP_NAMES[role],
    })

