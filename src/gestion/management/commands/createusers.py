from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os


class Command(BaseCommand):
    help = 'Crea los usuarios principales del sistema'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('=' * 60))
        self.stdout.write(self.style.WARNING('👥 CREANDO USUARIOS SUPERADMIN'))
        self.stdout.write(self.style.WARNING('=' * 60))
        
        users = [
            {
                'username': 'sister_emprendedora',
                'email': 'sister@linosaludable.com',
                'password': os.environ.get('ADMIN_PASSWORD_1', 'SisterLino2025!')
            },
            {
                'username': 'el_super_creador',
                'email': 'creador@linosaludable.com',
                'password': os.environ.get('ADMIN_PASSWORD_2', 'CreadorLino2025!')
            }
        ]
        
        created_count = 0
        for user_data in users:
            username = user_data['username']
            if User.objects.filter(username=username).exists():
                self.stdout.write(self.style.WARNING(f'⚠️  Usuario {username} ya existe'))
            else:
                User.objects.create_superuser(
                    username=username,
                    email=user_data['email'],
                    password=user_data['password']
                )
                self.stdout.write(self.style.SUCCESS(f'✅ Usuario {username} creado'))
                self.stdout.write(f'   📧 Email: {user_data["email"]}')
                created_count += 1
        
        if created_count > 0:
            self.stdout.write('')
            self.stdout.write(self.style.WARNING('⚠️  IMPORTANTE: Cambiar contraseñas inmediatamente!'))
            self.stdout.write(self.style.WARNING('=' * 60))
        else:
            self.stdout.write(self.style.SUCCESS('✅ Todos los usuarios ya existen'))
            self.stdout.write(self.style.WARNING('=' * 60))

