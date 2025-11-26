# 🥜 Lino Saludable - Sistema de Gestión

Sistema de gestión integral desarrollado en **Django** para la administración completa de un negocio de frutos secos y productos saludables.

**[GitHub](https://github.com/giuliano-z/lino_saludable)** | Sistema en producción hosteado en Railway

## ✨ Características Principales

### 📦 Gestión de Productos
- Control completo de inventario con alertas de stock bajo
- Categorización y precios dinámicos
- Seguimiento de stock mínimo y máximo

### 💰 Sistema de Ventas
- Registro rápido de ventas con cálculo automático
- Historial completo de transacciones
- Control de stock en tiempo real

### 🚛 Compras al Mayoreo
- Gestión de materias primas y proveedores
- Cálculo automático de precios por kilogramo
- Control de stock de materias primas

### 📊 Dashboard y Reportes
- Estadísticas en tiempo real
- Gráficos de tendencias de ventas
- Análisis financiero con márgenes de ganancia
- Reportes de productos más vendidos
- Reportes configurables por rango de fechas

### 🔔 Sistema de Alertas
- Notificaciones de stock bajo
- Alertas de productos críticos
- Seguimiento de materias primas

## 🛠️ Tecnologías Utilizadas

- **Backend:** Django 4.x, Python 3.x
- **Frontend:** Bootstrap 5, HTML5, CSS3, JavaScript
- **Base de Datos:** PostgreSQL (producción)
- **Gráficos:** Chart.js
- **Deployment:** Railway con Docker
- **Control de versiones:** Git

## 📋 Requisitos Previos

- Python 3.8+
- PostgreSQL 12+ (para producción)
- Git
- pip (gestor de paquetes de Python)

## 🚀 Instalación y Configuración Local

### 1. Clonar el repositorio

git clone https://github.com/giuliano-z/lino_saludable.git
cd lino_saludable

text

### 2. Crear entorno virtual

python3 -m venv venv
source venv/bin/activate # En Windows: venv\Scripts\activate

text

### 3. Instalar dependencias

pip install -r requirements.txt

text

### 4. Configurar variables de entorno

cp .env.example .env

text

Edita el archivo `.env` con tus credenciales locales:

SECRET_KEY=tu-secret-key-super-segura-aqui
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1

text

### 5. Ejecutar migraciones

python manage.py migrate

text

### 6. Crear superusuario (admin)

python manage.py createsuperuser

text

Sigue las instrucciones para crear tu usuario administrativo.

### 7. Ejecutar servidor de desarrollo

python manage.py runserver

text

El sistema estará disponible en: [**http://localhost:8000**](http://localhost:8000)

Accede al admin en: [**http://localhost:8000/admin**](http://localhost:8000/admin)

## 📂 Estructura del Proyecto

lino_saludable/
├── lino/ # Configuración principal de Django
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
├── productos/ # Aplicación de productos
│ ├── models.py
│ ├── views.py
│ └── templates/
├── ventas/ # Aplicación de ventas
├── dashboard/ # Aplicación de reportes y dashboard
├── static/ # Archivos CSS, JS, imágenes
├── media/ # Archivos subidos por usuarios
├── templates/ # Templates HTML globales
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md

text

## 🌐 Deployment en Railway

El proyecto está configurado para deployarse automáticamente en [Railway](https://railway.app).

**Variables de entorno en Railway:**
- `DEBUG=False`
- `DATABASE_URL=` (Proporcionado por Railway)
- `SECRET_KEY=` (Tu secret key segura)
- `ALLOWED_HOSTS=tu-dominio.railway.app`

**Auto-deploy:** Cada push a `main` se actualiza automáticamente en producción.

## 🔐 Seguridad

- Las variables sensibles (`.env`) se excluyen de Git
- Usa `.env.example` como template para nuevas configuraciones
- En producción, todas las credenciales están en Railway
- `DEBUG=False` en producción para evitar exposición de datos

## 📊 Métricas del Proyecto

- **+1800 transacciones** registradas en la BD
- **Sistema de reportes** con múltiples filtros y análisis
- **Control de stock** en tiempo real con alertas automáticas
- **ROI tracking** y análisis financiero completo

## 🎯 Próximas Mejoras

- [ ] API REST para integraciones externas
- [ ] Sistema de usuarios con roles
- [ ] Notificaciones por email
- [ ] Aplicación móvil

## 👨‍💻 Autor

**Giuliano Daniel Zulatto**
- [LinkedIn](https://www.linkedin.com/in/giuliano-daniel-zulatto-37250b270/)
- [GitHub](https://github.com/giuliano-z)
- Email: giulianodanielzulatto@gmail.com

## 📄 Licencia

Este proyecto está bajo licencia MIT. Ver archivo `LICENSE` para más detalles.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para cambios mayores, por favor abre un issue primero.

git checkout -b feature/AmazingFeature
git commit -m 'Add some AmazingFeature'
git push origin feature/AmazingFeature

text

## 📞 Contacto y Soporte

Si tienes preguntas o encuentras issues, puedes:
- Abrir un [GitHub Issue](https://github.com/giuliano-z/lino_saludable/issues)
- Contactarme directamente por LinkedIn
