#!/usr/bin/env python
"""
Script de ayuda para cargar datos reales en LINO
Puedes modificar este script con tus datos o usar el admin de Django
"""
import os
import sys
import django
from decimal import Decimal
from datetime import datetime, timedelta

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lino_saludable.settings')
django.setup()

from gestion.models import MateriaPrima, Producto, Compra, Venta, VentaDetalle, Receta
from django.contrib.auth import get_user_model

User = get_user_model()

def cargar_ejemplo():
    """
    Función de ejemplo - MODIFICA ESTO CON TUS DATOS REALES
    """
    print("\n" + "="*60)
    print("📦 CARGA DE DATOS REALES - LINO SALUDABLE")
    print("="*60 + "\n")
    
    # Obtener usuario admin
    admin = User.objects.first()
    if not admin:
        print("❌ No hay usuarios. Crea un superusuario primero:")
        print("   python manage.py createsuperuser")
        return
    
    print(f"👤 Usuario admin: {admin.username}\n")
    
    # =====================================================
    # EJEMPLO 1: CREAR MATERIA PRIMA
    # =====================================================
    print("1️⃣ Creando materia prima de ejemplo...")
    
    materia = MateriaPrima.objects.create(
        nombre="Harina Integral Orgánica",
        unidad_medida="kg",
        costo_unitario=Decimal("450.00"),  # Precio por kg
        stock_actual=Decimal("25.00"),     # 25 kg en stock
        stock_minimo=Decimal("10.00"),     # Alerta si baja de 10kg
        proveedor="Proveedor Ejemplo SA",
        activo=True
    )
    print(f"   ✅ Creada: {materia.nombre} (${materia.costo_unitario}/kg)")
    
    # =====================================================
    # EJEMPLO 2: CREAR PRODUCTO PARA VENTA
    # =====================================================
    print("\n2️⃣ Creando producto para venta...")
    
    producto = Producto.objects.create(
        nombre="Mix de Semillas 500g",
        descripcion="Mix nutritivo de semillas orgánicas",
        precio=Decimal("850.00"),          # Precio de venta
        stock=50,                          # 50 unidades
        categoria="Semillas",
        activo=True
    )
    print(f"   ✅ Creado: {producto.nombre} (${producto.precio} c/u)")
    
    # =====================================================
    # EJEMPLO 3: REGISTRAR COMPRA
    # =====================================================
    print("\n3️⃣ Registrando compra de materia prima...")
    
    compra = Compra.objects.create(
        materia_prima=materia,
        cantidad=Decimal("10.00"),         # Compró 10 kg
        precio_mayoreo=Decimal("4500.00"), # Pagó $4500 total
        proveedor=materia.proveedor,
        fecha_compra=datetime.now().date()
    )
    # Actualizar stock
    materia.stock_actual += compra.cantidad
    materia.save()
    
    print(f"   ✅ Compra registrada: {compra.cantidad}kg por ${compra.precio_mayoreo}")
    print(f"   📦 Stock actualizado: {materia.stock_actual}kg")
    
    # =====================================================
    # EJEMPLO 4: REGISTRAR VENTA
    # =====================================================
    print("\n4️⃣ Registrando venta...")
    
    venta = Venta.objects.create(
        cliente="Cliente Ejemplo",
        total=Decimal("0"),  # Se calculará
        usuario=admin,
        fecha=datetime.now()
    )
    
    # Agregar productos a la venta
    detalle = VentaDetalle.objects.create(
        venta=venta,
        producto=producto,
        cantidad=3,                        # Vendió 3 unidades
        precio_unitario=producto.precio,
        subtotal=producto.precio * 3
    )
    
    # Actualizar total y stock
    venta.total = detalle.subtotal
    venta.save()
    
    producto.stock -= detalle.cantidad
    producto.save()
    
    print(f"   ✅ Venta creada: {detalle.cantidad}x {producto.nombre}")
    print(f"   💰 Total: ${venta.total}")
    print(f"   📦 Stock restante: {producto.stock} unidades")
    
    # =====================================================
    # RESUMEN
    # =====================================================
    print("\n" + "="*60)
    print("✅ DATOS DE EJEMPLO CARGADOS")
    print("="*60)
    print(f"\n📊 Estado actual:")
    print(f"   - Materias Primas: {MateriaPrima.objects.count()}")
    print(f"   - Productos: {Producto.objects.count()}")
    print(f"   - Compras: {Compra.objects.count()}")
    print(f"   - Ventas: {Venta.objects.count()}")
    
    print("\n💡 TIP: Modifica este script con tus datos reales")
    print("   O usa el admin: http://127.0.0.1:8000/admin/\n")


# =====================================================
# PLANTILLA PARA TUS DATOS REALES
# =====================================================
def cargar_mis_datos():
    """
    USA ESTA FUNCIÓN PARA CARGAR TUS DATOS REALES
    Descomenta y completa con tus datos
    """
    
    admin = User.objects.first()
    
    # TUS MATERIAS PRIMAS
    # materias_primas = [
    #     {
    #         'nombre': 'Nombre de tu materia prima',
    #         'unidad_medida': 'kg',  # o 'lt', 'unidad', etc
    #         'costo_unitario': Decimal('100.00'),
    #         'stock_actual': Decimal('50.00'),
    #         'stock_minimo': Decimal('10.00'),
    #         'proveedor': 'Tu Proveedor',
    #     },
    #     # Agrega más aquí...
    # ]
    # 
    # for mp_data in materias_primas:
    #     MateriaPrima.objects.create(**mp_data)
    #     print(f"✅ Creada: {mp_data['nombre']}")
    
    # TUS PRODUCTOS
    # productos = [
    #     {
    #         'nombre': 'Nombre de tu producto',
    #         'descripcion': 'Descripción',
    #         'precio': Decimal('500.00'),
    #         'stock': 100,
    #         'categoria': 'Categoría',
    #     },
    #     # Agrega más aquí...
    # ]
    # 
    # for prod_data in productos:
    #     Producto.objects.create(**prod_data)
    #     print(f"✅ Creado: {prod_data['nombre']}")
    
    print("\n💡 Descomenta y completa cargar_mis_datos() con tus datos")


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--ejemplo':
        cargar_ejemplo()
    elif len(sys.argv) > 1 and sys.argv[1] == '--mis-datos':
        cargar_mis_datos()
    else:
        print("\n" + "="*60)
        print("📦 SCRIPT DE CARGA DE DATOS - LINO SALUDABLE")
        print("="*60)
        print("\nUso:")
        print("  python cargar_datos_reales.py --ejemplo      # Carga datos de ejemplo")
        print("  python cargar_datos_reales.py --mis-datos    # Carga tus datos (modifica antes)")
        print("\nO usa el admin de Django: http://127.0.0.1:8000/admin/")
        print()
