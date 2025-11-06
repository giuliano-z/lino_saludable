#!/bin/bash
set -e

echo "🔄 Running database migrations..."
cd src
python manage.py migrate --noinput --verbosity 2

echo "👤 Creating temporary admin user..."
python manage.py create_temp_admin

echo "🚀 Starting Gunicorn..."
exec gunicorn lino_saludable.wsgi --log-file -
