"""
TEST DE MÉTRICAS DEL DASHBOARD
Verifica que los KPIs, gráficos y tablas muestren datos correctos
"""
from gestion.models import *
from django.db.models import Sum, Count, F
from decimal import Decimal
from datetime import datetime, timedelta
from django.utils import timezone

print("\n" + "="*70)
print("📊 VERIFICACIÓN DE MÉTRICAS DEL DASHBOARD")
print("="*70)

# ============================================================
# 1. KPIs PRINCIPALES
# ============================================================
print("\n1️⃣ KPIs PRINCIPALES:")
print("-"*70)

hoy = timezone.now()
primer_dia = hoy.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

# Ventas del mes
ventas_mes = Venta.objects.filter(fecha__gte=primer_dia).aggregate(
    total=Sum('total'),
    cantidad=Count('id')
)
total_ventas = ventas_mes['total'] or 0
cant_ventas = ventas_mes['cantidad']
print(f"💵 Ventas del mes:")
print(f"   Total: ${total_ventas:,.2f}")
print(f"   Cantidad: {cant_ventas} ventas")

# Compras del mes
compras_mes = Compra.objects.filter(fecha_compra__gte=primer_dia.date()).aggregate(
    total=Sum('total'),
    cantidad=Count('id')
)
total_compras = compras_mes['total'] or 0
cant_compras = compras_mes['cantidad']
print(f"\n📦 Compras del mes:")
print(f"   Total: ${total_compras:,.2f}")
print(f"   Cantidad: {cant_compras} compras")

# Stock bajo
productos_stock_bajo = Producto.objects.filter(
    stock__lte=F('stock_minimo')
).count()
print(f"\n⚠️  Productos con stock bajo: {productos_stock_bajo}")

mps_stock_bajo = MateriaPrima.objects.filter(
    stock_actual__lte=F('stock_minimo')
).count()
print(f"⚠️  Materias primas con stock bajo: {mps_stock_bajo}")

# ============================================================
# 2. GRÁFICO DE VENTAS (últimos 7 días)
# ============================================================
print("\n\n2️⃣ DATOS PARA GRÁFICO DE VENTAS (últimos 7 días):")
print("-"*70)
for i in range(6, -1, -1):
    dia = hoy - timedelta(days=i)
    ventas_dia = Venta.objects.filter(
        fecha__date=dia.date()
    ).aggregate(total=Sum('total'))
    total = ventas_dia['total'] or 0
    print(f"{dia.strftime('%d/%m')}: ${total:,.2f}")

# ============================================================
# 3. TOP PRODUCTOS MÁS VENDIDOS
# ============================================================
print("\n\n3️⃣ TOP 5 PRODUCTOS MÁS VENDIDOS (mes actual):")
print("-"*70)
top_productos = VentaDetalle.objects.filter(
    venta__fecha__gte=primer_dia
).values(
    'producto__nombre'
).annotate(
    cantidad=Sum('cantidad'),
    total=Sum('subtotal')
).order_by('-cantidad')[:5]

if top_productos:
    for i, p in enumerate(top_productos, 1):
        print(f"{i}. {p['producto__nombre']}")
        print(f"   Cantidad: {p['cantidad']} unidades")
        print(f"   Total: ${p['total']:,.2f}")
else:
    print("   Sin ventas en el período")

# ============================================================
# 4. MATERIAS PRIMAS CON STOCK CRÍTICO
# ============================================================
print("\n\n4️⃣ MATERIAS PRIMAS CON STOCK CRÍTICO:")
print("-"*70)
mps_criticas = MateriaPrima.objects.filter(
    stock_actual__lte=F('stock_minimo')
).order_by('stock_actual')

if mps_criticas:
    for mp in mps_criticas:
        porcentaje = (mp.stock_actual / mp.stock_minimo * 100) if mp.stock_minimo > 0 else 0
        print(f"⚠️  {mp.nombre}")
        print(f"   Stock: {mp.stock_actual} {mp.unidad_medida}")
        print(f"   Mínimo: {mp.stock_minimo} {mp.unidad_medida}")
        print(f"   Estado: {porcentaje:.1f}% del mínimo")
else:
    print("   ✅ Todas las materias primas con stock adecuado")

# ============================================================
# 5. ÚLTIMAS VENTAS
# ============================================================
print("\n\n5️⃣ ÚLTIMAS 5 VENTAS:")
print("-"*70)
ultimas_ventas = Venta.objects.order_by('-fecha')[:5]

if ultimas_ventas:
    for v in ultimas_ventas:
        cliente_nombre = v.cliente if isinstance(v.cliente, str) else "Sin cliente"
        print(f"#{v.id} - {v.fecha.strftime('%d/%m/%Y %H:%M')}")
        print(f"   Cliente: {cliente_nombre}")
        print(f"   Total: ${v.total:,.2f}")
        detalles = v.detalles.count()
        print(f"   Items: {detalles}")
else:
    print("   Sin ventas registradas")

# ============================================================
# 6. BALANCE GENERAL
# ============================================================
print("\n\n6️⃣ BALANCE GENERAL:")
print("-"*70)
total_ventas_hist = Venta.objects.aggregate(total=Sum('total'))['total'] or 0
total_compras_hist = Compra.objects.aggregate(total=Sum('total'))['total'] or 0
balance = total_ventas_hist - total_compras_hist

print(f"💰 Total ventas históricas: ${total_ventas_hist:,.2f}")
print(f"💸 Total compras históricas: ${total_compras_hist:,.2f}")
print(f"📊 Balance neto: ${balance:,.2f}")

# ============================================================
# 7. PRODUCTOS CON STOCK BAJO
# ============================================================
print("\n\n7️⃣ PRODUCTOS CON STOCK BAJO:")
print("-"*70)
productos_criticos = Producto.objects.filter(
    stock__lte=F('stock_minimo')
).order_by('stock')

if productos_criticos:
    for p in productos_criticos:
        porcentaje = (p.stock / p.stock_minimo * 100) if p.stock_minimo > 0 else 0
        print(f"⚠️  {p.nombre}")
        print(f"   Stock: {p.stock} unidades")
        print(f"   Mínimo: {p.stock_minimo} unidades")
        print(f"   Estado: {porcentaje:.1f}% del mínimo")
else:
    print("   ✅ Todos los productos con stock adecuado")

print("\n" + "="*70)
print("✅ Verificación completada")
print("="*70 + "\n")
