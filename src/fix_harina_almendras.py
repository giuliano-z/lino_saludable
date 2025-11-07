#!/usr/bin/env python
"""
Script para CORREGIR el producto "Harina de Almendras" en Railway
Ejecutar: python src/fix_harina_almendras.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lino_saludable.settings')
django.setup()

from gestion.models import Producto, MateriaPrima
from decimal import Decimal


def fix_harina_almendras():
    print("\n" + "="*80)
    print(" CORRECCIÓN: Harina de Almendras")
    print("="*80)
    
    try:
        # Buscar el producto
        producto = Producto.objects.get(nombre__icontains="Harina de Almendras")
        
        print(f"\n✅ Producto encontrado: {producto.nombre} (ID: {producto.id})")
        
        if producto.materia_prima_asociada:
            mp = producto.materia_prima_asociada
            
            print(f"\nESTADO ACTUAL:")
            print(f"  Materia Prima: {mp.nombre}")
            print(f"  Unidad MP: {mp.get_unidad_medida_display()}")
            print(f"  Costo unitario MP: ${mp.costo_unitario}")
            print(f"  Cantidad fracción: {producto.cantidad_fraccion}")
            print(f"  Costo calculado: ${producto.calcular_costo_real()}")
            print(f"  Precio venta: ${producto.precio}")
            print(f"  Margen: {producto.calcular_margen_real()}%")
            
            # Detectar el problema
            if producto.cantidad_fraccion > 100:
                print(f"\n⚠️  PROBLEMA DETECTADO:")
                print(f"   cantidad_fraccion = {producto.cantidad_fraccion}")
                print(f"   Esto parece estar en gramos cuando debería estar en kg")
                
                # Calcular valor corregido
                # Si la MP está en kg y queremos 500gr, debería ser 0.5
                cantidad_corregida = producto.cantidad_fraccion / 1000
                
                print(f"\n🔧 CORRECCIÓN PROPUESTA:")
                print(f"   Cambiar cantidad_fraccion de {producto.cantidad_fraccion} a {cantidad_corregida}")
                
                # Calcular cómo quedaría
                costo_nuevo = mp.costo_unitario * Decimal(str(cantidad_corregida))
                margen_nuevo = ((Decimal(str(producto.precio)) - costo_nuevo) / Decimal(str(producto.precio))) * 100
                
                print(f"\n   Nuevo costo: ${costo_nuevo}")
                print(f"   Nuevo margen: {margen_nuevo:.2f}%")
                
                # Aplicar corrección
                print(f"\n🚀 Aplicando corrección...")
                producto.cantidad_fraccion = Decimal(str(cantidad_corregida))
                producto.save()
                
                print(f"\n✅ ¡CORRECCIÓN APLICADA!")
                
                # Verificar
                producto.refresh_from_db()
                print(f"\nESTADO FINAL:")
                print(f"  Cantidad fracción: {producto.cantidad_fraccion}")
                print(f"  Costo calculado: ${producto.calcular_costo_real()}")
                print(f"  Margen: {producto.calcular_margen_real()}%")
                
                return True
            else:
                print(f"\n✅ El producto ya está correcto")
                return True
        else:
            print(f"\n❌ El producto no tiene materia prima asociada")
            return False
            
    except Producto.DoesNotExist:
        print(f"\n❌ No se encontró el producto 'Harina de Almendras'")
        print(f"\nProductos disponibles:")
        for p in Producto.objects.all():
            print(f"  • {p.nombre}")
        return False
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    import sys
    success = fix_harina_almendras()
    sys.exit(0 if success else 1)
