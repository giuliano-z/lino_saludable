# conftest.py - Configuración de fixtures para tests E2E
import pytest
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lino_saludable.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture(scope="function")
def test_user(db):
    """Crear usuario de test para login."""
    user = User.objects.create_user(
        username='testuser_e2e',
        email='test_e2e@lino.com',
        password='testpass123',
        is_staff=True,
        is_superuser=True
    )
    yield user
    user.delete()

@pytest.fixture(scope="function")
def sample_producto(db):
    """Crear producto de ejemplo para tests."""
    from gestion.models import Producto
    
    producto = Producto.objects.create(
        nombre="Producto Test E2E",
        precio=100,
        stock=50,
        stock_minimo=10,
        categoria="otros"
    )
    yield producto
    try:
        producto.delete()
    except:
        pass

@pytest.fixture(scope="function")
def sample_materia_prima(db):
    """Crear materia prima de ejemplo para tests."""
    from gestion.models import MateriaPrima
    
    mp = MateriaPrima.objects.create(
        nombre="MP Test E2E UniqueXYZ",
        costo_unitario=25,
        stock_actual=100,
        stock_minimo=20,
        unidad_medida="kg"
    )
    yield mp
    try:
        mp.delete()
    except:
        pass
