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


## Instalación y ejecución local (Windows)

### 1. Clonar el repositorio

```powershell
git clone <URL-DEL-REPOSITORIO> SIDINO
cd SIDINO
git checkout feature/US-01-estructura-django
```

### 2. Crear el entorno virtual

Requiere Python 3.12 o superior.

```powershell
python -m venv .venv
```

### 3. Activar el entorno virtual

```powershell
.venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la ejecución de scripts:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

En CMD: `.venv\Scripts\activate.bat`

### 4. Instalar dependencias

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Configurar el archivo .env

```powershell
copy .env.example .env
```

Edita `.env` y reemplaza `SECRET_KEY` y `DB_PASSWORD`. Para generar una clave secreta:

```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

El archivo `.env` está en `.gitignore`: nunca lo subas al repositorio.

### 6. Configurar MySQL

Con el servidor MySQL iniciado, ejecuta en el cliente `mysql`:

```sql
CREATE DATABASE sidino_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'sidino_user'@'localhost' IDENTIFIED BY 'tu-contraseña';
GRANT ALL PRIVILEGES ON sidino_db.* TO 'sidino_user'@'localhost';
FLUSH PRIVILEGES;
```

Usa en `.env` los mismos valores de `DB_NAME`, `DB_USER` y `DB_PASSWORD`.

### 7. Ejecutar el servidor

```powershell
python manage.py migrate
python manage.py create_roles
python manage.py createsuperuser
python manage.py runserver
```

`createsuperuser` solicitará un nombre de usuario y una contraseña propia para el administrador inicial. No hay registro público ni credenciales predeterminadas. Inicia sesión en http://127.0.0.1:8000/login/; desde http://127.0.0.1:8000/admin/ el administrador puede crear usuarios, asignar grupos/roles y gestionar contraseñas.

Al asignar el rol de una cuenta, selecciona un único grupo institucional: `Rector`, `Administrativo`, `Coordinador`, `Docente`, `Estudiante` o `Acudiente`. Los grupos se crean al ejecutar las migraciones. Cada cuenta debe tener exactamente uno de estos grupos para acceder a su panel; el superusuario sin rol puede entrar al Admin para asignarlo.


Administrador demo:
admin
IlcGaCn3XtgvC96dVUx-eENlf1kCgX6I
