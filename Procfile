web: cd src && gunicorn lino_saludable.wsgi --log-file -
release: cd src && python manage.py migrate --noinput --verbosity 2 && python manage.py create_temp_admin
