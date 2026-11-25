"""Configuración para desarrollo local."""
from .base import *  # noqa: F401,F403

DEBUG = True

# Mientras no exista el login real, usar el login de desarrollo.
LOGIN_URL = "/dev/login/"
