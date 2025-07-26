# 🏢 Portal de Accionistas - Minera Fidami S.A.

Un sistema web moderno y seguro para la gestión integral de accionistas, desarrollado con Django y tecnologías web actuales.

## 📋 Descripción

El Portal de Accionistas es una plataforma completa que permite a los accionistas de Minera Fidami S.A. acceder a su información personal, consultar documentos legales, informes financieros, noticias corporativas y gestionar su portafolio de acciones de manera segura y transparente.

## ✨ Características Principales

### 🔐 **Sistema de Autenticación y Autorización**
- Registro de accionistas con validación de DNI
- Sistema de aprobación de cuentas
- Roles diferenciados (Accionista, Usuario, Administrador)
- Gestión de permisos granular

### 📊 **Gestión de Portafolio**
- Visualización de acciones por accionista
- Historial de transacciones
- Valoración actual de inversiones
- Dashboard personalizado con estadísticas

### 📰 **Sistema de Noticias**
- Publicación de noticias corporativas
- Categorización de contenido
- Noticias destacadas en dashboard
- Soporte para videos de YouTube
- Gestión de imágenes

### 📄 **Documentos Legales**
- Subida y gestión de documentos PDF
- Categorización por tipo de documento
- Vista previa y descarga segura
- Eliminación automática de archivos

### 📈 **Informes Financieros**
- Gestión de informes financieros
- Diferentes tipos y periodicidades
- Descarga en formato PDF
- Organización por áreas

### 🗓️ **Gestión de Eventos**
- Calendario de eventos corporativos
- Registro de asistencia
- Notificaciones automáticas

### 💬 **Sistema de Soporte**
- Formulario de contacto
- Mensajes de soporte
- Configuración de información de contacto
- Botón flotante de WhatsApp

### 🎨 **Personalización del Dashboard**
- Imagen de fondo configurable
- Interfaz moderna y responsiva
- Diseño adaptativo para móviles

### 🔧 **Panel de Administración**
- Interfaz personalizada para administradores
- Gestión completa de todas las secciones
- Funciones de backup (Base de datos y archivos)
- Importación masiva de datos

## 🛠️ Tecnologías Utilizadas

### **Backend**
- **Django 5.2.1** - Framework web principal
- **Python 3.13** - Lenguaje de programación
- **SQLite** - Base de datos (desarrollo)
- **Pillow** - Procesamiento de imágenes
- **Crispy Forms** - Formularios mejorados

### **Frontend**
- **Bootstrap 5** - Framework CSS
- **Bootstrap Icons** - Iconografía
- **HTML5/CSS3** - Estructura y estilos
- **JavaScript** - Interactividad

### **Herramientas de Desarrollo**
- **Git** - Control de versiones
- **Virtual Environment** - Entorno virtual Python
- **Django Management Commands** - Comandos personalizados

## 📁 Estructura del Proyecto

```
Accionistas/
├── accounts/                 # Gestión de usuarios y autenticación
│   ├── models.py            # Modelos de Usuario y Configuración
│   ├── views.py             # Vistas de autenticación y dashboard
│   ├── forms.py             # Formularios de registro y login
│   ├── signals.py           # Señales para gestión automática
│   └── templates/           # Templates de autenticación
├── portafolio/              # Gestión de portafolio de acciones
│   ├── models.py            # Modelo Portafolio
│   ├── views.py             # Vistas del portafolio
│   └── templates/           # Templates del portafolio
├── noticias/                # Sistema de noticias
│   ├── models.py            # Modelo Noticia
│   ├── views.py             # Vistas de noticias
│   ├── templatetags/        # Filtros personalizados (YouTube)
│   └── templates/           # Templates de noticias
├── documentos/              # Gestión de documentos legales
│   ├── models.py            # Modelo DocumentoLegal
│   ├── views.py             # Vistas de documentos
│   ├── forms.py             # Formularios de documentos
│   ├── signals.py           # Gestión automática de archivos
│   └── templates/           # Templates de documentos
├── informes/                # Informes financieros
│   ├── models.py            # Modelo InformeFinanciero
│   ├── views.py             # Vistas de informes
│   ├── forms.py             # Formularios de informes
│   ├── signals.py           # Gestión automática de archivos
│   └── templates/           # Templates de informes
├── eventos/                 # Gestión de eventos
│   ├── models.py            # Modelo Evento
│   ├── views.py             # Vistas de eventos
│   └── templates/           # Templates de eventos
├── transacciones/           # Historial de transacciones
│   ├── models.py            # Modelo HistorialTransaccion
│   └── views.py             # Vistas de transacciones
├── soporte/                 # Sistema de soporte
│   ├── models.py            # Modelos de contacto y mensajes
│   ├── views.py             # Vistas de soporte
│   ├── forms.py             # Formularios de contacto
│   ├── admin.py             # Configuración del admin
│   ├── admin_backup.py      # Funciones de backup
│   └── templates/           # Templates de soporte
├── configuracion/           # Panel de administración personalizado
│   ├── views.py             # Vistas del panel admin
│   ├── urls.py              # URLs del panel admin
│   └── templates/           # Templates del panel admin
├── templates/               # Templates base y compartidos
│   ├── base.html            # Template base principal
│   └── components/          # Componentes reutilizables
├── static/                  # Archivos estáticos
│   ├── css/                 # Hojas de estilo
│   ├── js/                  # JavaScript
│   └── images/              # Imágenes
├── media/                   # Archivos subidos por usuarios
├── fidami_portal/           # Configuración principal del proyecto
│   ├── settings.py          # Configuración de Django
│   ├── urls.py              # URLs principales
│   └── wsgi.py              # Configuración WSGI
├── manage.py                # Script de gestión de Django
├── requirements.txt         # Dependencias del proyecto
└── README.md               # Este archivo
```

