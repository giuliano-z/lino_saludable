"""
Comando Django para limpiar TODA la base de datos y comenzar de cero
Uso: python manage.py limpiar_datos
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from gestion.models import (
    Producto, MateriaPrima, Compra, Venta, VentaDetalle, 
    Receta, RecetaMateriaPrima, LoteMateriaPrima
)

User = get_user_model()

class Command(BaseCommand):
    help = 'Limpia TODOS los datos de prueba de la base de datos (excepto usuarios)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirmar',
            action='store_true',
            help='Confirma que deseas borrar TODOS los datos',
        )

    def handle(self, *args, **options):
        if not options['confirmar']:
            self.stdout.write(
                self.style.WARNING('⚠️  ADVERTENCIA: Este comando borrará TODOS los datos!')
            )
            self.stdout.write(
                self.style.WARNING('Para confirmar, ejecuta: python manage.py limpiar_datos --confirmar')
            )
            return

        self.stdout.write(self.style.WARNING('\n🗑️  Iniciando limpieza de datos...\n'))

        # Conteo antes
        counts_before = {
            'detalles_venta': VentaDetalle.objects.count(),
            'ventas': Venta.objects.count(),
            'ingredientes': RecetaMateriaPrima.objects.count(),
            'recetas': Receta.objects.count(),
            'lotes': LoteMateriaPrima.objects.count(),
            'compras': Compra.objects.count(),
            'productos': Producto.objects.count(),
            'materias_primas': MateriaPrima.objects.count(),
        }

        self.stdout.write('📊 Datos actuales:')
        for model, count in counts_before.items():
            self.stdout.write(f'  - {model}: {count}')

        # Borrar en orden para evitar errores de FK
        self.stdout.write('\n🔄 Eliminando datos...\n')

        try:
            # 1. Detalles de venta (dependen de Venta y Producto)
            VentaDetalle.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('✅ Detalles de venta eliminados'))

            # 2. Ventas
            Venta.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('✅ Ventas eliminadas'))

            # 3. Ingredientes de receta (dependen de Receta y MateriaPrima)
            RecetaMateriaPrima.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('✅ Ingredientes de receta eliminados'))

            # 4. Recetas
            Receta.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('✅ Recetas eliminadas'))

            # 5. Lotes de materia prima (dependen de MateriaPrima)
            LoteMateriaPrima.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('✅ Lotes de materia prima eliminados'))

            # 6. Compras (dependen de MateriaPrima)
            Compra.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('✅ Compras eliminadas'))

            # 7. Productos
            Producto.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('✅ Productos eliminados'))

            # 8. Materias primas
            MateriaPrima.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('✅ Materias primas eliminadas'))

            self.stdout.write(self.style.SUCCESS('\n✨ Base de datos limpiada exitosamente!\n'))
            
            # Mostrar resumen
            self.stdout.write('📊 Datos eliminados:')
            for model, count in counts_before.items():
                self.stdout.write(f'  - {model}: {count} registros')

            self.stdout.write(self.style.SUCCESS(f'\n🎉 Total: {sum(counts_before.values())} registros eliminados'))
            self.stdout.write(self.style.WARNING('\n💡 Los usuarios NO fueron eliminados'))
            self.stdout.write(self.style.SUCCESS('\n✅ Puedes comenzar a cargar datos reales ahora!\n'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\n❌ Error al limpiar datos: {str(e)}\n'))
            raise
