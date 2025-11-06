from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Crea los usuarios principales del sistema'

    def handle(self, *args, **options):
        users = [
            {
                'username': 'sister_emprendedora',
                'email': 'sister@linosaludable.com',
                'password': 'SisterLino2025!'
            },
            {
                'username': 'el_super_creador',
                'email': 'creador@linosaludable.com',
                'password': 'CreadorLino2025!'
            }
        ]
        
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
                self.stdout.write(f'   Password temporal: {user_data["password"]}')
                self.stdout.write(self.style.WARNING('   ⚠️  CAMBIAR INMEDIATAMENTE!'))
