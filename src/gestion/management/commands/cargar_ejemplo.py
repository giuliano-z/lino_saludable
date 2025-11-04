"""
Comando Django para cargar datos de ejemplo realistas
Uso: python manage.py cargar_ejemplo
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from gestion.models import (
    Producto, MateriaPrima, Compra, Venta, VentaDetalle, 
    Receta, RecetaMateriaPrima
)
from decimal import Decimal
from datetime import datetime, timedelta
from django.utils import timezone

User = get_user_model()

class Command(BaseCommand):
    help = 'Carga datos de ejemplo realistas para testing'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('\n🌱 Cargando datos de ejemplo...\n'))

        # Usuario admin (debe existir)
        admin = User.objects.first()
        if not admin:
            self.stdout.write(self.style.ERROR('❌ No hay usuarios. Crea un superusuario primero.'))
            return

        # ===== 1. MATERIAS PRIMAS =====
        self.stdout.write('📦 Creando materias primas...')
        
        harina_integral = MateriaPrima.objects.create(
            nombre='Harina Integral Orgánica',
            unidad_medida='kg',
            costo_unitario=Decimal('450.00'),
            stock_actual=Decimal('50.00'),
            stock_minimo=Decimal('10.00'),
            proveedor='Alimentos Naturales SA'
        )
        
        aceite_coco = MateriaPrima.objects.create(
            nombre='Aceite de Coco Virgen',
            unidad_medida='lt',
            costo_unitario=Decimal('850.00'),
            stock_actual=Decimal('20.00'),
            stock_minimo=Decimal('5.00'),
            proveedor='Orgánicos del Sur'
        )
        
        mani = MateriaPrima.objects.create(
            nombre='Maní sin Sal',
            unidad_medida='kg',
            costo_unitario=Decimal('600.00'),
            stock_actual=Decimal('30.00'),
            stock_minimo=Decimal('8.00'),
            proveedor='Frutos Secos Argentina'
        )

        avena = MateriaPrima.objects.create(
            nombre='Avena Integral',
            unidad_medida='kg',
            costo_unitario=Decimal('350.00'),
            stock_actual=Decimal('40.00'),
            stock_minimo=Decimal('12.00'),
            proveedor='Cereales Naturales'
        )

        self.stdout.write(self.style.SUCCESS(f'✅ {MateriaPrima.objects.count()} materias primas creadas'))

        # ===== 2. COMPRAS =====
        self.stdout.write('🛒 Registrando compras...')
        
        Compra.objects.create(
            proveedor='Alimentos Naturales SA',
            materia_prima=harina_integral,
            cantidad_mayoreo=Decimal('50.00'),
            precio_mayoreo=Decimal('22500.00'),  # 450 x 50
        )
        
        Compra.objects.create(
            proveedor='Orgánicos del Sur',
            materia_prima=aceite_coco,
            cantidad_mayoreo=Decimal('20.00'),
            precio_mayoreo=Decimal('17000.00'),  # 850 x 20
        )

        Compra.objects.create(
            proveedor='Frutos Secos Argentina',
            materia_prima=mani,
            cantidad_mayoreo=Decimal('30.00'),
            precio_mayoreo=Decimal('18000.00'),  # 600 x 30
        )

        self.stdout.write(self.style.SUCCESS(f'✅ {Compra.objects.count()} compras registradas'))

        # ===== 3. RECETAS =====
        self.stdout.write('📖 Creando recetas...')
        
        receta_barras = Receta.objects.create(
            nombre='Barras de Cereal Integral',
            descripcion='Barras nutritivas con avena, maní y aceite de coco. Rinde 20 unidades.'
        )
        
        RecetaMateriaPrima.objects.create(
            receta=receta_barras,
            materia_prima=avena,
            cantidad=Decimal('2.00')
        )
        
        RecetaMateriaPrima.objects.create(
            receta=receta_barras,
            materia_prima=mani,
            cantidad=Decimal('1.00')
        )

        RecetaMateriaPrima.objects.create(
            receta=receta_barras,
            materia_prima=aceite_coco,
            cantidad=Decimal('0.3')
        )

        receta_crackers = Receta.objects.create(
            nombre='Crackers Integrales',
            descripcion='Galletas crujientes con harina integral. Rinde 50 unidades.'
        )

        RecetaMateriaPrima.objects.create(
            receta=receta_crackers,
            materia_prima=harina_integral,
            cantidad=Decimal('1.5')
        )

        RecetaMateriaPrima.objects.create(
            receta=receta_crackers,
            materia_prima=aceite_coco,
            cantidad=Decimal('0.2')
        )

        self.stdout.write(self.style.SUCCESS(f'✅ {Receta.objects.count()} recetas creadas'))

        # ===== 4. PRODUCTOS =====
        self.stdout.write('🏷️  Creando productos...')
        
        # Calcular costos de recetas
        costo_barras = sum(
            ing.cantidad * ing.materia_prima.costo_unitario 
            for ing in receta_barras.ingredientes.all()
        ) / receta_barras.rendimiento

        costo_crackers = sum(
            ing.cantidad * ing.materia_prima.costo_unitario 
            for ing in receta_crackers.ingredientes.all()
        ) / receta_crackers.rendimiento

        producto_barras = Producto.objects.create(
            nombre='Barras de Cereal Integral x20',
            descripcion='Pack de 20 barras de cereal integral con maní',
            categoria='snacks_saludables',
            precio=Decimal('3500.00'),  # Margen ~40%
            costo=costo_barras * 20,
            stock_actual=Decimal('15.00'),
            stock_minimo=Decimal('5.00'),
            receta=receta_barras
        )

        producto_crackers = Producto.objects.create(
            nombre='Crackers Integrales x50',
            descripcion='Pack de 50 crackers integrales crujientes',
            categoria='snacks_saludables',
            precio=Decimal('2800.00'),  # Margen ~45%
            costo=costo_crackers * 50,
            stock_actual=Decimal('20.00'),
            stock_minimo=Decimal('8.00'),
            receta=receta_crackers
        )

        # Producto directo (sin receta)
        producto_mani = Producto.objects.create(
            nombre='Maní Natural 500g',
            descripcion='Maní sin sal, tostado, envase 500g',
            categoria='frutos_secos',
            precio=Decimal('1200.00'),  # Margen 100%
            costo=Decimal('600.00'),  # Costo directo
            stock_actual=Decimal('30.00'),
            stock_minimo=Decimal('10.00')
        )

        self.stdout.write(self.style.SUCCESS(f'✅ {Producto.objects.count()} productos creados'))

        # ===== 5. VENTAS =====
        self.stdout.write('💰 Registrando ventas...')
        
        # Venta 1 - Hace 3 días
        venta1 = Venta.objects.create(
            fecha=timezone.now() - timedelta(days=3),
            cliente='María González',
            usuario=admin,
            total=Decimal('0.00')
        )
        
        VentaDetalle.objects.create(
            venta=venta1,
            producto=producto_barras,
            cantidad=Decimal('2.00'),
            precio_unitario=producto_barras.precio,
            subtotal=producto_barras.precio * 2
        )
        
        VentaDetalle.objects.create(
            venta=venta1,
            producto=producto_mani,
            cantidad=Decimal('3.00'),
            precio_unitario=producto_mani.precio,
            subtotal=producto_mani.precio * 3
        )
        
        venta1.total = sum(d.subtotal for d in venta1.detalles.all())
        venta1.save()

        # Venta 2 - Hace 1 día
        venta2 = Venta.objects.create(
            fecha=timezone.now() - timedelta(days=1),
            cliente='Carlos Rodríguez',
            usuario=admin,
            total=Decimal('0.00')
        )
        
        VentaDetalle.objects.create(
            venta=venta2,
            producto=producto_crackers,
            cantidad=Decimal('4.00'),
            precio_unitario=producto_crackers.precio,
            subtotal=producto_crackers.precio * 4
        )
        
        venta2.total = sum(d.subtotal for d in venta2.detalles.all())
        venta2.save()

        # Venta 3 - Hoy
        venta3 = Venta.objects.create(
            fecha=timezone.now(),
            cliente='Ana Martínez',
            usuario=admin,
            total=Decimal('0.00')
        )
        
        VentaDetalle.objects.create(
            venta=venta3,
            producto=producto_barras,
            cantidad=Decimal('5.00'),
            precio_unitario=producto_barras.precio,
            subtotal=producto_barras.precio * 5
        )

        VentaDetalle.objects.create(
            venta=venta3,
            producto=producto_crackers,
            cantidad=Decimal('2.00'),
            precio_unitario=producto_crackers.precio,
            subtotal=producto_crackers.precio * 2
        )

        VentaDetalle.objects.create(
            venta=venta3,
            producto=producto_mani,
            cantidad=Decimal('6.00'),
            precio_unitario=producto_mani.precio,
            subtotal=producto_mani.precio * 6
        )
        
        venta3.total = sum(d.subtotal for d in venta3.detalles.all())
        venta3.save()

        self.stdout.write(self.style.SUCCESS(f'✅ {Venta.objects.count()} ventas registradas'))

        # ===== RESUMEN =====
        self.stdout.write(self.style.SUCCESS('\n✨ Datos de ejemplo cargados exitosamente!\n'))
        
        total_ingresos = sum(v.total for v in Venta.objects.all())
        total_gastos = sum(c.precio_mayoreo for c in Compra.objects.all())
        ganancia = total_ingresos - total_gastos

        self.stdout.write('📊 Resumen:')
        self.stdout.write(f'  - Materias Primas: {MateriaPrima.objects.count()}')
        self.stdout.write(f'  - Compras: {Compra.objects.count()} (${total_gastos:,.0f})')
        self.stdout.write(f'  - Recetas: {Receta.objects.count()}')
        self.stdout.write(f'  - Productos: {Producto.objects.count()}')
        self.stdout.write(f'  - Ventas: {Venta.objects.count()} (${total_ingresos:,.0f})')
        self.stdout.write(self.style.SUCCESS(f'  - Ganancia: ${ganancia:,.0f}'))
        
        margen = (ganancia / total_ingresos * 100) if total_ingresos > 0 else 0
        self.stdout.write(f'  - Margen: {margen:.1f}%')
        
        self.stdout.write(self.style.SUCCESS('\n🚀 Puedes probar los dashboards ahora!\n'))
