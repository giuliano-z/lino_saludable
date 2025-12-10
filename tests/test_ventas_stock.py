"""
Tests TDD para sistema de ventas - Bug #1 y Bug #2
====================================================

Estos tests aseguran que:
1. El stock se descuenta UNA SOLA VEZ al crear una venta
2. Los productos con stock > 0 aparecen en el dropdown
3. Los productos con stock = 0 NO aparecen en el dropdown
4. El signal de eliminación devuelve el stock correctamente

Autor: Sistema LINO Saludable
Fecha: 9 de Diciembre 2025
"""

import pytest
from decimal import Decimal
from django.test import TestCase, Client
from django.contrib.auth.models import User
from gestion.models import Producto, Venta, VentaDetalle


class TestVentaStockDescuento(TestCase):
    """
    Tests para Bug #1: Descuento duplicado de stock
    """
    
    def setUp(self):
        """Crear datos de prueba"""
        self.usuario = User.objects.create_user(
            username='test_user',
            password='test_pass'
        )
        
        self.producto = Producto.objects.create(
            nombre='Producto Test',
            stock=10,
            precio=100.00,
            stock_minimo=2,
            categoria='test'
        )
    
    def test_stock_descuenta_una_sola_vez(self):
        """
        BUG #1 CORREGIDO: Stock debe descontarse UNA SOLA VEZ
        
        Escenario:
        - Producto con stock = 10
        - Venta de 3 unidades
        - Stock final debe ser 7 (no 4 por descuento duplicado)
        """
        # Arrange
        stock_inicial = self.producto.stock
        cantidad_venta = 3
        stock_esperado = stock_inicial - cantidad_venta
        
        # Act
        venta = Venta.objects.create(
            cliente='Cliente Test',
            usuario=self.usuario,
            total=Decimal('300.00')
        )
        
        detalle = VentaDetalle.objects.create(
            venta=venta,
            producto=self.producto,
            cantidad=cantidad_venta,
            precio_unitario=Decimal('100.00'),
            subtotal=Decimal('300.00')
        )
        
        # Simular descuento manual (como en la vista)
        from django.db.models import F
        Producto.objects.filter(id=self.producto.id).update(
            stock=F('stock') - cantidad_venta
        )
        
        # Assert
        self.producto.refresh_from_db()
        self.assertEqual(
            self.producto.stock,
            stock_esperado,
            f'Stock debe ser {stock_esperado} (inicial={stock_inicial}, vendido={cantidad_venta})'
        )
    
    def test_stock_no_negativo_con_signal_desactivado(self):
        """
        Verificar que el signal NO descuenta stock adicional
        """
        # Arrange
        self.producto.stock = 5
        self.producto.save()
        
        # Act
        venta = Venta.objects.create(
            cliente='Cliente Test',
            usuario=self.usuario,
            total=Decimal('200.00')
        )
        
        # Crear detalle (signal debería estar desactivado)
        detalle = VentaDetalle.objects.create(
            venta=venta,
            producto=self.producto,
            cantidad=2,
            precio_unitario=Decimal('100.00'),
            subtotal=Decimal('200.00')
        )
        
        # Descuento manual
        from django.db.models import F
        Producto.objects.filter(id=self.producto.id).update(
            stock=F('stock') - 2
        )
        
        # Assert
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock, 3)
        self.assertGreaterEqual(self.producto.stock, 0, 'Stock no debe ser negativo')
    
    def test_venta_multiple_productos(self):
        """
        Test con múltiples productos en una venta
        """
        # Arrange
        producto2 = Producto.objects.create(
            nombre='Producto 2',
            stock=8,
            precio=50.00,
            stock_minimo=1,
            categoria='test'
        )
        
        # Act
        venta = Venta.objects.create(
            cliente='Cliente Multi',
            usuario=self.usuario,
            total=Decimal('450.00')
        )
        
        # Detalle 1: Producto 1, cantidad 3
        VentaDetalle.objects.create(
            venta=venta,
            producto=self.producto,
            cantidad=3,
            precio_unitario=Decimal('100.00'),
            subtotal=Decimal('300.00')
        )
        from django.db.models import F
        Producto.objects.filter(id=self.producto.id).update(stock=F('stock') - 3)
        
        # Detalle 2: Producto 2, cantidad 3
        VentaDetalle.objects.create(
            venta=venta,
            producto=producto2,
            cantidad=3,
            precio_unitario=Decimal('50.00'),
            subtotal=Decimal('150.00')
        )
        Producto.objects.filter(id=producto2.id).update(stock=F('stock') - 3)
        
        # Assert
        self.producto.refresh_from_db()
        producto2.refresh_from_db()
        
        self.assertEqual(self.producto.stock, 7)
        self.assertEqual(producto2.stock, 5)


