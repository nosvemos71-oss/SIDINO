# SIDINO

## Descripción del proyecto

SIDINO busca centralizar los procesos académicos, administrativos y comunicativos de una institución educativa mediante una plataforma modular desarrollada con **Python y Django**. El sistema contempla una gestión organizada de usuarios, roles y permisos, administración de información académica, calificaciones, reportes, auditoría y herramientas de comunicación.

La plataforma está planteada para adaptarse a las necesidades de cada institución, permitiendo controlar qué módulos y funcionalidades están disponibles según su configuración y los permisos de cada usuario.

## Product Goal

Desarrollar SIDINO, una plataforma modular de gestión escolar construida con Python y Django que permita centralizar los procesos académicos, administrativos y comunicativos de una institución educativa, mediante una interfaz intuitiva, un sistema flexible de roles y permisos, gestión de información segura y mecanismos que permitan trabajar en entornos con conectividad limitada o sin acceso a Internet.

El sistema buscará facilitar la gestión institucional, reducir procesos manuales, mejorar la comunicación entre actores y permitir que las instituciones adapten sus funcionalidades según sus necesidades.

## Sprint Goal

Migrar el proyecto SIDINO de Java a Python, utilizando Django como framework principal, y desarrollar los componentes necesarios para su adaptación a esta tecnología, contemplando la gestión de los procesos académicos y administrativos, la seguridad básica, las validaciones de información, la carga masiva de datos, la integración con servicios externos y la generación de reportes estadísticos con filtros multicriterio.

## Estructura general del proyecto

```text
SIDINO/
├── manage.py
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
├── README.md
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── apps/
│   ├── usuarios/
│   ├── permisos/
│   ├── dashboard/
│   ├── estudiantes/
│   ├── academico/
│   ├── calificaciones/
│   ├── calendario/
│   ├── comunicaciones/
│   ├── reportes/
│   ├── auditoria/
│   ├── configuracion/
│   ├── importaciones/
│   └── integraciones/
│
├── templates/
│   ├── base.html
│   ├── registration/
│   ├── dashboard/
│   └── componentes/
│
├── static/
│   ├── css/
│   ├── js/
│   └── img/
│
├── media/
├── docs/
└── tests/
```


