#!/usr/bin/env bash
# Exit on error
set -o errexit

# Instalar dependencias
pip install -r requirements.txt

# Recoger archivos estáticos
python manage.py collectstatic --no-input

# Aplicar migraciones a PostgreSQL
python manage.py migrate

# Crear superusuario automático (si no existe)
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='josed').exists():
    User.objects.create_superuser('josed', 'jose070908@gmail.com', 'jose070908')
    print('Superusuario creado exitosamente.')
else:
    print('El superusuario ya existe.')
"