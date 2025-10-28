import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lino_saludable.settings')
django.setup()

from gestion.models import MateriaPrima, Producto
from decimal import Decimal

# LIMPIAR DATOS EXISTENTES
print("🗑️ Limpiando datos existentes...")
MateriaPrima.objects.all().delete()
Producto.objects.all().delete()

# CREAR MATERIAS PRIMAS CON DATOS REALES DE LINO
print("🌾 Creando materias primas basadas en catálogo LINO...")

materias_primas_data = [
    # HARINAS (Costo = Precio Venta / 1.30 para margen 30%)
    {"nombre": "Harina Integral Agroecológica", "costo_unitario": Decimal("1461.54"), "stock": 50, "unidad_medida": "kg", "categoria": "harinas_especiales"},
    {"nombre": "Harina de Chía", "costo_unitario": Decimal("923.08"), "stock": 30, "unidad_medida": "g", "categoria": "harinas_especiales"},
    {"nombre": "Harina de Garbanzo", "costo_unitario": Decimal("1076.92"), "stock": 25, "unidad_medida": "g", "categoria": "harinas_especiales"},
    {"nombre": "Harina de Avena", "costo_unitario": Decimal("1307.69"), "stock": 40, "unidad_medida": "g", "categoria": "harinas_especiales"},
    {"nombre": "Harina de Trigo Sarraceno", "costo_unitario": Decimal("1461.54"), "stock": 15, "unidad_medida": "g", "categoria": "harinas_especiales"},
    {"nombre": "Harina de Almendras", "costo_unitario": Decimal("2692.31"), "stock": 10, "unidad_medida": "g", "categoria": "harinas_especiales"},
    {"nombre": "Harina de Lino", "costo_unitario": Decimal("1230.77"), "stock": 20, "unidad_medida": "g", "categoria": "harinas_especiales"},
    {"nombre": "Harina de Coco", "costo_unitario": Decimal("2692.31"), "stock": 12, "unidad_medida": "g", "categoria": "harinas_especiales"},
    {"nombre": "Avena Instantánea", "costo_unitario": Decimal("1153.85"), "stock": 35, "unidad_medida": "g", "categoria": "cereales"},
    
    # HARINAS SIN TACC
    {"nombre": "Harina de Arroz", "costo_unitario": Decimal("1307.69"), "stock": 20, "unidad_medida": "g", "categoria": "sin_tacc"},
    {"nombre": "Premezcla Universal", "costo_unitario": Decimal("1461.54"), "stock": 15, "unidad_medida": "g", "categoria": "sin_tacc"},
    {"nombre": "Almidón de Maíz", "costo_unitario": Decimal("1230.77"), "stock": 25, "unidad_medida": "g", "categoria": "sin_tacc"},
    {"nombre": "Fécula de Mandioca", "costo_unitario": Decimal("1615.38"), "stock": 18, "unidad_medida": "g", "categoria": "sin_tacc"},
    
    # FRUTOS SECOS Y MIX
    {"nombre": "Mix Tradicional", "costo_unitario": Decimal("4230.77"), "stock": 15, "unidad_medida": "g", "categoria": "frutos_secos"},
    {"nombre": "Mix Tropical", "costo_unitario": Decimal("4615.38"), "stock": 12, "unidad_medida": "g", "categoria": "frutos_secos"},
    {"nombre": "Mix sin Pasas", "costo_unitario": Decimal("5000.00"), "stock": 10, "unidad_medida": "g", "categoria": "frutos_secos"},
    {"nombre": "Mix Cervecero", "costo_unitario": Decimal("3769.23"), "stock": 8, "unidad_medida": "g", "categoria": "frutos_secos"},
    {"nombre": "Nueces Extralight", "costo_unitario": Decimal("4307.69"), "stock": 12, "unidad_medida": "g", "categoria": "frutos_secos"},
    {"nombre": "Almendras", "costo_unitario": Decimal("4307.69"), "stock": 15, "unidad_medida": "g", "categoria": "frutos_secos"},
    {"nombre": "Bananas Chips", "costo_unitario": Decimal("2230.77"), "stock": 20, "unidad_medida": "g", "categoria": "frutos_secos"},
    {"nombre": "Castañas de Cajú", "costo_unitario": Decimal("4307.69"), "stock": 8, "unidad_medida": "g", "categoria": "frutos_secos"},
    {"nombre": "Maíz Frito", "costo_unitario": Decimal("2692.31"), "stock": 25, "unidad_medida": "g", "categoria": "frutos_secos"},
    {"nombre": "Maní con Sal", "costo_unitario": Decimal("1461.54"), "stock": 30, "unidad_medida": "g", "categoria": "frutos_secos"},
    {"nombre": "Maní sin Sal", "costo_unitario": Decimal("1461.54"), "stock": 30, "unidad_medida": "g", "categoria": "frutos_secos"},
    
    # FRUTAS DESECADAS
    {"nombre": "Pasas de Uva", "costo_unitario": Decimal("1153.85"), "stock": 25, "unidad_medida": "g", "categoria": "frutos_secos"},
    
    # GRANOLAS
    {"nombre": "Granola Tradicional", "costo_unitario": Decimal("2153.85"), "stock": 20, "unidad_medida": "g", "categoria": "cereales"},
    {"nombre": "Granola Stevia (Diabéticos)", "costo_unitario": Decimal("2307.69"), "stock": 15, "unidad_medida": "g", "categoria": "cereales"},
    {"nombre": "Granola Proteica", "costo_unitario": Decimal("2307.69"), "stock": 15, "unidad_medida": "g", "categoria": "cereales"},
    {"nombre": "Granola Pasta de Maní", "costo_unitario": Decimal("2307.69"), "stock": 12, "unidad_medida": "g", "categoria": "cereales"},
    {"nombre": "Granola SIN TACC", "costo_unitario": Decimal("4230.77"), "stock": 8, "unidad_medida": "g", "categoria": "sin_tacc"},
    
    # CEREALES
    {"nombre": "Almohaditas de Avellana", "costo_unitario": Decimal("1769.23"), "stock": 20, "unidad_medida": "g", "categoria": "cereales"},
    {"nombre": "Almohaditas de Frutilla", "costo_unitario": Decimal("1769.23"), "stock": 20, "unidad_medida": "g", "categoria": "cereales"},
    {"nombre": "Almohaditas de Limón", "costo_unitario": Decimal("1769.23"), "stock": 20, "unidad_medida": "g", "categoria": "cereales"},
    {"nombre": "Aritos Frutales", "costo_unitario": Decimal("1461.54"), "stock": 25, "unidad_medida": "g", "categoria": "cereales"},
    {"nombre": "Copos de Maíz Natural", "costo_unitario": Decimal("1307.69"), "stock": 30, "unidad_medida": "g", "categoria": "cereales"},
    {"nombre": "Copos de Maíz Azucarados", "costo_unitario": Decimal("1307.69"), "stock": 30, "unidad_medida": "g", "categoria": "cereales"},
    {"nombre": "Tutuca SIN Azúcar", "costo_unitario": Decimal("1153.85"), "stock": 20, "unidad_medida": "g", "categoria": "cereales"},
    
    # CEREALES SIN TACC
    {"nombre": "Almohaditas Frutilla SIN TACC", "costo_unitario": Decimal("1923.08"), "stock": 15, "unidad_medida": "g", "categoria": "sin_tacc"},
    {"nombre": "Almohaditas Limón SIN TACC", "costo_unitario": Decimal("1923.08"), "stock": 15, "unidad_medida": "g", "categoria": "sin_tacc"},
    {"nombre": "Almohaditas Avellana SIN TACC", "costo_unitario": Decimal("1923.08"), "stock": 15, "unidad_medida": "g", "categoria": "sin_tacc"},
    {"nombre": "Aritos de Miel SIN TACC", "costo_unitario": Decimal("1461.54"), "stock": 18, "unidad_medida": "g", "categoria": "sin_tacc"},
    {"nombre": "Copos Naturales SIN TACC", "costo_unitario": Decimal("1384.62"), "stock": 20, "unidad_medida": "g", "categoria": "sin_tacc"},
    {"nombre": "Quinoa Pop", "costo_unitario": Decimal("1769.23"), "stock": 15, "unidad_medida": "g", "categoria": "sin_tacc"},
    
    # SEMILLAS
    {"nombre": "Mix de Semillas", "costo_unitario": Decimal("1307.69"), "stock": 25, "unidad_medida": "g", "categoria": "frutos_secos"},
    {"nombre": "Semillas de Lino", "costo_unitario": Decimal("615.38"), "stock": 50, "unidad_medida": "g", "categoria": "frutos_secos"},
    {"nombre": "Semillas de Sésamo", "costo_unitario": Decimal("846.15"), "stock": 40, "unidad_medida": "g", "categoria": "frutos_secos"},
    {"nombre": "Semillas de Chía", "costo_unitario": Decimal("1307.69"), "stock": 30, "unidad_medida": "g", "categoria": "frutos_secos"},
    {"nombre": "Semillas de Girasol", "costo_unitario": Decimal("923.08"), "stock": 35, "unidad_medida": "g", "categoria": "frutos_secos"},
    {"nombre": "Semillas de Amapola", "costo_unitario": Decimal("3769.23"), "stock": 8, "unidad_medida": "g", "categoria": "frutos_secos"},
    {"nombre": "Semillas de Zapallo", "costo_unitario": Decimal("3384.62"), "stock": 10, "unidad_medida": "g", "categoria": "frutos_secos"},
    
    # OTROS PRODUCTOS
    {"nombre": "Azúcar Mascabo", "costo_unitario": Decimal("1230.77"), "stock": 30, "unidad_medida": "g", "categoria": "endulzantes"},
    {"nombre": "Miel 100% Pura de Abeja", "costo_unitario": Decimal("3230.77"), "stock": 15, "unidad_medida": "g", "categoria": "endulzantes"},
    {"nombre": "Coco Rallado", "costo_unitario": Decimal("3461.54"), "stock": 12, "unidad_medida": "g", "categoria": "frutos_secos"},
    {"nombre": "Dulce de Leche con Stevia", "costo_unitario": Decimal("3461.54"), "stock": 10, "unidad_medida": "g", "categoria": "productos_veganos"},
    
    # PASTA DE MANÍ Y ACEITES
    {"nombre": "Pasta Maní ODDIS Clásica", "costo_unitario": Decimal("2230.77"), "stock": 15, "unidad_medida": "g", "categoria": "productos_veganos"},
    {"nombre": "Aceite de Coco Virgen", "costo_unitario": Decimal("6846.15"), "stock": 8, "unidad_medida": "ml", "categoria": "aceites_vinagres"},
    {"nombre": "Aceite de Coco Neutro", "costo_unitario": Decimal("4538.46"), "stock": 10, "unidad_medida": "ml", "categoria": "aceites_vinagres"},
    
    # PRODUCTOS MARCA INTEGRA
    {"nombre": "Barrita Avena Almendra Nuez", "costo_unitario": Decimal("1000.00"), "stock": 50, "unidad_medida": "unidad", "categoria": "productos_veganos"},
    {"nombre": "Barrita Girasol Arándanos", "costo_unitario": Decimal("1000.00"), "stock": 50, "unidad_medida": "unidad", "categoria": "productos_veganos"},
    {"nombre": "Barrita Base Choco Arándanos", "costo_unitario": Decimal("1000.00"), "stock": 50, "unidad_medida": "unidad", "categoria": "productos_veganos"},
    {"nombre": "Barrita Proteica Arándanos", "costo_unitario": Decimal("1230.77"), "stock": 40, "unidad_medida": "unidad", "categoria": "productos_veganos"},
    {"nombre": "Barrita Proteica Maní Cacao", "costo_unitario": Decimal("1230.77"), "stock": 40, "unidad_medida": "unidad", "categoria": "productos_veganos"},
    {"nombre": "Barrita SIN TACC Semillas Arándanos", "costo_unitario": Decimal("1000.00"), "stock": 30, "unidad_medida": "unidad", "categoria": "sin_tacc"},
    {"nombre": "Barrita SIN TACC Semillas Cacao", "costo_unitario": Decimal("1000.00"), "stock": 30, "unidad_medida": "unidad", "categoria": "sin_tacc"},
    
    # GALLETITAS Y OTROS
    {"nombre": "Galletitas con Pasas y Ciruelas", "costo_unitario": Decimal("1153.85"), "stock": 25, "unidad_medida": "unidad", "categoria": "conservas"},
    
    # PANIFICACIÓN (productos especiales)
    {"nombre": "Pan Keto Harina Almendras", "costo_unitario": Decimal("4000.00"), "stock": 5, "unidad_medida": "unidad", "categoria": "sin_tacc"},
    {"nombre": "Pan Integral sin Semillas", "costo_unitario": Decimal("2500.00"), "stock": 8, "unidad_medida": "unidad", "categoria": "organicos"},
    {"nombre": "Budín Integral Limón", "costo_unitario": Decimal("2000.00"), "stock": 6, "unidad_medida": "unidad", "categoria": "organicos"},
    {"nombre": "Budín Integral Banana", "costo_unitario": Decimal("2000.00"), "stock": 6, "unidad_medida": "unidad", "categoria": "organicos"},
]

