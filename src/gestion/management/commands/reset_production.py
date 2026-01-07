"""
Comando CRÍTICO para resetear base de datos de PRODUCCIÓN (Railway).
⚠️  USAR CON EXTREMA PRECAUCIÓN ⚠️

Este comando:
- Elimina TODOS los datos transaccionales (ventas, compras, alertas, etc.)
- Elimina TODOS los productos y materias primas
- MANTIENE solo los usuarios especificados
- Resetea el sistema para empezar desde cero

Uso:
    # EN RAILWAY SHELL:
    python manage.py reset_production --confirm

    # Para ver qué haría sin ejecutar:
    python manage.py reset_production --dry-run
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth.models import User
from gestion.models import (
    Venta, VentaDetalle,
    Compra, CompraDetalle,
    LoteMateriaPrima,
    Alerta,
    Producto,
    MateriaPrima,
    MovimientoMateriaPrima,
    HistorialCosto,
    HistorialPreciosMateriaPrima,
    AjusteInventario,
    ProductoMateriaPrima,
    Receta,
    RecetaMateriaPrima
)


class Command(BaseCommand):
    help = '⚠️  RESETEA LA BASE DE DATOS DE PRODUCCIÓN - Mantiene solo usuarios especificados'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirma que deseas ejecutar el reset (REQUERIDO)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Muestra qué se eliminará sin ejecutar cambios'
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        confirm = options['confirm']

        # ⚠️  PROTECCIÓN: Requiere confirmación explícita
        if not dry_run and not confirm:
            self.stdout.write('')
            self.stdout.write(self.style.ERROR('=' * 70))
            self.stdout.write(self.style.ERROR('⚠️  ERROR: Debes usar --confirm para ejecutar este comando'))
            self.stdout.write(self.style.ERROR('=' * 70))
            self.stdout.write('')
            self.stdout.write('Este comando eliminará TODOS los datos de producción.')
            self.stdout.write('Para ver qué se eliminará: python manage.py reset_production --dry-run')
            self.stdout.write('Para ejecutar: python manage.py reset_production --confirm')
            self.stdout.write('')
            return

        # Header
        self.stdout.write('')
        self.stdout.write('=' * 70)
        if dry_run:
            self.stdout.write(self.style.WARNING('🔍 MODO SIMULACIÓN - No se eliminará nada'))
        else:
            self.stdout.write(self.style.ERROR('⚠️  RESET DE PRODUCCIÓN - RAILWAY'))
        self.stdout.write('=' * 70)
        self.stdout.write('')

        # Usuarios que se mantendrán
        USUARIOS_A_MANTENER = ['sister_emprendedora', 'el_super_creador']
        
        self.stdout.write(self.style.SUCCESS('✅ USUARIOS QUE SE MANTENDRÁN:'))
        usuarios_existentes = User.objects.filter(username__in=USUARIOS_A_MANTENER)
        for user in usuarios_existentes:
            self.stdout.write(f"   ✓ {user.username} ({user.email})")
        self.stdout.write('')

        # Contar registros actuales
        counts = self.count_records()
        
        # Mostrar reporte
        self.stdout.write(self.style.WARNING('📊 REGISTROS A ELIMINAR:'))
        self.stdout.write('')
        self.stdout.write(f"   ❌ Ventas: {counts['ventas']}")
        self.stdout.write(f"   ❌ Detalles de ventas: {counts['venta_detalles']}")
        self.stdout.write(f"   ❌ Compras: {counts['compras']}")
        self.stdout.write(f"   ❌ Detalles de compras: {counts['compra_detalles']}")
        self.stdout.write(f"   ❌ Productos: {counts['productos']}")
        self.stdout.write(f"   ❌ Materias primas: {counts['materias_primas']}")
        self.stdout.write(f"   ❌ Recetas: {counts['recetas']}")
        self.stdout.write(f"   ❌ Lotes MP: {counts['lotes']}")
        self.stdout.write(f"   ❌ Alertas: {counts['alertas']}")
        self.stdout.write(f"   ❌ Movimientos: {counts['movimientos']}")
        self.stdout.write(f"   ❌ Historial costos: {counts['historial_costos']}")
        self.stdout.write(f"   ❌ Historial precios: {counts['historial_precios']}")
        self.stdout.write(f"   ❌ Ajustes: {counts['ajustes']}")
        self.stdout.write(f"   ❌ Usuarios (excepto los 2 principales): {counts['otros_usuarios']}")
        self.stdout.write('')
        
        total_eliminar = sum([
            counts['ventas'], counts['venta_detalles'],
            counts['compras'], counts['compra_detalles'],
            counts['productos'], counts['materias_primas'],
            counts['recetas'], counts['lotes'], counts['alertas'],
            counts['movimientos'], counts['historial_costos'],
            counts['historial_precios'], counts['ajustes'],
            counts['otros_usuarios']
        ])

        if total_eliminar == 0:
            self.stdout.write(self.style.SUCCESS('✅ No hay registros para eliminar. El sistema ya está limpio.'))
            return

        # Modo dry-run
        if dry_run:
            self.stdout.write('=' * 70)
            self.stdout.write(self.style.WARNING(f'🔍 SIMULACIÓN: Se eliminarían {total_eliminar} registros'))
            self.stdout.write(self.style.WARNING('Para ejecutar el reset, usa: python manage.py reset_production --confirm'))
            self.stdout.write('=' * 70)
            self.stdout.write('')
            return

        # Confirmación final
        self.stdout.write('=' * 70)
        self.stdout.write(self.style.ERROR(f'⚠️  ADVERTENCIA FINAL: Se eliminarán {total_eliminar} registros'))
        self.stdout.write(self.style.ERROR('⚠️  Esta acción NO se puede deshacer'))
        self.stdout.write(self.style.ERROR('⚠️  Esto afectará la base de datos de PRODUCCIÓN en Railway'))
        self.stdout.write('=' * 70)
        self.stdout.write('')
        
        confirmacion = input('¿Estás 100% seguro? Escribe "RESETEAR PRODUCCION" para continuar: ')
        
        if confirmacion != 'RESETEAR PRODUCCION':
            self.stdout.write(self.style.ERROR('❌ Operación cancelada'))
            return

        # Ejecutar el reset
        self.stdout.write('')
        self.stdout.write(self.style.WARNING('🔄 Ejecutando reset de producción...'))
        self.stdout.write('')

        try:
            with transaction.atomic():
                deleted_counts = self.execute_reset(USUARIOS_A_MANTENER)

            # Reporte de éxito
            self.stdout.write('')
            self.stdout.write('=' * 70)
            self.stdout.write(self.style.SUCCESS('✅ RESET DE PRODUCCIÓN COMPLETADO'))
            self.stdout.write('=' * 70)
            self.stdout.write('')
            
            self.stdout.write(self.style.SUCCESS('📊 REGISTROS ELIMINADOS:'))
            for key, value in deleted_counts.items():
                self.stdout.write(f"   ✓ {key}: {value}")
            self.stdout.write('')
            
            self.stdout.write(self.style.SUCCESS('👥 USUARIOS ACTIVOS:'))
            usuarios_finales = User.objects.all()
            for user in usuarios_finales:
                self.stdout.write(f"   ✓ {user.username} - {user.email}")
            self.stdout.write('')
            
            self.stdout.write('=' * 70)
            self.stdout.write(self.style.SUCCESS('🎯 SISTEMA LISTO PARA EMPEZAR DE CERO'))
            self.stdout.write('')
            self.stdout.write('Próximos pasos:')
            self.stdout.write('1. Ingresa a: https://web-production-b0ad1.up.railway.app/admin/')
            self.stdout.write('2. Login con: sister_emprendedora / SisterLino2025!')
            self.stdout.write('3. Comienza a cargar productos y materias primas de enero 2026')
            self.stdout.write('')
            self.stdout.write('=' * 70)

        except Exception as e:
            self.stdout.write('')
            self.stdout.write(self.style.ERROR(f'❌ ERROR: {str(e)}'))
            self.stdout.write(self.style.ERROR('El reset no se completó. Se hizo rollback de cambios.'))
            raise

    def count_records(self):
        """Cuenta todos los registros relevantes"""
        USUARIOS_A_MANTENER = ['sister_emprendedora', 'el_super_creador']
        
        return {
            'ventas': Venta.objects.count(),
            'venta_detalles': VentaDetalle.objects.count(),
            'compras': Compra.objects.count(),
            'compra_detalles': CompraDetalle.objects.count(),
            'productos': Producto.objects.count(),
            'materias_primas': MateriaPrima.objects.count(),
            'recetas': Receta.objects.count(),
            'lotes': LoteMateriaPrima.objects.count(),
            'alertas': Alerta.objects.count(),
            'movimientos': MovimientoMateriaPrima.objects.count(),
            'historial_costos': HistorialCosto.objects.count(),
            'historial_precios': HistorialPreciosMateriaPrima.objects.count(),
            'ajustes': AjusteInventario.objects.count(),
            'otros_usuarios': User.objects.exclude(username__in=USUARIOS_A_MANTENER).count(),
        }

    def execute_reset(self, usuarios_a_mantener):
        """Ejecuta la eliminación completa"""
        deleted = {}

        # 1. Eliminar datos transaccionales
        self.stdout.write('   🗑️  Eliminando ventas...')
        vd = VentaDetalle.objects.count()
        v, _ = Venta.objects.all().delete()
        deleted['Ventas'] = v
        deleted['Detalles de ventas'] = vd

        self.stdout.write('   🗑️  Eliminando compras...')
        cd = CompraDetalle.objects.count()
        c, _ = Compra.objects.all().delete()
        deleted['Compras'] = c
        deleted['Detalles de compras'] = cd

        self.stdout.write('   🗑️  Eliminando lotes...')
        l, _ = LoteMateriaPrima.objects.all().delete()
        deleted['Lotes'] = l

        self.stdout.write('   🗑️  Eliminando alertas...')
        a, _ = Alerta.objects.all().delete()
        deleted['Alertas'] = a

        self.stdout.write('   🗑️  Eliminando movimientos...')
        m, _ = MovimientoMateriaPrima.objects.all().delete()
        deleted['Movimientos'] = m

        self.stdout.write('   🗑️  Eliminando historiales...')
        hc, _ = HistorialCosto.objects.all().delete()
        deleted['Historial costos'] = hc
        
        hp, _ = HistorialPreciosMateriaPrima.objects.all().delete()
        deleted['Historial precios'] = hp

        self.stdout.write('   🗑️  Eliminando ajustes...')
        aj, _ = AjusteInventario.objects.all().delete()
        deleted['Ajustes'] = aj

        # 2. Eliminar recetas (antes de productos)
        self.stdout.write('   🗑️  Eliminando recetas...')
        RecetaMateriaPrima.objects.all().delete()
        ProductoMateriaPrima.objects.all().delete()
        r, _ = Receta.objects.all().delete()
        deleted['Recetas'] = r

        # 3. Eliminar productos y materias primas
        self.stdout.write('   🗑️  Eliminando productos...')
        p, _ = Producto.objects.all().delete()
        deleted['Productos'] = p

        self.stdout.write('   🗑️  Eliminando materias primas...')
        mp, _ = MateriaPrima.objects.all().delete()
        deleted['Materias primas'] = mp

        # 4. Eliminar usuarios que NO están en la lista
        self.stdout.write('   🗑️  Eliminando usuarios no esenciales...')
        u, _ = User.objects.exclude(username__in=usuarios_a_mantener).delete()
        deleted['Usuarios eliminados'] = u

        return deleted
