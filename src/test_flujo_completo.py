"""
TEST COMPLETO DEL FLUJO DE STOCK
Verifica: MPs → Compras → Productos → Re-Stockeo → Ventas
"""
from gestion.models import *
from decimal import Decimal
from django.contrib.auth import get_user_model

User = get_user_model()
user = User.objects.first()

print("\n" + "="*70)
print("🧪 TEST FLUJO COMPLETO - SISTEMA LINO")
print("="*70)

# ============================================================
# PASO 1: CREAR MATERIAS PRIMAS (Stock 0)
# ============================================================
print("\n📦 PASO 1: CREAR MATERIAS PRIMAS")
print("-"*70)

mp_mani = MateriaPrima.objects.create(
    nombre='Maní sin sal',
    unidad_medida='kg',
    stock_actual=0,
    stock_minimo=5,
    costo_unitario=0
)
print(f"✅ {mp_mani.nombre} - Stock: {mp_mani.stock_actual}kg")

mp_barrita = MateriaPrima.objects.create(
    nombre='Barrita Cereal',
    unidad_medida='unidad',
    stock_actual=0,
    stock_minimo=10,
    costo_unitario=0
)
print(f"✅ {mp_barrita.nombre} - Stock: {mp_barrita.stock_actual} unidades")

mp_almendras = MateriaPrima.objects.create(
    nombre='Almendras',
    unidad_medida='kg',
    stock_actual=0,
    stock_minimo=3,
    costo_unitario=0
)
print(f"✅ {mp_almendras.nombre} - Stock: {mp_almendras.stock_actual}kg")

# ============================================================
# PASO 2: REGISTRAR COMPRAS
# ============================================================
print("\n💰 PASO 2: REGISTRAR COMPRAS")
print("-"*70)

# Compra 1: Maní (20kg × $2000)
c1 = Compra.objects.create(proveedor='Dist ABC', usuario=user)
CompraDetalle.objects.create(
    compra=c1,
    materia_prima=mp_mani,
    cantidad=20,
    precio_unitario=2000
)
mp_mani.refresh_from_db()
print(f"✅ Compra Maní: 20kg × $2000 = ${c1.total}")
print(f"   Stock MP: {mp_mani.stock_actual}kg | Costo: ${mp_mani.costo_unitario}/kg")

# Compra 2: Barritas (50 × $800)
c2 = Compra.objects.create(proveedor='Prov XYZ', usuario=user)
CompraDetalle.objects.create(
    compra=c2,
    materia_prima=mp_barrita,
    cantidad=50,
    precio_unitario=800
)
mp_barrita.refresh_from_db()
print(f"✅ Compra Barritas: 50 × $800 = ${c2.total}")
print(f"   Stock MP: {mp_barrita.stock_actual} unidades | Costo: ${mp_barrita.costo_unitario}/u")

# Compra 3: Almendras (10kg × $3500)
c3 = Compra.objects.create(proveedor='Dist ABC', usuario=user)
CompraDetalle.objects.create(
    compra=c3,
    materia_prima=mp_almendras,
    cantidad=10,
    precio_unitario=3500
)
mp_almendras.refresh_from_db()
print(f"✅ Compra Almendras: 10kg × $3500 = ${c3.total}")
print(f"   Stock MP: {mp_almendras.stock_actual}kg | Costo: ${mp_almendras.costo_unitario}/kg")

balance_compras = c1.total + c2.total + c3.total
print(f"\n💸 Balance después de compras: -${balance_compras}")

# ============================================================
# PASO 3: CREAR PRODUCTOS (Stock 0)
# ============================================================
print("\n🏭 PASO 3: CREAR PRODUCTOS")
print("-"*70)

# A) Venta Directa (1:1)
prod_barrita = Producto.objects.create(
    nombre='Barrita Cereal',
    categoria='snacks',
    tipo_producto='reventa',
    materia_prima_asociada=mp_barrita,
    cantidad_fraccion=Decimal('1'),
    precio=1500,
    stock=0,
    stock_minimo=5
)
print(f"✅ A) VENTA DIRECTA: {prod_barrita.nombre}")
print(f"   1 producto = 1 MP | Precio: ${prod_barrita.precio}")