# Crear las materias primas
contador = 0
for data in materias_primas_data:
    try:
        MateriaPrima.objects.create(
            nombre=data["nombre"],
            costo_unitario=data["costo_unitario"],
            stock_actual=data["stock"],
            stock_minimo=5,
            unidad_medida=data["unidad_medida"],
            descripcion=f"Producto de DIETÉTICA LINO - Categoría: {data['categoria']}"
        )
        contador += 1
        if contador % 10 == 0:
            print(f"  📦 Creadas {contador} materias primas...")
    except Exception as e:
        print(f"  ❌ Error creando {data['nombre']}: {e}")

print(f"\n✅ Creadas {contador}/{len(materias_primas_data)} materias primas con precios reales de LINO")

# Ahora crear productos basados en las materias primas (con margen 30%)
print("\n🛍️ Creando productos para venta con margen del 30%...")

productos_creados = 0
for i, data in enumerate(materias_primas_data):
    try:
        # Buscar la materia prima correspondiente
        materia = MateriaPrima.objects.get(nombre=data["nombre"])
        
        # Mapear categorías de materias primas a categorías de productos
        categoria_mapping = {
            'harinas_especiales': 'harinas_especiales',
            'cereales': 'cereales',
            'sin_tacc': 'sin_tacc',
            'frutos_secos': 'frutos_secos',
            'endulzantes': 'endulzantes',
            'productos_veganos': 'productos_veganos',
            'aceites_vinagres': 'aceites_vinagres',
            'conservas': 'conservas',
            'organicos': 'organicos'
        }
        
        # Determinar atributos dietéticos
        atributos = []
        if 'SIN TACC' in materia.nombre.upper():
            atributos.append('sin_tacc')
        if any(word in materia.nombre.upper() for word in ['ORGANICO', 'AGROECOLOGICA', 'INTEGRAL']):
            atributos.append('organico')
        if 'STEVIA' in materia.nombre.upper():
            atributos.append('sin_azucar')
        if any(word in materia.nombre.upper() for word in ['VEGANO', 'BARRITA', 'GRANOLA']):
            atributos.append('vegano')
        
        precio_con_margen = float(materia.costo_unitario * Decimal("1.30"))
        
        Producto.objects.create(
            nombre=materia.nombre,
            descripcion=f"Producto premium de DIETÉTICA LINO. {materia.descripcion or ''}",
            precio=precio_con_margen,
            stock=int(materia.stock_actual),
            categoria=categoria_mapping.get(data.get("categoria", "otros"), "otros"),
            atributos_dieteticos=','.join(atributos),
            marca="LINO",
            origen="Nacional",
            stock_minimo=5,
            materia_prima_asociada=materia,
            tipo_producto='fraccionamiento',
            costo_base=materia.costo_unitario,
            margen_ganancia=Decimal("30.00"),
            precio_venta_calculado=materia.costo_unitario * Decimal("1.30"),
            actualizar_precio_automatico=True
        )
        productos_creados += 1
        
    except Exception as e:
        print(f"  ❌ Error creando producto para {data['nombre']}: {e}")

print(f"✅ Creados {productos_creados} productos para venta")
print("💰 Todos con margen del 30% aplicado")
print("📦 Stock inicial asignado según disponibilidad estimada")
print("🏷️ Atributos dietéticos asignados automáticamente")
print("\n🎉 ¡Base de datos poblada con catálogo real de DIETÉTICA LINO!")
print("🌐 Sistema listo para producción con datos reales del cliente")
