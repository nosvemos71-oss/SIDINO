# Roles institucionales de SIDINO

ROLE_RECTOR = "Rector"
ROLE_ADMINISTRATIVO = "Administrativo"
ROLE_COORDINADOR = "Coordinador"
ROLE_DOCENTE = "Docente"
ROLE_ESTUDIANTE = "Estudiante"
ROLE_ACUDIENTE = "Acudiente"


ROLE_NAMES = (
    ROLE_RECTOR,
    ROLE_ADMINISTRATIVO,
    ROLE_COORDINADOR,
    ROLE_DOCENTE,
    ROLE_ESTUDIANTE,
    ROLE_ACUDIENTE,
)


# Relación con los nombres de la tabla rol de la base existente.
LEGACY_ROLE_NAMES = {
    ROLE_RECTOR: "Rectoria",
    ROLE_ADMINISTRATIVO: "Administrativo",
    ROLE_COORDINADOR: "Coordinacion",
    ROLE_DOCENTE: "Docente",
    ROLE_ESTUDIANTE: "Estudiante",
    ROLE_ACUDIENTE: "Acudiente",
}


# Catálogo de permisos institucionales.
PERMISSION_DEFINITIONS = (
    ("manage_users", "Puede administrar usuarios institucionales"),
    ("view_students", "Puede consultar estudiantes"),
    ("manage_students", "Puede gestionar estudiantes"),
    ("manage_courses", "Puede gestionar cursos y grupos"),
    ("manage_subjects", "Puede gestionar áreas y asignaturas"),
    ("assign_teachers", "Puede asignar docentes"),
    ("record_grades", "Puede registrar calificaciones"),
    ("view_assigned_grades", "Puede consultar calificaciones asignadas"),
    ("view_own_grades", "Puede consultar sus propias calificaciones"),
    ("view_wards_grades", "Puede consultar calificaciones de sus acudidos"),
    ("manage_calendar", "Puede gestionar el calendario académico"),
    ("view_calendar", "Puede consultar el calendario académico"),
    ("view_reports", "Puede consultar reportes académicos"),
    ("view_audit_log", "Puede consultar el historial de acciones"),
)


ALL_PERMISSIONS = tuple(
    codename for codename, description in PERMISSION_DEFINITIONS
)


# Matriz inicial de permisos por rol.
ROLE_PERMISSIONS = {
    ROLE_RECTOR: ALL_PERMISSIONS,

    ROLE_ADMINISTRATIVO: (
        "manage_users",
        "view_students",
        "manage_students",
        "view_audit_log",
    ),

    ROLE_COORDINADOR: (
        "view_students",
        "manage_courses",
        "manage_subjects",
        "assign_teachers",
        "manage_calendar",
        "view_calendar",
        "view_reports",
    ),

    ROLE_DOCENTE: (
        "record_grades",
        "view_assigned_grades",
        "view_calendar",
    ),

    ROLE_ESTUDIANTE: (
        "view_own_grades",
        "view_calendar",
    ),

    ROLE_ACUDIENTE: (
        "view_wards_grades",
        "view_calendar",
    ),
}