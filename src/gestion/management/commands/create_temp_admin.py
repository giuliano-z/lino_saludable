from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Crea usuario temporal admin para acceso inicial'

    def handle(self, *args, **options):
        username = "admin"
        password = "admin123"
        email = "admin@linosaludable.com"

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