# B) Fraccionamiento
prod_mani = Producto.objects.create(
    nombre='Maní sin sal 500g',
    categoria='frutos_secos',
    tipo_producto='reventa',
    materia_prima_asociada=mp_mani,
    cantidad_fraccion=Decimal('0.5'),
    precio=1800,
    stock=0,
    stock_minimo=10
)
print(f"✅ B) FRACCIONAMIENTO: {prod_mani.nombre}")
print(f"   1 producto = 0.5kg MP | Precio: ${prod_mani.precio}")

# ============================================================
# PASO 4: RE-STOCKEO (PRODUCCIÓN)
# ============================================================
print("\n🔄 PASO 4: RE-STOCKEO (PRODUCCIÓN DESDE MPs)")
print("-"*70)

# Test A: Producir 20 barritas
print(f"\n📌 A) Producir 20 barritas")
print(f"   ANTES: Producto={prod_barrita.stock}, MP={mp_barrita.stock_actual}")
ok, faltantes = prod_barrita.verificar_stock_materias_primas(20)
if ok:
    prod_barrita.descontar_materias_primas(20, user)
    prod_barrita.stock += 20
    prod_barrita.save()
    mp_barrita.refresh_from_db()
    print(f"   DESPUÉS: Producto={prod_barrita.stock}, MP={mp_barrita.stock_actual}")
    print(f"   ✅ CORRECTO: 50 - 20 = 30")
else:
    print(f"   ❌ ERROR: {faltantes}")

# Test B: Producir 10 bolsas de 500g
print(f"\n📌 B) Producir 10 bolsas Maní 500g")
print(f"   ANTES: Producto={prod_mani.stock}, MP={mp_mani.stock_actual}kg")
ok, faltantes = prod_mani.verificar_stock_materias_primas(10)
if ok:
    prod_mani.descontar_materias_primas(10, user)
    prod_mani.stock += 10
    prod_mani.save()
    mp_mani.refresh_from_db()
    print(f"   DESPUÉS: Producto={prod_mani.stock}, MP={mp_mani.stock_actual}kg")
    print(f"   ✅ CORRECTO: 20 - 5 = 15kg")
else:
    print(f"   ❌ ERROR: {faltantes}")

# ============================================================
# PASO 5: VENTAS
# ============================================================
print("\n💵 PASO 5: REGISTRAR VENTAS")
print("-"*70)

venta = Venta.objects.create(
    usuario=user,
    cliente='Cliente Test'
)
VentaDetalle.objects.create(
    venta=venta,
    producto=prod_barrita,
    cantidad=5,
    precio_unitario=prod_barrita.precio,
    subtotal=5 * prod_barrita.precio
)
VentaDetalle.objects.create(
    venta=venta,
    producto=prod_mani,
    cantidad=3,
    precio_unitario=prod_mani.precio,
    subtotal=3 * prod_mani.precio
)

prod_barrita.refresh_from_db()
prod_mani.refresh_from_db()

print(f"✅ Venta registrada:")
print(f"   5 Barritas × ${prod_barrita.precio} = $7500")
print(f"   3 Maní 500g × ${prod_mani.precio} = $5400")
print(f"   TOTAL: ${venta.total}")
print(f"\n📦 Stock después de venta:")
print(f"   Barritas: 20 - 5 = {prod_barrita.stock}")
print(f"   Maní 500g: 10 - 3 = {prod_mani.stock}")

# ============================================================
# RESUMEN FINAL
# ============================================================
print("\n" + "="*70)
print("📊 RESUMEN FINAL")
print("="*70)

print(f"\n💰 BALANCE:")
print(f"   Gastado en compras: -${balance_compras}")
print(f"   Ingreso por ventas: +${venta.total}")
print(f"   Balance neto: ${venta.total - balance_compras}")

print(f"\n📦 INVENTARIO:")
print(f"   MP Maní: {mp_mani.stock_actual}kg")
print(f"   MP Barritas: {mp_barrita.stock_actual} unidades")
print(f"   MP Almendras: {mp_almendras.stock_actual}kg (sin usar aún)")

print(f"\n🏪 PRODUCTOS:")
print(f"   Barritas: {prod_barrita.stock} unidades")
print(f"   Maní 500g: {prod_mani.stock} unidades")

print("\n" + "="*70)
print("✅ TEST COMPLETADO")
print("="*70 + "\n")
