from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from gestion.models import (
    MateriaPrima, Producto, Receta, RecetaMateriaPrima, 
    ConfiguracionCostos
)
from decimal import Decimal

class Command(BaseCommand):
    help = 'Crea datos de ejemplo para probar el sistema de costos'

    def handle(self, *args, **options):
        # Crear usuario admin si no existe
        user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@lino.com',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            user.set_password('admin123')
            user.save()
            self.stdout.write("👤 Usuario admin creado (password: admin123)")

        # Crear materias primas de ejemplo
        materias_primas = [
            {
                'nombre': 'Harina de Avena Orgánica',
                'descripcion': 'Harina de avena integral certificada orgánica',
                'unidad_medida': 'kg',
                'stock_actual': Decimal('50.0'),
                'stock_minimo': Decimal('10.0'),
                'costo_unitario': Decimal('450.0'),  # $450 por kg
                'proveedor': 'Granos del Valle'
            },
            {
                'nombre': 'Aceite de Coco Virgen',
                'descripcion': 'Aceite de coco prensado en frío',
                'unidad_medida': 'l',
                'stock_actual': Decimal('20.0'),
                'stock_minimo': Decimal('5.0'),
                'costo_unitario': Decimal('1200.0'),  # $1200 por litro
                'proveedor': 'Coco Natural'
            },
            {
                'nombre': 'Stevia en Polvo',
                'descripcion': 'Endulzante natural de stevia',
                'unidad_medida': 'kg',
                'stock_actual': Decimal('5.0'),
                'stock_minimo': Decimal('1.0'),
                'costo_unitario': Decimal('2500.0'),  # $2500 por kg
                'proveedor': 'Endulzantes Naturales'
            },
            {
                'nombre': 'Nueces Pecanas',
                'descripcion': 'Nueces pecanas premium',
                'unidad_medida': 'kg',
                'stock_actual': Decimal('15.0'),
                'stock_minimo': Decimal('3.0'),
                'costo_unitario': Decimal('3200.0'),  # $3200 por kg
                'proveedor': 'Frutos Secos del Sur'
            },
            {
                'nombre': 'Cacao en Polvo',
                'descripcion': 'Cacao puro en polvo sin azúcar',
                'unidad_medida': 'kg',
                'stock_actual': Decimal('25.0'),
                'stock_minimo': Decimal('5.0'),
                'costo_unitario': Decimal('850.0'),  # $850 por kg
                'proveedor': 'Cacao Artesanal'
            }
        ]

        materias_creadas = []
        for mp_data in materias_primas:
            mp, created = MateriaPrima.objects.get_or_create(
                nombre=mp_data['nombre'],
                defaults=mp_data
            )
            if created:
                materias_creadas.append(mp.nombre)

        self.stdout.write(f"🥗 Creadas {len(materias_creadas)} materias primas:")
        for nombre in materias_creadas:
            self.stdout.write(f"   • {nombre}")

        # Crear productos de ejemplo
        productos_ejemplo = [
            {
                'nombre': 'Granola Energética 500g',
                'descripcion': 'Granola casera con avena, nueces y cacao',
                'tipo_producto': 'receta',
                'stock': 0,
                'stock_minimo': 10,
                'precio': 800.0,
                'margen_ganancia': Decimal('35.0'),  # 35% de margen
                'actualizar_precio_automatico': True,
                'categoria': 'Desayunos',
                'marca': 'Lino Saludable'
            },
            {
                'nombre': 'Aceite de Coco 250ml',
                'descripcion': 'Aceite de coco fraccionado para venta al público',
                'tipo_producto': 'fraccionamiento',
                'stock': 0,
                'stock_minimo': 20,
                'precio': 350.0,
                'margen_ganancia': Decimal('40.0'),  # 40% de margen
                'actualizar_precio_automatico': True,
                'categoria': 'Aceites',
                'marca': 'Lino Saludable'
            }
        ]

        productos_creados = []
        for prod_data in productos_ejemplo:
            producto, created = Producto.objects.get_or_create(
                nombre=prod_data['nombre'],
                defaults=prod_data
            )
            if created:
                productos_creados.append(producto)

        self.stdout.write(f"🍯 Creados {len(productos_creados)} productos:")
        for producto in productos_creados:
            self.stdout.write(f"   • {producto.nombre} ({producto.tipo_producto})")

        # Configurar producto fraccionado
        aceite_fraccionado = None
        aceite_origen = None
        for producto in productos_creados:
            if producto.tipo_producto == 'fraccionamiento':
                aceite_fraccionado = producto
                aceite_origen = MateriaPrima.objects.filter(nombre__contains='Aceite de Coco').first()
                break

        if aceite_fraccionado and aceite_origen:
            # Configurar fraccionamiento: 1 litro -> 4 botellas de 250ml
            aceite_fraccionado.unidad_compra = 'l'
            aceite_fraccionado.unidad_venta = 'ml'
            aceite_fraccionado.cantidad_origen = Decimal('1.0')  # 1 litro
            aceite_fraccionado.cantidad_fraccion = Decimal('250.0')  # 250ml
            aceite_fraccionado.factor_conversion = Decimal('4.0')  # 4 unidades por litro
            aceite_fraccionado.save()
            
            self.stdout.write("🔄 Configurado fraccionamiento de aceite de coco")

        # Crear receta para granola
        granola = None
        for producto in productos_creados:
            if producto.tipo_producto == 'receta':
                granola = producto
                break

        if granola:
            # Crear receta
            receta, created = Receta.objects.get_or_create(
                nombre='Granola Energética Casera',
                defaults={
                    'descripcion': 'Receta de granola con ingredientes naturales',
                    'activa': True,
                    'creador': user
                }
            )
            
            if created:
                # Agregar el producto a la receta
                receta.productos.add(granola)
                
                # Definir ingredientes para 500g de granola
                ingredientes = [
                    ('Harina de Avena Orgánica', Decimal('0.300')),  # 300g
                    ('Aceite de Coco Virgen', Decimal('0.050')),     # 50ml
                    ('Stevia en Polvo', Decimal('0.020')),           # 20g
                    ('Nueces Pecanas', Decimal('0.100')),            # 100g
                    ('Cacao en Polvo', Decimal('0.030'))             # 30g
                ]
                
                for nombre_mp, cantidad in ingredientes:
                    materia_prima = MateriaPrima.objects.filter(nombre__contains=nombre_mp.split()[0]).first()
                    if materia_prima:
                        RecetaMateriaPrima.objects.get_or_create(
                            receta=receta,
                            materia_prima=materia_prima,
                            defaults={
                                'cantidad': cantidad,
                                'unidad': materia_prima.unidad_medida,
                                'notas': f'Para 500g de {granola.nombre}'
                            }
                        )
                
                self.stdout.write("📝 Creada receta para granola con 5 ingredientes")

        # Calcular costos iniciales
        productos_actualizados = 0
        for producto in Producto.objects.filter(tipo_producto__in=['receta', 'fraccionamiento']):
            if producto.actualizar_costos_y_precios(usuario=user, motivo="Inicialización del sistema"):
                productos_actualizados += 1

        self.stdout.write(f"💰 Actualizados costos de {productos_actualizados} productos")

        # Mostrar resumen de costos
        self.stdout.write("\n📊 RESUMEN DE COSTOS CALCULADOS:")
        for producto in Producto.objects.filter(tipo_producto__in=['receta', 'fraccionamiento']):
            costo = producto.calcular_costo_unitario()
            precio = producto.calcular_precio_venta()
            margen_real = ((precio - costo) / costo * 100) if costo > 0 else 0
            
            self.stdout.write(
                f"   • {producto.nombre}:\n"
                f"     - Costo: ${costo:.2f}\n"
                f"     - Precio: ${precio:.2f}\n"
                f"     - Margen: {margen_real:.1f}%"
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"\n✅ Sistema de costos inicializado exitosamente!\n"
                f"🎯 Datos creados:\n"
                f"   • {len(materias_creadas)} materias primas\n"
                f"   • {len(productos_creados)} productos\n"
                f"   • 1 receta con ingredientes\n"
                f"   • 1 producto fraccionado\n\n"
                f"🌐 Accede al admin en: http://localhost:8000/admin/\n"
                f"👤 Usuario: admin | Contraseña: admin123"
            )
        )
