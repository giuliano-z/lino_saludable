from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import connection


class Command(BaseCommand):
    help = 'Crea usuario temporal admin para acceso inicial'

    def handle(self, *args, **options):
        username = "admin"
        password = "admin123"
        email = "admin@linosaludable.com"

        # Verificar que la tabla auth_user existe
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'auth_user'
                );
            """)
            table_exists = cursor.fetchone()[0]
        
        if not table_exists:
            self.stdout.write(self.style.ERROR('❌ Tabla auth_user no existe. Ejecutar migraciones primero.'))
            return

        try:
            if User.objects.filter(username=username).exists():
                self.stdout.write(self.style.WARNING(f'Usuario {username} ya existe'))
            else:
                User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password
                )
                self.stdout.write(self.style.SUCCESS(f'✅ Usuario temporal creado:'))
                self.stdout.write(f'   Username: {username}')
                self.stdout.write(f'   Password: {password}')
                self.stdout.write(self.style.WARNING('   ⚠️  CAMBIAR INMEDIATAMENTE!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error al crear usuario: {e}'))
