"""
Comando Django para cargar datos de ejemplo simples
Uso: python manage.py cargar_ejemplo_simple
"""
from django.core.management.base import BaseCommand
from gestion.models import (
    Producto, MateriaPrima, Compra, Venta, VentaDetalle
)
from decimal import Decimal
from datetime import timedelta
from django.utils import timezone


class Command(BaseCommand):
    help = 'Carga datos de ejemplo simples en la base de datos'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('\n🌱 Cargando datos de ejemplo simples...\n'))

        # ===== 1. MATERIAS PRIMAS =====
        self.stdout.write('📦 Creando materias primas...')
        
        harina = MateriaPrima.objects.create(
            nombre='Harina Integral',
            descripcion='Harina integral orgánica',
            unidad_medida='KG',
            costo_unitario=Decimal('450.00'),
            stock_actual=Decimal('50.00'),
            stock_minimo=Decimal('10.00')
        )
        
        avena = MateriaPrima.objects.create(
            nombre='Avena Arrollada',
            descripcion='Avena en hojuelas',
            unidad_medida='KG',
            costo_unitario=Decimal('350.00'),
            stock_actual=Decimal('40.00'),
            stock_minimo=Decimal('8.00')
        )
        
        mani = MateriaPrima.objects.create(
            nombre='Maní Natural',
            descripcion='Maní sin sal',
            unidad_medida='KG',
            costo_unitario=Decimal('600.00'),
            stock_actual=Decimal('30.00'),
            stock_minimo=Decimal('5.00')
        )
        
        aceite = MateriaPrima.objects.create(
            nombre='Aceite de Coco',
            descripcion='Aceite de coco virgen',
            unidad_medida='LT',
            costo_unitario=Decimal('850.00'),
            stock_actual=Decimal('20.00'),
            stock_minimo=Decimal('3.00')
        )
        
        self.stdout.write(self.style.SUCCESS(f'✅ {MateriaPrima.objects.count()} materias primas creadas'))

        # ===== 2. COMPRAS =====
        self.stdout.write('🛒 Registrando compras...')
        
        Compra.objects.create(
            materia_prima=harina,
            proveedor='Proveedor A',
            cantidad_mayoreo=Decimal('50.00'),
            precio_mayoreo=Decimal('22500.00')  # 50kg x $450
        )
        
        Compra.objects.create(
            materia_prima=avena,
            proveedor='Proveedor B',
            cantidad_mayoreo=Decimal('40.00'),
            precio_mayoreo=Decimal('14000.00')  # 40kg x $350
        )
        
        Compra.objects.create(
            materia_prima=mani,
            proveedor='Proveedor C',
            cantidad_mayoreo=Decimal('30.00'),
            precio_mayoreo=Decimal('18000.00')  # 30kg x $600
        )
        
        self.stdout.write(self.style.SUCCESS(f'✅ {Compra.objects.count()} compras registradas'))

        # ===== 3. PRODUCTOS =====
        self.stdout.write('📦 Creando productos...')
        
        # Productos simples sin receta
        producto1 = Producto.objects.create(
            nombre='Maní Natural 500g',
            descripcion='Maní sin sal, tostado, envase 500g',
            categoria='frutos_secos',
            precio=1200.00,  # FloatField
            stock=30,  # IntegerField
            stock_minimo=10,
            marca='Lino Saludable',
            materia_prima_asociada=mani,
            tipo_producto='reventa',
            cantidad_fraccion=500  # 500 gramos
        )
        
        producto2 = Producto.objects.create(
            nombre='Harina Integral 1kg',
            descripcion='Harina integral orgánica envasada',
            categoria='harinas_especiales',
            precio=680.00,
            stock=45,
            stock_minimo=15,
            marca='Lino Saludable',
            materia_prima_asociada=harina,
            tipo_producto='reventa',
            cantidad_fraccion=1000  # 1000 gramos = 1kg
        )
        
        producto3 = Producto.objects.create(
            nombre='Avena Arrollada 500g',
            descripcion='Avena en hojuelas, envase 500g',
            categoria='cereales',
            precio=520.00,
            stock=40,
            stock_minimo=12,
            marca='Lino Saludable',
            materia_prima_asociada=avena,
            tipo_producto='reventa',
            cantidad_fraccion=500  # 500 gramos
        )
        
        self.stdout.write(self.style.SUCCESS(f'✅ {Producto.objects.count()} productos creados'))

        # ===== 4. VENTAS =====
        self.stdout.write('💰 Registrando ventas...')
        
        # Venta 1 - Hace 3 días
        venta1 = Venta.objects.create(
            fecha=timezone.now() - timedelta(days=3),
            total=Decimal('3600.00')
        )
        
        VentaDetalle.objects.create(
            venta=venta1,
            producto=producto1,
            cantidad=2,
            precio_unitario=Decimal('1200.00'),
            subtotal=Decimal('2400.00')
        )
        
        VentaDetalle.objects.create(
            venta=venta1,
            producto=producto2,
            cantidad=1,
            precio_unitario=Decimal('680.00'),
            subtotal=Decimal('680.00')
        )
        
        VentaDetalle.objects.create(
            venta=venta1,
            producto=producto3,
            cantidad=1,
            precio_unitario=Decimal('520.00'),
            subtotal=Decimal('520.00')
        )
        
        # Venta 2 - Hace 2 días
        venta2 = Venta.objects.create(
            fecha=timezone.now() - timedelta(days=2),
            total=Decimal('4240.00')
        )
        
        VentaDetalle.objects.create(
            venta=venta2,
            producto=producto1,
            cantidad=3,
            precio_unitario=Decimal('1200.00'),
            subtotal=Decimal('3600.00')
        )
        
        VentaDetalle.objects.create(
            venta=venta2,
            producto=producto3,
            cantidad=1,
            precio_unitario=Decimal('520.00'),
            subtotal=Decimal('520.00')
        )
        
        VentaDetalle.objects.create(
            venta=venta2,
            producto=producto2,
            cantidad=2,
            precio_unitario=Decimal('680.00'),
            subtotal=Decimal('1360.00')
        )
        
        # Venta 3 - Hoy
        venta3 = Venta.objects.create(
            fecha=timezone.now(),
            total=Decimal('2720.00')
        )
        
        VentaDetalle.objects.create(
            venta=venta3,
            producto=producto2,
            cantidad=4,
            precio_unitario=Decimal('680.00'),
            subtotal=Decimal('2720.00')
        )
        
        self.stdout.write(self.style.SUCCESS(f'✅ {Venta.objects.count()} ventas registradas'))
        
        # ===== RESUMEN =====
        self.stdout.write(self.style.SUCCESS('\n✨ Datos cargados exitosamente!\n'))
        self.stdout.write(self.style.SUCCESS('📊 Resumen:'))
        self.stdout.write(f'  - Materias Primas: {MateriaPrima.objects.count()}')
        self.stdout.write(f'  - Compras: {Compra.objects.count()}')
        self.stdout.write(f'  - Productos: {Producto.objects.count()}')
        self.stdout.write(f'  - Ventas: {Venta.objects.count()}')
        self.stdout.write(f'  - Detalles de Venta: {VentaDetalle.objects.count()}\n')
        
        # Mostrar cálculos
        total_ventas = sum(v.total for v in Venta.objects.all())
        total_compras = sum(c.precio_mayoreo for c in Compra.objects.all())
        
        self.stdout.write(self.style.SUCCESS('💰 Totales:'))
        self.stdout.write(f'  - Total Ventas: ${total_ventas:,.2f}')
        self.stdout.write(f'  - Total Compras: ${total_compras:,.2f}\n')
