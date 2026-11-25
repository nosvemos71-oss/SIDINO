"""Modelos que mapean las tablas YA existentes en MySQL (sidino.sql).

Son managed=False: Django no los crea ni los migra, solo los lee.
Por seguridad NO se declara la columna `contrasena`.
"""
import unicodedata

from django.db import models

# nombre_rol (tabla `rol`) -> clave interna usada en URLs, vistas y plantillas
ROLE_SLUGS = {
    "rectoria": "rector",
    "coordinacion": "coordinador",
    "administrativo": "administrativo",
    "docente": "docente",
    "estudiante": "estudiante",
    "acudiente": "acudiente",
}


def _normalize(text):
    text = unicodedata.normalize("NFKD", text or "")
    return "".join(c for c in text if not unicodedata.combining(c)).strip().lower()


class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True)
    nombre_rol = models.CharField(max_length=60)

    class Meta:
        managed = False
        db_table = "rol"

    def __str__(self):
        return self.nombre_rol

    @property
    def slug(self):
        return ROLE_SLUGS.get(_normalize(self.nombre_rol))


class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=120)
    correo = models.CharField(max_length=120)
    rol = models.ForeignKey(Rol, db_column="id_rol", on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "usuario"

    def __str__(self):
        return self.nombre

    @property
    def slug(self):
        return self.rol.slug

    @property
    def iniciales(self):
        partes = self.nombre.split()
        return "".join(p[0] for p in partes[:2]).upper() or "U"
