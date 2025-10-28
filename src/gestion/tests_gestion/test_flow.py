from django.test import TestCase
from django.contrib.auth.models import User
from gestion.models import MateriaPrima, Producto, ProductoMateriaPrima, Compra, Venta, VentaDetalle
from decimal import Decimal

class FlujoCompletoTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.materia = MateriaPrima.objects.create(
            nombre='Harina', unidad_medida='kg', stock_actual=0, stock_minimo=2, costo_unitario=0, proveedor='Proveedor X'
        )
        self.producto = Producto.objects.create(
            nombre='Pan', precio=100, stock=0, stock_minimo=1, materia_prima_asociada=self.materia
        )
        ProductoMateriaPrima.objects.create(
            producto=self.producto, materia_prima=self.materia, cantidad_necesaria=Decimal('0.5')
        )

    def test_flujo_completo(self):
        # 1. Compra de materia prima
        compra = Compra.objects.create(
            proveedor='Proveedor X', materia_prima=self.materia,
            cantidad_mayoreo=Decimal('10'), precio_mayoreo=Decimal('2000')
        )
        self.materia.refresh_from_db()
        self.assertEqual(self.materia.stock_actual, Decimal('10'))
        self.assertEqual(self.materia.costo_unitario, Decimal('200'))

        # 2. Producción de producto (Pan) usando receta
        cantidad_a_producir = 4
        for _ in range(cantidad_a_producir):
            if self.materia.stock_actual >= Decimal('0.5'):
                self.materia.stock_actual -= Decimal('0.5')
                self.producto.stock += 1
                self.materia.save()
                self.producto.save()
        self.producto.refresh_from_db()
        self.materia.refresh_from_db()
        self.assertEqual(self.producto.stock, 4)
        self.assertEqual(self.materia.stock_actual, Decimal('8'))

        # 3. Venta de producto
        venta = Venta.objects.create(cliente='Juan', usuario=self.user, total=0)
        detalle = VentaDetalle.objects.create(venta=venta, producto=self.producto, cantidad=2, precio_unitario=100, subtotal=200)
        self.producto.stock -= 2
        self.producto.save()
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock, 2)

        # 4. Validación de stock insuficiente
        detalle2 = VentaDetalle(venta=venta, producto=self.producto, cantidad=10, precio_unitario=100, subtotal=1000)
        self.assertFalse(detalle2.cantidad <= self.producto.stock)

        # 5. Validación de stock de materia prima insuficiente para producción
        self.materia.stock_actual = Decimal('0.3')
        self.materia.save()
        puede_producir = self.materia.stock_actual >= Decimal('0.5')
        self.assertFalse(puede_producir)
