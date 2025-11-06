#!/usr/bin/env python
"""
Script para crear usuarios en Railway
Ejecutar: railway run --service web python src/create_users.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lino_saludable.settings')
django.setup()

from django.contrib.auth.models import User

# Crear superusuario 1: elsupercreador
print("Creando superusuario: elsupercreador")
username1 = input("Username para superusuario [elsupercreador]: ") or "elsupercreador"
email1 = input("Email: ")
password1 = input("Password: ")

if User.objects.filter(username=username1).exists():
    print(f"Usuario {username1} ya existe. Saltando...")
else:
    user1 = User.objects.create_superuser(
        username=username1,
        email=email1,
        password=password1
    )
    print(f"✅ Superusuario {username1} creado exitosamente!")

# Crear superusuario 2: gordalaemprendedora
print("\nCreando superusuario: gordalaemprendedora")
username2 = input("Username para segundo superusuario [gordalaemprendedora]: ") or "gordalaemprendedora"
email2 = input("Email: ")
password2 = input("Password: ")

if User.objects.filter(username=username2).exists():
    print(f"Usuario {username2} ya existe. Saltando...")
else:
    user2 = User.objects.create_superuser(
        username=username2,
        email=email2,
        password=password2
    )
    print(f"✅ Superusuario {username2} creado exitosamente!")

print("\n🎉 ¡Todos los usuarios creados!")
