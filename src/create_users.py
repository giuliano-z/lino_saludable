#!/usr/bin/env python
"""
Script para crear usuario inicial temporal en Railway
Después podés cambiarlo desde el admin web
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lino_saludable.settings')
django.setup()

from django.contrib.auth.models import User

# Crear usuario temporal "admin" con password "admin123"
# CAMBIAR INMEDIATAMENTE después del primer login
username = "admin"
password = "admin123"
email = "admin@linosaludable.com"

if User.objects.filter(username=username).exists():
    print(f"Usuario {username} ya existe.")
else:
    user = User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )
    print(f"✅ Usuario temporal creado:")
    print(f"   Username: {username}")
    print(f"   Password: {password}")
    print(f"   ⚠️  CAMBIAR INMEDIATAMENTE desde el admin!")

