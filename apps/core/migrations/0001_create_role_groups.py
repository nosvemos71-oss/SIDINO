from django.db import migrations


ROLE_GROUPS = (
    "Rector",
    "Administrativo",
    "Coordinador",
    "Docente",
    "Estudiante",
    "Acudiente",
)


def create_role_groups(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    database = schema_editor.connection.alias

    for group_name in ROLE_GROUPS:
        Group.objects.using(database).get_or_create(name=group_name)


class Migration(migrations.Migration):
    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.RunPython(create_role_groups, migrations.RunPython.noop),
    ]
