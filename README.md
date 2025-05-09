# Los Archivos de Mi Cole 📚

Una aplicación web en Django para organizar archivos escolares (PDF, videos, imágenes, textos) clasificados por curso, asignatura y trimestre.

## Características
- Gestión de usuarios (Admin, alumnos)
- CRUD de archivos educativos
- Relación jerárquica: Curso → Asignaturas → Trimestres → Archivos
- Compatible con phpMyAdmin y MySQL
- Diseño responsive con HTML, CSS y JavaScript
- Archivos almacenados localmente en `media/`

## Instalación
```bash
git clone https://github.com/tu_usuario/los_archivos_de_mi_cole.git
cd los_archivos_de_mi_cole
python -m venv env
source env/bin/activate  # o env\Scripts\activate en Windows
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

