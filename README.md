# SIDINO

## Descripción del proyecto

SIDINO busca centralizar los procesos académicos, administrativos y comunicativos de una institución educativa mediante una plataforma modular desarrollada con **Python y Django**. El sistema contempla una gestión organizada de usuarios, roles y permisos, administración de información académica, calificaciones, reportes, auditoría y herramientas de comunicación.

La plataforma está planteada para adaptarse a las necesidades de cada institución, permitiendo controlar qué módulos y funcionalidades están disponibles según su configuración y los permisos de cada usuario.

## Product Goal

Desarrollar SIDINO, una plataforma modular de gestión escolar construida para entornos con conectividad limitada o sin acceso a Internet.

## Sprint Goals
Sprint 1 – Preparación de la plataforma institucional
Establecer las bases de SIDINO para ofrecer una plataforma centralizada que permita organizar la información institucional y facilitar la gestión de los procesos académicos y administrativos.
Sprint 2 – Acceso y administración institucional
Ofrecer un acceso organizado y seguro a SIDINO, permitiendo administrar los usuarios institucionales y garantizar que cada integrante de la comunidad educativa disponga de las funcionalidades correspondientes a sus responsabilidades.
Sprint 3 – Gestión académica integral
Facilitar la administración de estudiantes, cursos, grupos, asignaturas, docentes y calificaciones, permitiendo centralizar la información académica y mejorar el seguimiento del rendimiento estudiantil.
Sprint 4 – Seguimiento, control y consulta de información
Fortalecer la gestión institucional mediante la consulta del calendario académico, la generación de reportes, el seguimiento de las actividades realizadas y la consolidación de las funcionalidades principales del sistema.

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