## 🚀 Instalación y Configuración

### **Prerrequisitos**
- Python 3.13 o superior
- pip (gestor de paquetes de Python)
- Git

### **Pasos de Instalación**

1. **Clonar el repositorio**
   ```bash
   git clone <url-del-repositorio>
   cd Accionistas
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar base de datos**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Crear superusuario**
   ```bash
   python manage.py createsuperuser
   ```

6. **Ejecutar el servidor**
   ```bash
   python manage.py runserver
   ```

7. **Acceder al sistema**
   - URL: http://127.0.0.1:8000/
   - Admin: http://127.0.0.1:8000/admin/

## 👥 Roles de Usuario

### **Accionista**
- Acceso a su portafolio personal
- Consulta de documentos e informes
- Visualización de noticias y eventos
- Contacto con soporte

### **Usuario**
- Acceso limitado a información pública
- Registro de eventos
- Contacto con soporte

### **Administrador**
- Gestión completa del sistema
- Panel de administración personalizado
- Funciones de backup
- Gestión de usuarios y contenido

## 🔧 Funcionalidades Administrativas

### **Panel de Administración Personalizado**
- Acceso en `/configuracion/administrar/`
- Gestión de todas las secciones del sistema
- Interfaz moderna y intuitiva

### **Gestión de Archivos**
- Eliminación automática de archivos al editar/eliminar registros
- Validación de tipos de archivo
- Organización en carpetas específicas

### **Sistema de Backup**
- Backup de base de datos SQLite
- Backup de carpeta media (archivos subidos)
- Acceso directo desde el admin

### **Configuración del Dashboard**
- Personalización de imagen de fondo
- Gestión desde panel administrativo
- Vista previa de cambios

## 📱 Características Responsivas

- **Diseño adaptativo** para todos los dispositivos
- **Navegación optimizada** para móviles
- **Botón flotante** de WhatsApp
- **Interfaz moderna** con Bootstrap 5

## 🔒 Seguridad

- **Autenticación robusta** con Django
- **Validación de formularios** en frontend y backend
- **Protección CSRF** en todos los formularios
- **Gestión de permisos** granular
- **Validación de archivos** subidos

## 📊 Gestión de Datos

### **Importación Masiva**
- Comandos de Django para importar datos
- Validación automática de información
- Manejo de errores y duplicados

### **Eliminación Automática**
- Señales de Django para gestión de archivos
- Limpieza automática de archivos no utilizados
- Prevención de acumulación de datos

## 🎨 Personalización

### **Temas y Estilos**
- Diseño corporativo de Minera Fidami S.A.
- Colores y branding personalizados
- Iconografía consistente

### **Configuración Dinámica**
- Información de contacto configurable
- Imágenes de fondo personalizables
- Contenido dinámico en dashboard

## 📞 Soporte y Contacto

### **Funciones de Soporte**
- Formulario de contacto integrado
- Mensajes de soporte con seguimiento
- Configuración de información de contacto
- Integración con WhatsApp

### **Comunicación**
- Notificaciones automáticas
- Sistema de mensajes
- Alertas y recordatorios

## 🔄 Mantenimiento

### **Backup Regular**
- Base de datos SQLite
- Archivos de media
- Configuraciones del sistema

### **Actualizaciones**
- Gestión de dependencias
- Migraciones de base de datos
- Actualizaciones de seguridad

## 📈 Escalabilidad

### **Arquitectura Modular**
- Apps independientes y reutilizables
- Separación clara de responsabilidades
- Fácil extensión de funcionalidades

### **Optimización**
- Consultas de base de datos optimizadas
- Carga lazy de imágenes
- Compresión de archivos estáticos

## 🤝 Contribución

### **Desarrollo**
1. Fork del repositorio
2. Crear rama para nueva funcionalidad
3. Implementar cambios
4. Crear Pull Request

### **Reporte de Bugs**
- Usar el sistema de issues de GitHub
- Incluir pasos para reproducir
- Especificar entorno y versión

## 📄 Licencia

Este proyecto es propiedad de Minera Fidami S.A. y está destinado para uso interno de la empresa.

## 👨‍💻 Desarrollado por

**Portal de Accionistas - Minera Fidami S.A.**
- **Versión**: 1.0.0
- **Fecha**: Julio 2025
- **Tecnología**: Django + Bootstrap

---

*Para más información, contactar al equipo de desarrollo de Minera Fidami S.A.* 