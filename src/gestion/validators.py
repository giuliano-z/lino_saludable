"""
Sistema de validaciones robustas para LINO SALUDABLE
Previene errores críticos en operaciones de dinero y stock
"""
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import models
from typing import Dict, List, Tuple, Any, Optional
from .models import Producto, MateriaPrima, Venta, VentaDetalle
from .logging_system import LinoLogger

class ValidationError(Exception):
    """Excepción personalizada para errores de validación de negocio"""
    def __init__(self, message: str, error_code: str = None, context: Dict = None):
        self.message = message
        self.error_code = error_code
        self.context = context or {}
        super().__init__(self.message)

class LinoValidator:
    """Validador centralizado para todas las operaciones críticas de LINO"""
    
    @staticmethod
    def validar_venta_completa(detalles_venta: List[Dict[str, Any]], usuario=None) -> Tuple[bool, List[str]]:
        """
        Valida una venta completa antes de procesarla
        
        Args:
            detalles_venta: Lista de diccionarios con producto_id, cantidad, precio_unitario
            usuario: Usuario que realiza la operación
            
        Returns:
            Tuple[bool, List[str]]: (es_valida, lista_errores)
        """
        errores = []
        
        try:
            # Validación básica: debe haber al menos un detalle
            if not detalles_venta:
                errores.append("La venta debe tener al menos un producto")
                return False, errores
            
            # Validar cada detalle individualmente
            for i, detalle in enumerate(detalles_venta):
                producto_id = detalle.get('producto_id')
                cantidad = detalle.get('cantidad', 0)
                precio_unitario = detalle.get('precio_unitario')
                
                # Validar producto existe
                try:
                    producto = Producto.objects.get(id=producto_id)
                except Producto.DoesNotExist:
                    errores.append(f"Detalle {i+1}: Producto no encontrado (ID: {producto_id})")
                    continue
                
                # Validar cantidad
                if not isinstance(cantidad, (int, float)) or cantidad <= 0:
                    errores.append(f"Detalle {i+1} ({producto.nombre}): Cantidad debe ser mayor a 0")
                    continue
                
                # Validar stock disponible
                if producto.stock < cantidad:
                    errores.append(
                        f"Detalle {i+1} ({producto.nombre}): Stock insuficiente. "
                        f"Solicitado: {cantidad}, Disponible: {producto.stock}"
                    )
                    continue
                
                # Validar precio unitario
                if precio_unitario is not None:
                    if not isinstance(precio_unitario, (int, float, Decimal)) or precio_unitario < 0:
                        errores.append(f"Detalle {i+1} ({producto.nombre}): Precio unitario inválido")
                        continue
                
                # Log de validación exitosa por producto
                LinoLogger.stock_logger.debug(
                    f"VALIDACIÓN_OK - Producto: {producto.nombre}, Cantidad: {cantidad}, Stock: {producto.stock}"
                )
            
            # Si llegó hasta aquí sin errores, la venta es válida
            es_valida = len(errores) == 0
            
            if es_valida:
                LinoLogger.business_logger.info(f"VALIDACIÓN_VENTA_EXITOSA - {len(detalles_venta)} productos validados")
            else:
                LinoLogger.log_venta_error("VALIDACION_MULTIPLE", len(detalles_venta), 
                                         f"Errores: {'; '.join(errores)}", usuario)
            
            return es_valida, errores
            
        except Exception as e:
            error_msg = f"Error inesperado en validación: {str(e)}"
            LinoLogger.log_error_critico("validaciones", "validar_venta_completa", error_msg)
            errores.append(error_msg)
            return False, errores
    
    @staticmethod
    def validar_compra_materia_prima(materia_prima_id: int, cantidad: Decimal, 
                                   precio_total: Decimal, usuario=None) -> Tuple[bool, List[str]]:
        """
        Valida una compra de materia prima antes de procesarla
        
        Returns:
            Tuple[bool, List[str]]: (es_valida, lista_errores)
        """
        errores = []
        
        try:
            # Validar que la materia prima existe
            try:
                materia_prima = MateriaPrima.objects.get(id=materia_prima_id)
            except MateriaPrima.DoesNotExist:
                errores.append(f"Materia prima no encontrada (ID: {materia_prima_id})")
                return False, errores
            
            # Validar cantidad
            if not isinstance(cantidad, (int, float, Decimal)) or cantidad <= 0:
                errores.append("La cantidad debe ser mayor a 0")
            
            # Validar precio total
            if not isinstance(precio_total, (int, float, Decimal)) or precio_total <= 0:
                errores.append("El precio total debe ser mayor a 0")
            
            # Validar coherencia cantidad vs precio (precio unitario mínimo)
            if cantidad > 0 and precio_total > 0:
                precio_unitario = precio_total / Decimal(str(cantidad))
                if precio_unitario < Decimal('0.01'):  # Precio mínimo de 1 centavo
                    errores.append("El precio unitario es demasiado bajo (mínimo: $0.01)")
            
            # Validar límites razonables (prevenir errores de tipeo)
            if cantidad > 10000:  # Más de 10,000 unidades de una vez
                errores.append("Cantidad excesiva. Verificar si es correcto.")
            
            if precio_total > Decimal('1000000'):  # Más de $1,000,000 en una compra
                errores.append("Monto excesivo. Verificar si es correcto.")
            
            # Log de validación
            if len(errores) == 0:
                LinoLogger.business_logger.info(
                    f"VALIDACIÓN_COMPRA_OK - MP: {materia_prima.nombre}, "
                    f"Cantidad: {cantidad}, Precio: ${precio_total}"
                )
            else:
                LinoLogger.log_error_critico(
                    "validaciones", "validar_compra_materia_prima", 
                    f"Errores: {'; '.join(errores)}", 
                    {"materia_prima": materia_prima.nombre, "cantidad": cantidad, "precio": precio_total}
                )
            
            return len(errores) == 0, errores
            
        except Exception as e:
            error_msg = f"Error inesperado en validación de compra: {str(e)}"
            LinoLogger.log_error_critico("validaciones", "validar_compra_materia_prima", error_msg)
            errores.append(error_msg)
            return False, errores
    
    @staticmethod
    def validar_stock_producto(producto: Producto) -> Dict[str, Any]:
        """
        Valida el estado del stock de un producto y retorna información detallada
        
        Returns:
            Dict con información del estado del stock
        """
        try:
            estado = {
                'producto_id': producto.id,
                'producto_nombre': producto.nombre,
                'stock_actual': producto.stock,
                'stock_minimo': producto.stock_minimo,
                'estado': 'normal',
                'alerta': False,
                'mensaje': '',
                'acciones_recomendadas': []
            }
            
            if producto.stock <= 0:
                estado.update({
                    'estado': 'agotado',
                    'alerta': True,
                    'mensaje': 'Producto sin stock - Ventas bloqueadas',
                    'acciones_recomendadas': ['Comprar inmediatamente', 'Ocultar del catálogo']
                })
                LinoLogger.log_stock_agotado(producto.nombre)
                
            elif producto.stock <= producto.stock_minimo:
                estado.update({
                    'estado': 'critico',
                    'alerta': True,
                    'mensaje': f'Stock crítico - Solo {producto.stock} unidades disponibles',
                    'acciones_recomendadas': ['Realizar pedido urgente']
                })
                LinoLogger.log_stock_critico(producto.nombre, producto.stock, producto.stock_minimo)
                
            elif producto.stock <= producto.stock_minimo * 2:
                estado.update({
                    'estado': 'bajo',
                    'alerta': True,
                    'mensaje': f'Stock bajo - {producto.stock} unidades disponibles',
                    'acciones_recomendadas': ['Programar pedido pronto']
                })
            
            return estado
            
        except Exception as e:
            LinoLogger.log_error_critico(
                "validaciones", "validar_stock_producto", 
                f"Error validando stock: {str(e)}", 
                {"producto_id": producto.id}
            )
            return {
                'producto_id': producto.id,
                'error': True,
                'mensaje': 'Error validando stock'
            }
    
    @staticmethod
    def obtener_productos_alertas_stock() -> Dict[str, List[Dict]]:
        """
        Obtiene todos los productos que requieren atención por stock
        
        Returns:
            Dict con productos categorizados por tipo de alerta
        """
        try:
            productos = Producto.objects.all()
            alertas = {
                'agotados': [],
                'criticos': [],
                'bajos': [],
                'total_alertas': 0
            }
            
            for producto in productos:
                validacion = LinoValidator.validar_stock_producto(producto)
                
                if validacion.get('estado') == 'agotado':
                    alertas['agotados'].append(validacion)
                elif validacion.get('estado') == 'critico':
                    alertas['criticos'].append(validacion)
                elif validacion.get('estado') == 'bajo':
                    alertas['bajos'].append(validacion)
            
            alertas['total_alertas'] = (
                len(alertas['agotados']) + 
                len(alertas['criticos']) + 
                len(alertas['bajos'])
            )
            
            # Log del resumen de alertas
            if alertas['total_alertas'] > 0:
                from .logging_system import business_logger
                business_logger.warning(
                    f"ALERTAS_STOCK - Total: {alertas['total_alertas']} | "
                    f"Agotados: {len(alertas['agotados'])} | "
                    f"Críticos: {len(alertas['criticos'])} | "
                    f"Bajos: {len(alertas['bajos'])}"
                )
            
            return alertas
            
        except Exception as e:
            LinoLogger.log_error_critico(
                "validaciones", "obtener_productos_alertas_stock", 
                f"Error obteniendo alertas: {str(e)}"
            )
            return {'error': True, 'mensaje': 'Error obteniendo alertas de stock'}

# ==================== FUNCIONES UTILES ====================
def es_numero_valido(valor, minimo=0, maximo=None) -> bool:
    """Valida que un valor sea numérico y esté en el rango especificado"""
    try:
        num = float(valor)
        if num < minimo:
            return False
        if maximo is not None and num > maximo:
            return False
        return True
    except (ValueError, TypeError):
        return False

def limpiar_decimal(valor) -> Decimal:
    """Convierte un valor a Decimal de forma segura"""
    try:
        return Decimal(str(valor))
    except:
        return Decimal('0.00')
