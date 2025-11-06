"""
Comando Django para backup automático de la base de datos
Uso: python manage.py backup_db

Este comando:
1. Crea una copia de la base de datos con timestamp
2. Guarda en directorio backups/
3. Mantiene solo los últimos 7 días de backups
4. Puede ejecutarse desde cron job para backups automáticos
"""

from django.core.management.base import BaseCommand
from django.conf import settings
from pathlib import Path
import shutil
from datetime import datetime, timedelta
import os


class Command(BaseCommand):
    help = 'Crea backup de la base de datos y limpia backups antiguos'
    
    # Deshabilitar system checks para este comando
    requires_system_checks = []

    def add_arguments(self, parser):
        parser.add_argument(
            '--keep-days',
            type=int,
            default=7,
            help='Número de días de backups a mantener (default: 7)'
        )

    def handle(self, *args, **options):
        """Ejecuta el backup de la base de datos"""
        
        # Directorio base del proyecto
        base_dir = Path(settings.BASE_DIR)
        
        # Directorio de backups
        backup_dir = base_dir / 'backups'
        backup_dir.mkdir(exist_ok=True)
        
        # Base de datos actual
        db_path = base_dir / 'db.sqlite3'
        
        if not db_path.exists():
            self.stdout.write(self.style.ERROR('❌ No se encontró la base de datos'))
            return
        
        # Timestamp para el nombre del backup
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f'db_backup_{timestamp}.sqlite3'
        backup_path = backup_dir / backup_name
        
        try:
            # Crear backup
            self.stdout.write('📦 Creando backup de la base de datos...')
            shutil.copy2(db_path, backup_path)
            
            # Verificar que se creó correctamente
            if backup_path.exists():
                size_mb = backup_path.stat().st_size / (1024 * 1024)
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✅ Backup creado exitosamente: {backup_name} ({size_mb:.2f} MB)'
                    )
                )
            else:
                self.stdout.write(self.style.ERROR('❌ Error al crear el backup'))
                return
            
            # Limpiar backups antiguos
            self.cleanup_old_backups(backup_dir, options['keep_days'])
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error al crear backup: {str(e)}')
            )
    
    def cleanup_old_backups(self, backup_dir, keep_days):
        """Elimina backups más antiguos que keep_days"""
        
        self.stdout.write(f'\n🧹 Limpiando backups antiguos (manteniendo últimos {keep_days} días)...')
        
        # Fecha límite
        cutoff_date = datetime.now() - timedelta(days=keep_days)
        
        # Listar todos los backups
        backup_files = list(backup_dir.glob('db_backup_*.sqlite3'))
        
        if not backup_files:
            self.stdout.write('   No hay backups para limpiar')
            return
        
        deleted_count = 0
        kept_count = 0
        
        for backup_file in backup_files:
            # Obtener fecha del archivo
            file_date = datetime.fromtimestamp(backup_file.stat().st_mtime)
            
            if file_date < cutoff_date:
                try:
                    backup_file.unlink()
                    deleted_count += 1
                    self.stdout.write(f'   🗑️  Eliminado: {backup_file.name}')
                except Exception as e:
                    self.stdout.write(
                        self.style.WARNING(f'   ⚠️  No se pudo eliminar {backup_file.name}: {e}')
                    )
            else:
                kept_count += 1
        
        # Resumen
        self.stdout.write('')
        if deleted_count > 0:
            self.stdout.write(self.style.SUCCESS(f'✅ Eliminados {deleted_count} backups antiguos'))
        if kept_count > 0:
            self.stdout.write(f'📁 Mantenidos {kept_count} backups recientes')
        
        # Mostrar espacio total usado
        total_size = sum(f.stat().st_size for f in backup_dir.glob('db_backup_*.sqlite3'))
        total_size_mb = total_size / (1024 * 1024)
        self.stdout.write(f'💾 Espacio total de backups: {total_size_mb:.2f} MB')
