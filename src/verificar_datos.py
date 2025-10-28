import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lino_saludable.settings')
django.setup()

from gestion.models import MateriaPrima, Producto

print('=== RESUMEN DE DATOS CREADOS ===')
print(f'📦 Materias Primas: {MateriaPrima.objects.count()}')
print(f'🛍️ Productos: {Producto.objects.count()}')
print()

print('=== ALGUNAS MATERIAS PRIMAS ===')
for mp in MateriaPrima.objects.all()[:5]:
    print(f'{mp.nombre}: ${mp.costo_unitario} ({mp.unidad_medida}) - Stock: {mp.stock_actual}')
print()

print('=== ALGUNOS PRODUCTOS ===')
for p in Producto.objects.all()[:5]:
    print(f'{p.nombre}: ${p.precio} - Stock: {p.stock} - Categoría: {p.categoria}')
print()

print('=== PRODUCTOS SIN TACC ===')
sin_tacc = Producto.objects.filter(atributos_dieteticos__contains='sin_tacc')
print(f'Productos Sin TACC: {sin_tacc.count()}')
for p in sin_tacc[:3]:
    print(f'- {p.nombre}: ${p.precio}')
print()

print('=== PRODUCTOS ORGÁNICOS ===')
organicos = Producto.objects.filter(atributos_dieteticos__contains='organico')
print(f'Productos Orgánicos: {organicos.count()}')
for p in organicos[:3]:
    print(f'- {p.nombre}: ${p.precio}')
