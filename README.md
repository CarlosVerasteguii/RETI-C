# RETI-C - Registro de Equipos de Tecnologías de Información - Carlos

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![PyQt6](https://img.shields.io/badge/PyQt6-6.4+-green.svg)](https://pypi.org/project/PyQt6/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 Descripción

RETI-C es una aplicación de escritorio desarrollada para el departamento de TI de CFE (Comisión Federal de Electricidad). Su objetivo es reemplazar el proceso manual actual de seguimiento en hojas de cálculo por un sistema centralizado, rápido y a prueba de errores para registrar, gestionar y consultar el historial de los equipos que ingresan para mantenimiento.

## 🎯 Características Principales

- **Registro de Equipos**: Interfaz intuitiva para registrar equipos de TI
- **Almacenamiento Excel**: Persistencia de datos en archivos Excel
- **Búsqueda por Número de Serie**: Consulta rápida de historial de equipos con visualización detallada
- **Navegación Intuitiva**: Sistema de navegación entre vistas (Dashboard, Registro, Consulta)
- **Interfaz CFE**: Diseño alineado con la guía de estilos de CFE
- **Validación de Datos**: Verificación automática de campos requeridos

## 🚀 Instalación

### Prerrequisitos

- Python 3.9 o superior
- Windows 10/11

### Instalación Rápida

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/CarlosVerasteguii/RETI-C.git
   cd RETI-C
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   ```

3. **Activar entorno virtual**
   ```bash
   # Windows
   .\venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

4. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

5. **Ejecutar la aplicación**
   ```bash
   python run.py
   ```

### Ejecución con Script Automático

Para Windows, puedes usar el script incluido:

```bash
.\run_app.bat
```

## 📁 Estructura del Proyecto

```
RETI-C/
├── docs/                    # Documentación del proyecto
│   ├── PRD.md              # Product Requirements Document
│   ├── SRS.md              # Software Requirements Specification
│   └── CFE_Style_Guide.md  # Guía de estilos CFE
├── src/                     # Código fuente
│   ├── __init__.py
│   ├── config.py           # Configuración de la aplicación
│   ├── data_manager.py     # Gestión de datos Excel
│   ├── main_app.py         # Interfaz principal PyQt6
│   └── views/              # Vistas de la aplicación
│       ├── dashboard_view.py  # Vista de bienvenida
│       ├── registration_view.py # Vista de registro
│       └── search_view.py    # Vista de búsqueda
├── resources/               # Recursos de la aplicación
│   ├── styles.qss          # Estilos CFE
│   └── icons/              # Iconos (futuro)
├── data/                    # Datos de la aplicación
│   └── inventario_equipos.xlsx
├── requirements.txt         # Dependencias Python
├── run.py                  # Punto de entrada
├── run_app.bat            # Script de lanzamiento (Windows)
└── README.md              # Este archivo
```

## 🛠️ Tecnologías Utilizadas

- **Python 3.9+**: Lenguaje principal
- **PyQt6**: Framework de interfaz gráfica
- **Pandas**: Manipulación de datos
- **OpenPyXL**: Lectura/escritura de archivos Excel
- **Pytest**: Testing (futuro)

## 📊 Modelo de Datos

La aplicación utiliza un archivo Excel (`inventario_equipos.xlsx`) con las siguientes columnas:

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| ID | Entero | Sí | Identificador único autoincremental |
| Tipo de Equipo | Texto | Sí | Categoría del equipo |
| Marca y Modelo | Texto | Sí | Fabricante y modelo |
| Número de Serie | Texto | Sí | Identificador único del fabricante |
| Fecha de Recepción | Fecha | Sí | Fecha de recepción (YYYY-MM-DD) |
| Fecha de Entrega | Fecha | No | Fecha de entrega (YYYY-MM-DD) |
| Descripción del Problema | Texto | Sí | Descripción del fallo |
| Componentes Entregados | Texto | No | Accesorios recibidos |
| Responsable Recepción | Texto | Sí | Técnico que recibe |
| Historial Intervenciones | Texto | No | Registro de acciones |
| Estado | Texto | Sí | Estado actual del equipo |

## 🎨 Guía de Estilos CFE

La aplicación implementa la guía de estilos visuales de CFE:

- **Color Principal**: Verde CFE (#008E5A)
- **Color Secundario**: Negro CFE (#111111)
- **Tipografía**: Arial (fallback: Helvetica, sans-serif)
- **Bordes Redondeados**: 4px radius
- **Estados de Botones**: Hover y pressed states

## 🔧 Configuración

### Archivo de Configuración

El archivo `src/config.py` contiene todas las configuraciones de la aplicación:

- Rutas de archivos
- Columnas del Excel
- Campos requeridos
- Configuración de la aplicación

### Personalización

Para cambiar la ruta del archivo Excel, modifica `Config.EXCEL_PATH` en `src/config.py`.

## 🧪 Testing

```bash
# Ejecutar tests (cuando estén implementados)
pytest

# Ejecutar con coverage
pytest --cov=src
```

## 📝 Desarrollo

### Estructura de Código

- **config.py**: Configuración centralizada
- **data_manager.py**: Lógica de negocio y persistencia
- **main_app.py**: Contenedor principal y navegación
- **views/**: Vistas de la aplicación
  - **dashboard_view.py**: Vista de bienvenida
  - **registration_view.py**: Vista de registro de equipos
  - **search_view.py**: Vista de búsqueda por número de serie

### Convenciones

- **Nomenclatura**: camelCase para variables, PascalCase para clases
- **Documentación**: Docstrings en todas las funciones
- **Comentarios**: Explicativos para lógica compleja

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👨‍💻 Autor

**Carlos Verastegui**
- Proyecto: RETI-C
- Organización: CFE
- Fecha: 02/08/2025

## 🙏 Agradecimientos

- Departamento de TI de CFE
- Equipo de desarrollo
- Contribuidores del proyecto

## 📞 Soporte

Para soporte técnico o preguntas sobre el proyecto, contacta a:
- **Email**: [tu-email@cfe.gob.mx]
- **GitHub**: [@CarlosVerasteguii](https://github.com/CarlosVerasteguii)

---

**RETI-C** - Simplificando el registro de equipos de TI en CFE 🚀 