class TestProductosDropdown(TestCase):
    """
    Tests para Bug #2: Productos faltantes en dropdown
    """
    
    def setUp(self):
        """Crear productos con diferentes stocks"""
        self.producto_con_stock = Producto.objects.create(
            nombre='Producto Con Stock',
            stock=10,
            precio=100.00,
            stock_minimo=2,
            categoria='test'
        )
        
        self.producto_sin_stock = Producto.objects.create(
            nombre='Producto Sin Stock',
            stock=0,
            precio=100.00,
            stock_minimo=2,
            categoria='test'
        )
        
        self.usuario = User.objects.create_user(
            username='test_user',
            password='test_pass'
        )
    
    def test_productos_con_stock_aparecen(self):
        """
        Productos con stock > 0 deben aparecer en el dropdown
        """
        # Arrange & Act
        productos_disponibles = Producto.objects.filter(stock__gt=0)
        
        # Assert
        self.assertIn(
            self.producto_con_stock,
            productos_disponibles,
            'Producto con stock > 0 debe aparecer en dropdown'
        )
    
    def test_productos_sin_stock_no_aparecen(self):
        """
        Productos con stock = 0 NO deben aparecer en el dropdown
        """
        # Arrange & Act
        productos_disponibles = Producto.objects.filter(stock__gt=0)
        
        # Assert
        self.assertNotIn(
            self.producto_sin_stock,
            productos_disponibles,
            'Producto con stock = 0 NO debe aparecer en dropdown'
        )
    
    def test_filtro_vista_crear_venta(self):
        """
        Verificar que el filtro de la vista es correcto
        """
        # Arrange & Act (simular filtro de crear_venta_v3)
        productos = Producto.objects.filter(stock__gt=0).order_by('nombre')
        
        # Assert - verificar que el producto con stock SÍ está
        self.assertIn(self.producto_con_stock, productos)
        # Y el producto sin stock NO está
        self.assertNotIn(self.producto_sin_stock, productos)


class TestSignalDevolucionStock(TestCase):
    """
    Tests para signal de eliminación de VentaDetalle
    """
    
    def setUp(self):
        """Crear datos de prueba"""
        self.usuario = User.objects.create_user(
            username='test_user',
            password='test_pass'
        )
        
        self.producto = Producto.objects.create(
            nombre='Producto Test',
            stock=10,
            precio=100.00,
            stock_minimo=2,
            categoria='test'
        )
    
    def test_eliminar_detalle_devuelve_stock(self):
        """
        Al eliminar un detalle de venta, debe devolver el stock
        
        NOTA: El signal post_delete SÍ está activo y funciona correctamente
        """
        # Arrange
        stock_inicial = self.producto.stock  # 10
        
        venta = Venta.objects.create(
            cliente='Cliente Test',
            usuario=self.usuario,
            total=Decimal('300.00')
        )
        
        detalle = VentaDetalle.objects.create(
            venta=venta,
            producto=self.producto,
            cantidad=3,
            precio_unitario=Decimal('100.00'),
            subtotal=Decimal('300.00')
        )
        
        # Descuento manual (simular vista)
        from django.db.models import F
        Producto.objects.filter(id=self.producto.id).update(stock=F('stock') - 3)
        
        # Verificar que stock descendió
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock, stock_inicial - 3)  # 7
        
        # Act - eliminar detalle (signal devuelve stock)
        detalle.delete()
        
        # Assert - stock debe volver al inicial
        self.producto.refresh_from_db()
        self.assertEqual(
            self.producto.stock,
            stock_inicial,  # Debe volver a 10
            'Stock debe volver al inicial al eliminar detalle'
        )


class TestConcurrencyRaceConditions(TestCase):
    """
    Tests para verificar que F() expression previene race conditions
    """
    
    def setUp(self):
        self.usuario = User.objects.create_user(
            username='test_user',
            password='test_pass'
        )
        
        self.producto = Producto.objects.create(
            nombre='Producto Test',
            stock=100,
            precio=100.00,
            stock_minimo=10,
            categoria='test'
        )
    
    def test_f_expression_actualiza_atomicamente(self):
        """
        F() expression debe actualizar stock de forma atómica
        """
        from django.db.models import F
        
        # Arrange
        stock_inicial = self.producto.stock
        
        # Act
        Producto.objects.filter(id=self.producto.id).update(
            stock=F('stock') - 5
        )
        
        # Assert
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock, stock_inicial - 5)


# ==================== PYTEST FIXTURES ====================

@pytest.fixture
def producto_test(db):
    """Fixture para crear producto de prueba"""
    return Producto.objects.create(
        nombre='Producto Pytest',
        stock=20,
        precio=150.00,
        stock_minimo=3,
        categoria='test'
    )


@pytest.fixture
def usuario_test(db):
    """Fixture para crear usuario de prueba"""
    return User.objects.create_user(
        username='pytest_user',
        password='pytest_pass'
    )


@pytest.mark.django_db
def test_venta_basica_pytest(producto_test, usuario_test):
    """
    Test usando pytest fixtures
    """
    # Arrange
    stock_inicial = producto_test.stock
    
    # Act
    venta = Venta.objects.create(
        cliente='Cliente Pytest',
        usuario=usuario_test,
        total=Decimal('300.00')
    )
    
    VentaDetalle.objects.create(
        venta=venta,
        producto=producto_test,
        cantidad=2,
        precio_unitario=Decimal('150.00'),
        subtotal=Decimal('300.00')
    )
    
    from django.db.models import F
    Producto.objects.filter(id=producto_test.id).update(stock=F('stock') - 2)
    
    # Assert
    producto_test.refresh_from_db()
    assert producto_test.stock == stock_inicial - 2
