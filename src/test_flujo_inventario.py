#!/usr/bin/env python
"""
Script de Testing Completo - Flujo de Inventario LINO
======================================================

Prueba el flujo completo:
1. Compra → Inventario (promedio ponderado)
2. Producto SIN receta → Descuento inventario
3. Producto CON receta → Descuento múltiple
4. Edición de stock → Descuento adicional
5. Venta → Solo afecta stock producto

Autor: Claude (Anthropic)
Fecha: 29 de octubre de 2025
"""

import os
import django
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lino_saludable.settings')
django.setup()

from gestion.models import (
    MateriaPrima, Producto, Receta, RecetaMateriaPrima,
    Compra, Venta, VentaDetalle
)
from django.contrib.auth.models import User
from django.utils import timezone


class TestInventarioCompleto:
    """Suite de testing para el flujo de inventario"""
    
    def __init__(self):
        self.resultados = []
        self.errores = []
        
    def log(self, mensaje, tipo="INFO"):
        """Registra un mensaje"""
        simbolos = {
            "INFO": "ℹ️",
            "SUCCESS": "✅",
            "ERROR": "❌",
            "WARNING": "⚠️",
            "TEST": "🧪",
            "DATA": "📊"
        }
        print(f"{simbolos.get(tipo, '•')} {mensaje}")
        self.resultados.append((tipo, mensaje))
    
    def verificar(self, condicion, mensaje_exito, mensaje_error):
        """Verifica una condición y registra el resultado"""
        if condicion:
            self.log(mensaje_exito, "SUCCESS")
            return True
        else:
            self.log(mensaje_error, "ERROR")
            self.errores.append(mensaje_error)
            return False
    
    def limpiar_datos_test(self):
        """Limpia datos de tests anteriores"""
        self.log("Limpiando datos de tests anteriores...", "INFO")
        
        # Eliminar en orden (respetando foreign keys)
        VentaDetalle.objects.filter(producto__nombre__contains="TEST").delete()
        Venta.objects.filter(cliente__contains="TEST").delete()
        RecetaMateriaPrima.objects.filter(receta__nombre__contains="TEST").delete()
        Receta.objects.filter(nombre__contains="TEST").delete()
        Producto.objects.filter(nombre__contains="TEST").delete()
        Compra.objects.filter(materia_prima__nombre__contains="TEST").delete()
        MateriaPrima.objects.filter(nombre__contains="TEST").delete()
        
        self.log("Datos de test limpiados", "SUCCESS")
    
    def crear_datos_base(self):
        """Crea categorías y proveedor necesarios"""
        self.log("Creando datos base...", "INFO")
        
        # Usar categoría existente
        self.categoria = "frutos_secos"
        
        # Proveedor será un string
        self.proveedor = "TEST - Proveedor Demo"
        
        self.log("Datos base creados", "SUCCESS")
    
    def test_1_crear_materias_primas(self):
        """Test 1: Crear materias primas en inventario"""
        self.log("\n" + "="*60, "TEST")
        self.log("TEST 1: Crear Materias Primas", "TEST")
        self.log("="*60, "TEST")
        
        # Crear 3 materias primas con stock inicial 0
        self.mani = MateriaPrima.objects.create(
            nombre="TEST - Maní sin sal",
            descripcion="Maní crudo sin sal para fraccionamiento",
            unidad_medida="kg",
            stock_actual=Decimal('0.00'),
            stock_minimo=Decimal('5.00'),
            costo_unitario=Decimal('0.00')
        )
        
        self.almendras = MateriaPrima.objects.create(
            nombre="TEST - Almendras",
            descripcion="Almendras peladas para mezclas",
            unidad_medida="kg",
            stock_actual=Decimal('0.00'),
            stock_minimo=Decimal('3.00'),
            costo_unitario=Decimal('0.00')
        )
        
        self.nueces = MateriaPrima.objects.create(
            nombre="TEST - Nueces",
            descripcion="Nueces de nogal para mezclas",
            unidad_medida="kg",
            stock_actual=Decimal('0.00'),
            stock_minimo=Decimal('2.00'),
            costo_unitario=Decimal('0.00')
        )
        
        self.verificar(
            self.mani.stock_actual == 0,
            "Maní creado con stock inicial 0kg",
            "Error: Stock inicial de Maní no es 0"
        )
        
        self.verificar(
            self.almendras.stock_actual == 0,
            "Almendras creadas con stock inicial 0kg",
            "Error: Stock inicial de Almendras no es 0"
        )
        
        self.verificar(
            self.nueces.stock_actual == 0,
            "Nueces creadas con stock inicial 0kg",
            "Error: Stock inicial de Nueces no es 0"
        )
    
    def test_2_primera_compra_mani(self):
        """Test 2: Primera compra de Maní (establecer precio inicial)"""
        self.log("\n" + "="*60, "TEST")
        self.log("TEST 2: Primera Compra de Maní", "TEST")
        self.log("="*60, "TEST")
        
        # Comprar 5kg a $1000/kg = $5000 total
        compra1 = Compra.objects.create(
            proveedor=self.proveedor,
            materia_prima=self.mani,
            cantidad_mayoreo=Decimal('5.00'),
            precio_mayoreo=Decimal('5000.00')  # precio total
        )
        
        # El save() de Compra ya actualiza el stock y costo automáticamente
        # Refrescar desde DB
        self.mani.refresh_from_db()
        
        self.log(f"Compra 1: {compra1.cantidad_mayoreo}kg por ${compra1.precio_mayoreo} total", "DATA")
        self.log(f"Precio unitario: ${compra1.precio_unitario_mayoreo}/kg", "DATA")
        self.log(f"Stock después: {self.mani.stock_actual}kg @ ${self.mani.costo_unitario}/kg", "DATA")
        
        self.verificar(
            self.mani.stock_actual == Decimal('5.00'),
            "Stock actualizado correctamente a 5kg",
            f"Error: Stock esperado 5kg, obtenido {self.mani.stock_actual}kg"
        )
        
        self.verificar(
            abs(self.mani.costo_unitario - Decimal('1000.00')) <= Decimal('1.00'),
            f"Costo unitario correcto: ${self.mani.costo_unitario}/kg",
            f"Error: Costo esperado ~$1000/kg, obtenido ${self.mani.costo_unitario}/kg"
        )
    
    def test_3_segunda_compra_promedio_ponderado(self):
        """Test 3: Segunda compra con promedio ponderado"""
        self.log("\n" + "="*60, "TEST")
        self.log("TEST 3: Promedio Ponderado en Segunda Compra", "TEST")
        self.log("="*60, "TEST")
        
        # Estado antes de la compra
        stock_antes = self.mani.stock_actual
        precio_antes = self.mani.costo_unitario
        
        self.log(f"ANTES → Stock: {stock_antes}kg @ ${precio_antes}/kg", "DATA")
        
        # Comprar 20kg a $1400/kg = $28000 total
        compra2 = Compra.objects.create(
            proveedor=self.proveedor,
            materia_prima=self.mani,
            cantidad_mayoreo=Decimal('20.00'),
            precio_mayoreo=Decimal('28000.00')
        )
        
        # El save() de Compra ya calcula el promedio ponderado automáticamente
        self.mani.refresh_from_db()
        
        self.log(f"COMPRA → {compra2.cantidad_mayoreo}kg por ${compra2.precio_mayoreo} total", "DATA")
        self.log(f"Precio unitario compra: ${compra2.precio_unitario_mayoreo}/kg", "DATA")
        self.log(f"DESPUÉS → Stock: {self.mani.stock_actual}kg @ ${self.mani.costo_unitario}/kg", "DATA")
        
        # Calcular promedio esperado
        # (5kg × $1000 + 20kg × $1400) / 25kg = (5000 + 28000) / 25 = 1320
        valor_anterior = stock_antes * precio_antes
        valor_compra = compra2.cantidad_mayoreo * compra2.precio_unitario_mayoreo
        stock_total = stock_antes + compra2.cantidad_mayoreo
        promedio_esperado = (valor_anterior + valor_compra) / stock_total
        
        self.log(f"Promedio esperado: ${promedio_esperado:.2f}/kg", "DATA")
        
        self.verificar(
            self.mani.stock_actual == Decimal('25.00'),
            "Stock actualizado a 25kg",
            f"Error: Stock esperado 25kg, obtenido {self.mani.stock_actual}kg"
        )
        
        # Verificar promedio (con tolerancia de $5 por redondeos)
        diferencia = abs(self.mani.costo_unitario - Decimal('1320.00'))
        self.verificar(
            diferencia <= Decimal('5.00'),
            f"Promedio ponderado correcto: ${self.mani.costo_unitario}/kg",
            f"Error: Promedio esperado ~$1320/kg, obtenido ${self.mani.costo_unitario}/kg (dif: ${diferencia})"
        )
    
    def test_4_comprar_almendras_nueces(self):
        """Test 4: Comprar almendras y nueces para receta"""
        self.log("\n" + "="*60, "TEST")
        self.log("TEST 4: Comprar Almendras y Nueces", "TEST")
        self.log("="*60, "TEST")
        
        # Comprar 10kg de almendras a $3500/kg = $35000 total
        compra_alm = Compra.objects.create(
            proveedor=self.proveedor,
            materia_prima=self.almendras,
            cantidad_mayoreo=Decimal('10.00'),
            precio_mayoreo=Decimal('35000.00')
        )
        
        # Comprar 8kg de nueces a $4200/kg = $33600 total
        compra_nue = Compra.objects.create(
            proveedor=self.proveedor,
            materia_prima=self.nueces,
            cantidad_mayoreo=Decimal('8.00'),
            precio_mayoreo=Decimal('33600.00')
        )
        
        self.almendras.refresh_from_db()
        self.nueces.refresh_from_db()
        
        self.log(f"Almendras: {self.almendras.stock_actual}kg @ ${self.almendras.costo_unitario}/kg", "DATA")
        self.log(f"Nueces: {self.nueces.stock_actual}kg @ ${self.nueces.costo_unitario}/kg", "DATA")
        
        self.verificar(
            self.almendras.stock_actual == Decimal('10.00'),
            "Almendras en stock: 10kg",
            "Error en stock de Almendras"
        )
        
        self.verificar(
            self.nueces.stock_actual == Decimal('8.00'),
            "Nueces en stock: 8kg",
            "Error en stock de Nueces"
        )
    
    def test_5_crear_producto_fraccionado(self):
        """Test 5: Crear producto SIN receta (fraccionado)"""
        self.log("\n" + "="*60, "TEST")
        self.log("TEST 5: Crear Producto Fraccionado (SIN receta)", "TEST")
        self.log("="*60, "TEST")
        
        # Stock de maní antes
        stock_mani_antes = self.mani.stock_actual
        self.log(f"Stock Maní ANTES: {stock_mani_antes}kg", "DATA")
        
        # Crear producto "Maní sin sal 500g" con stock inicial de 10 unidades
        self.producto_mani = Producto.objects.create(
            nombre="TEST - Maní sin sal 500g",
            descripcion="Bolsita de maní fraccionado",
            categoria=self.categoria,
            tiene_receta=False,
            materia_prima_asociada=self.mani,
            cantidad_fraccion=500,  # 500 gramos = 0.5 kg
            precio=Decimal('1500.00'),
            stock=10,  # 10 unidades × 0.5kg = 5kg necesarios
            stock_minimo=5
        )
        
        # Refrescar maní desde DB
        self.mani.refresh_from_db()
        stock_mani_despues = self.mani.stock_actual
        
        self.log(f"Stock Maní DESPUÉS: {stock_mani_despues}kg", "DATA")
        self.log(f"Diferencia: {stock_mani_antes - stock_mani_despues}kg (esperado: 5kg)", "DATA")
        
        # El signal debería haber descontado 5kg (10 unidades × 0.5kg)
        descuento_esperado = Decimal('5.00')
        descuento_real = stock_mani_antes - stock_mani_despues
        
        self.verificar(
            descuento_real == descuento_esperado,
            f"Inventario descontado correctamente: {descuento_real}kg",
            f"Error: Esperado descuento de {descuento_esperado}kg, obtenido {descuento_real}kg"
        )
        
        # Verificar cálculo de costo
        costo_calculado = self.producto_mani.calcular_costo_real()
        costo_esperado = self.mani.costo_unitario * Decimal('0.5')  # 0.5kg
        
        self.log(f"Costo calculado: ${costo_calculado}", "DATA")
        self.log(f"Costo esperado: ${costo_esperado}", "DATA")
        
        self.verificar(
            abs(costo_calculado - costo_esperado) <= Decimal('0.01'),
            f"Costo calculado correctamente: ${costo_calculado}",
            f"Error en cálculo de costo"
        )
        
        # Verificar margen
        margen = self.producto_mani.calcular_margen_real()
        # Precio: $1500, Costo: $660 → Margen = (1500-660)/660 × 100 = 127.27%
        
        self.log(f"Margen calculado: {margen:.2f}%", "DATA")
        
        self.verificar(
            margen > 0,
            f"Margen positivo: {margen:.2f}%",
            f"Error: Margen negativo {margen:.2f}%"
        )
    
    def test_6_crear_receta_y_producto(self):
        """Test 6: Crear producto CON receta (múltiples ingredientes)"""
        self.log("\n" + "="*60, "TEST")
        self.log("TEST 6: Crear Producto CON Receta", "TEST")
        self.log("="*60, "TEST")
        
        # Crear receta "Mix Frutos Secos"
        self.receta_mix = Receta.objects.create(
            nombre="TEST - Mix Frutos Secos",
            descripcion="Mezcla de almendras y nueces"
        )
        
        # Agregar ingredientes (proporciones para 1kg de mix)
        RecetaMateriaPrima.objects.create(
            receta=self.receta_mix,
            materia_prima=self.almendras,
            cantidad=Decimal('0.600')  # 600g de almendras por kg de mix
        )
        
        RecetaMateriaPrima.objects.create(
            receta=self.receta_mix,
            materia_prima=self.nueces,
            cantidad=Decimal('0.400')  # 400g de nueces por kg de mix
        )
        
        # Calcular costo de la receta
        costo_receta = self.receta_mix.costo_total()
        # 0.6kg × $3500 + 0.4kg × $4200 = $2100 + $1680 = $3780/kg
        
        self.log(f"Costo de receta: ${costo_receta}/kg", "DATA")
        
        # Stocks antes
        stock_alm_antes = self.almendras.stock_actual
        stock_nue_antes = self.nueces.stock_actual
        
        self.log(f"Stock Almendras ANTES: {stock_alm_antes}kg", "DATA")
        self.log(f"Stock Nueces ANTES: {stock_nue_antes}kg", "DATA")
        
        # Crear producto "Mix Frutos Secos 250g" con stock 8 unidades
        self.producto_mix = Producto.objects.create(
            nombre="TEST - Mix Frutos Secos 250g",
            descripcion="Bolsa de mix premium",
            categoria=self.categoria,
            tiene_receta=True,
            receta=self.receta_mix,
            cantidad_fraccion=250,  # 250 gramos por bolsita
            precio=Decimal('1200.00'),
            stock=8,  # 8 unidades × 0.25kg = 2kg de mix necesario
            stock_minimo=5
        )
        
        # Refrescar stocks
        self.almendras.refresh_from_db()
        self.nueces.refresh_from_db()
        
        stock_alm_despues = self.almendras.stock_actual
        stock_nue_despues = self.nueces.stock_actual
        
        self.log(f"Stock Almendras DESPUÉS: {stock_alm_despues}kg", "DATA")
        self.log(f"Stock Nueces DESPUÉS: {stock_nue_despues}kg", "DATA")
        
        # Para 8 unidades de 250g = 2kg de mix
        # Almendras: 2kg × 0.6 = 1.2kg
        # Nueces: 2kg × 0.4 = 0.8kg
        
        descuento_alm = stock_alm_antes - stock_alm_despues
        descuento_nue = stock_nue_antes - stock_nue_despues
        
        self.log(f"Descuento Almendras: {descuento_alm}kg (esperado: 1.2kg)", "DATA")
        self.log(f"Descuento Nueces: {descuento_nue}kg (esperado: 0.8kg)", "DATA")
        
        self.verificar(
            abs(descuento_alm - Decimal('1.2')) <= Decimal('0.01'),
            f"Almendras descontadas correctamente: {descuento_alm}kg",
            f"Error: Descuento Almendras esperado 1.2kg, obtenido {descuento_alm}kg"
        )
        
        self.verificar(
            abs(descuento_nue - Decimal('0.8')) <= Decimal('0.01'),
            f"Nueces descontadas correctamente: {descuento_nue}kg",
            f"Error: Descuento Nueces esperado 0.8kg, obtenido {descuento_nue}kg"
        )
    
    def test_7_editar_stock_producto(self):
        """Test 7: Editar producto aumentando stock (reabastecimiento)"""
        self.log("\n" + "="*60, "TEST")
        self.log("TEST 7: Reabastecer Producto (editar stock)", "TEST")
        self.log("="*60, "TEST")
        
        # Stock actual del producto maní
        stock_producto_antes = self.producto_mani.stock
        stock_mani_antes = self.mani.stock_actual
        
        self.log(f"Stock Producto ANTES: {stock_producto_antes} unidades", "DATA")
        self.log(f"Stock Maní ANTES: {stock_mani_antes}kg", "DATA")
        
        # Aumentar stock del producto en 20 unidades (reabastecimiento)
        self.producto_mani.stock = 30  # de 10 a 30 = +20 unidades
        self.producto_mani.save()
        
        # Refrescar
        self.mani.refresh_from_db()
        stock_mani_despues = self.mani.stock_actual
        
        self.log(f"Stock Producto DESPUÉS: {self.producto_mani.stock} unidades", "DATA")
        self.log(f"Stock Maní DESPUÉS: {stock_mani_despues}kg", "DATA")
        
        # El signal debería descontar 10kg adicionales (20 unidades × 0.5kg)
        descuento_esperado = Decimal('10.00')
        descuento_real = stock_mani_antes - stock_mani_despues
        
        self.log(f"Descuento: {descuento_real}kg (esperado: {descuento_esperado}kg)", "DATA")
        
        self.verificar(
            abs(descuento_real - descuento_esperado) <= Decimal('0.01'),
            f"Reabastecimiento descontó correctamente {descuento_real}kg",
            f"Error: Esperado {descuento_esperado}kg, obtenido {descuento_real}kg"
        )
    
    def test_8_venta_solo_afecta_producto(self):
        """Test 8: Venta afecta solo stock de producto, NO inventario"""
        self.log("\n" + "="*60, "TEST")
        self.log("TEST 8: Venta (solo afecta producto, NO inventario)", "TEST")
        self.log("="*60, "TEST")
        
        # Stocks antes
        stock_producto_antes = self.producto_mani.stock
        stock_mani_antes = self.mani.stock_actual
        
        self.log(f"Stock Producto ANTES: {stock_producto_antes} unidades", "DATA")
        self.log(f"Stock Maní ANTES: {stock_mani_antes}kg", "DATA")
        
        # Crear venta de 5 unidades
        venta = Venta.objects.create(
            cliente="TEST - Cliente Demo",
            fecha=timezone.now(),
            total=Decimal('7500.00')  # 5 × $1500
        )
        
        subtotal_venta = self.producto_mani.precio * 5
        VentaDetalle.objects.create(
            venta=venta,
            producto=self.producto_mani,
            cantidad=5,
            precio_unitario=self.producto_mani.precio,
            subtotal=subtotal_venta
        )
        
        # Actualizar stock del producto manualmente (normalmente lo haría la vista)
        self.producto_mani.stock -= 5
        self.producto_mani.save()
        
        # Refrescar
        self.mani.refresh_from_db()
        
        stock_producto_despues = self.producto_mani.stock
        stock_mani_despues = self.mani.stock_actual
        
        self.log(f"Stock Producto DESPUÉS: {stock_producto_despues} unidades", "DATA")
        self.log(f"Stock Maní DESPUÉS: {stock_mani_despues}kg", "DATA")
        
        self.verificar(
            stock_producto_despues == stock_producto_antes - 5,
            f"Stock producto reducido correctamente: {stock_producto_antes} → {stock_producto_despues}",
            f"Error en reducción de stock producto"
        )
        
        self.verificar(
            stock_mani_despues == stock_mani_antes,
            f"Stock inventario NO cambió (correcto): {stock_mani_antes}kg",
            f"Error: Stock inventario cambió cuando NO debía"
        )
    
    def test_9_margen_negativo(self):
        """Test 9: Detectar producto con margen negativo"""
        self.log("\n" + "="*60, "TEST")
        self.log("TEST 9: Detección de Margen Negativo", "TEST")
        self.log("="*60, "TEST")
        
        # Crear producto con precio menor al costo
        producto_perdida = Producto.objects.create(
            nombre="TEST - Producto a Pérdida",
            descripcion="Producto vendido por debajo del costo",
            categoria=self.categoria,
            tiene_receta=False,
            materia_prima_asociada=self.almendras,
            cantidad_fraccion=1000,  # 1kg
            precio=Decimal('2000.00'),  # Precio bajo
            stock=0,  # Sin stock para no descontar inventario
            stock_minimo=0
        )
        
        costo = producto_perdida.calcular_costo_real()
        # Costo = $3500/kg × 1kg = $3500
        # Precio = $2000
        # Margen = ((2000-3500)/3500) × 100 = -42.86%
        
        margen = producto_perdida.calcular_margen_real()
        
        self.log(f"Costo: ${costo}", "DATA")
        self.log(f"Precio: ${producto_perdida.precio}", "DATA")
        self.log(f"Margen: {margen:.2f}%", "DATA")
        
        self.verificar(
            margen < 0,
            f"Margen negativo detectado correctamente: {margen:.2f}%",
            f"Error: Margen debería ser negativo, obtenido {margen:.2f}%"
        )
        
        self.verificar(
            producto_perdida.tiene_margen_negativo(),
            "Método tiene_margen_negativo() retorna True",
            "Error: Método no detecta margen negativo"
        )
    
    def mostrar_resumen(self):
        """Muestra resumen final de los tests"""
        self.log("\n" + "="*60, "TEST")
        self.log("RESUMEN DE TESTS", "TEST")
        self.log("="*60, "TEST")
        
        total = len([r for r in self.resultados if r[0] in ["SUCCESS", "ERROR"]])
        exitos = len([r for r in self.resultados if r[0] == "SUCCESS"])
        fallos = len([r for r in self.resultados if r[0] == "ERROR"])
        
        self.log(f"\nTotal de verificaciones: {total}", "INFO")
        self.log(f"Exitosas: {exitos}", "SUCCESS")
        self.log(f"Fallidas: {fallos}", "ERROR")
        
        if fallos == 0:
            self.log("\n🎉 ¡TODOS LOS TESTS PASARON! 🎉", "SUCCESS")
            self.log("El flujo de inventario funciona PERFECTAMENTE ✨", "SUCCESS")
        else:
            self.log(f"\n⚠️ Hay {fallos} tests fallidos", "WARNING")
            self.log("\nErrores encontrados:", "ERROR")
            for error in self.errores:
                self.log(f"  • {error}", "ERROR")
        
        self.log("\n" + "="*60 + "\n", "INFO")
        
        return fallos == 0


def main():
    """Función principal"""
    print("\n" + "🧪" * 30)
    print("TEST COMPLETO - FLUJO DE INVENTARIO LINO")
    print("🧪" * 30 + "\n")
    
    tester = TestInventarioCompleto()
    
    try:
        # Limpiar datos anteriores
        tester.limpiar_datos_test()
        
        # Crear datos base
        tester.crear_datos_base()
        
        # Ejecutar tests
        tester.test_1_crear_materias_primas()
        tester.test_2_primera_compra_mani()
        tester.test_3_segunda_compra_promedio_ponderado()
        tester.test_4_comprar_almendras_nueces()
        tester.test_5_crear_producto_fraccionado()
        tester.test_6_crear_receta_y_producto()
        tester.test_7_editar_stock_producto()
        tester.test_8_venta_solo_afecta_producto()
        tester.test_9_margen_negativo()
        
        # Mostrar resumen
        exito = tester.mostrar_resumen()
        
        # Retornar código de salida
        return 0 if exito else 1
        
    except Exception as e:
        tester.log(f"\n💥 ERROR CRÍTICO: {str(e)}", "ERROR")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
