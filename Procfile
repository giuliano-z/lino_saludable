web: cd src && echo "🔄 Ejecutando migraciones..." && python manage.py migrate --noinput && echo "✅ Migraciones completadas" && gunicorn lino_saludable.wsgi --log-file -
