#!/usr/bin/env python3
"""
Script temporal para ejecutar migraciones y crear usuarios en Railway PostgreSQL
"""
import os
import sys
import django

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lino_saludable.settings')
django.setup()

from django.core.management import call_command
from django.contrib.auth.models import User

def main():
    print("=" * 60)
    print("🚀 EJECUTANDO MIGRACIONES EN RAILWAY POSTGRESQL")
    print("=" * 60)
    
    # Verificar DATABASE_URL
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        print("❌ ERROR: DATABASE_URL no está configurada")
        print("   Ejecuta: railway shell --service web")
        print("   Luego ejecuta este script")
        sys.exit(1)
    
    print(f"\n📊 Base de datos: {db_url.split('@')[1] if '@' in db_url else 'unknown'}")
    
    # Ejecutar migraciones
    print("\n🔄 Ejecutando migraciones...")
    try:
        call_command('migrate', verbosity=2, interactive=False)
        print("✅ Migraciones completadas exitosamente")
    except Exception as e:
        print(f"❌ Error en migraciones: {e}")
        sys.exit(1)
    
    # Crear usuarios
    print("\n" + "=" * 60)
    print("👥 CREANDO USUARIOS")
    print("=" * 60)
    
    users_to_create = [
        {
            'username': 'sister_emprendedora',
            'email': 'sister@linosaludable.com',
            'password': 'SisterLino2025!',  # Cambiar después
            'is_superuser': True,
            'is_staff': True,
        },
        {
            'username': 'el_super_creador',
            'email': 'creador@linosaludable.com',
            'password': 'CreadorLino2025!',  # Cambiar después
            'is_superuser': True,
            'is_staff': True,
        }
    ]
    
    for user_data in users_to_create:
        username = user_data['username']
        
        if User.objects.filter(username=username).exists():
            print(f"\n⚠️  Usuario '{username}' ya existe, saltando...")
            continue
        
        try:
            user = User.objects.create_superuser(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password']
            )
            print(f"\n✅ Usuario creado exitosamente:")
            print(f"   👤 Username: {user_data['username']}")
            print(f"   🔑 Password temporal: {user_data['password']}")
            print(f"   ⚠️  IMPORTANTE: Cambiar contraseña inmediatamente!")
        except Exception as e:
            print(f"\n❌ Error creando usuario '{username}': {e}")
    
    print("\n" + "=" * 60)
    print("✅ PROCESO COMPLETADO")
    print("=" * 60)
    print("\n📝 Próximos pasos:")
    print("   1. Accede a: https://web-production-b0ad1.up.railway.app/admin/")
    print("   2. Usa las credenciales mostradas arriba")
    print("   3. CAMBIA las contraseñas inmediatamente")
    print("   4. Elimina este script: run_migrations_railway.py")
    print("\n")

if __name__ == '__main__':
    main()
