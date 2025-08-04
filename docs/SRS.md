# Software Requirements Specification (SRS) - RETI-C
**Versión:** 1.0
**Fecha:** 02/08/2025
**Referencia PRD:** PRD RETI-C v1.0

---

### 1. Introducción

Este documento detalla los requisitos técnicos y funcionales para el desarrollo del Producto Mínimo Viable (MVP) de la aplicación de escritorio RETI-C. Está diseñado para servir como la guía técnica principal para la implementación del software.

### 2. Arquitectura General

*   **Lenguaje de Programación:** Python 3.9+
*   **Framework de UI:** PyQt6
*   **Librería de Datos:** Pandas, Openpyxl
*   **Formato de Datos:** Microsoft Excel (.xlsx)
*   **Plataforma de Ejecución:** Windows 10 / 11
*   **Diseño:** La interfaz se regirá por la hoja de estilos `styles.qss`, que implementa la "Guía Maestra de Estilo Visual CFE".

### 3. Modelo de Datos (Esquema del Excel)

El archivo `inventario_equipos.xlsx` contendrá una única hoja con las siguientes columnas:

| Nombre de Columna          | Tipo de Dato   | Requerido | Descripción                                                |
| -------------------------- | -------------- | --------- | ---------------------------------------------------------- |
| ID                         | Entero         | Sí        | Identificador único, autoincremental (`max(ID) + 1`).      |
| Tipo de Equipo             | Texto (String) | Sí        | Categoría del equipo (ej. Laptop, PC, Impresora).          |
| Marca y Modelo             | Texto (String) | Sí        | Nombre del fabricante y modelo del equipo.                 |
| Numero de Serie            | Texto (String) | Sí        | Identificador único del fabricante. Campo de búsqueda.     |
| Fecha de Recepcion         | Fecha (String) | Sí        | Fecha en formato `YYYY-MM-DD` en que se recibe el equipo.  |
| Fecha de Entrega           | Fecha (String) | No        | Fecha en formato `YYYY-MM-DD` en que se devuelve el equipo.|
| Descripcion del Problema   | Texto (String) | Sí        | Descripción inicial del fallo reportado por el usuario.    |
| Componentes Entregados     | Texto (String) | No        | Lista de accesorios recibidos con el equipo (cargador, etc.).|
| Responsable Recepcion      | Texto (String) | Sí        | Nombre del técnico que recibe el equipo.                   |
| Historial Intervenciones   | Texto (String) | No        | Registro de acciones. Formato: `YYYY-MM-DD - Acción`.      |
| Estado                     | Texto (String) | Sí        | Estado actual (ej. Recibido, En Reparacion, Reparado).     |

### 4. Requisitos Funcionales

**RF-01: Creación de Nuevo Registro**
*   **RF-01.1:** La interfaz principal debe presentar un formulario con campos de entrada `QLineEdit` para todas las columnas requeridas del modelo de datos, excepto `ID`.
*   **RF-01.2:** Al hacer clic en el botón "Guardar Registro" (`primary_button`):
    *   Se deben validar que los campos requeridos no estén vacíos. Si falla, mostrar un `QMessageBox` de advertencia.
    *   Se debe generar un nuevo ID calculando el valor máximo actual en la columna `ID` del Excel y sumándole 1.
    *   Se debe crear una nueva fila en el DataFrame de pandas con los datos del formulario.
    *   Se debe escribir el DataFrame actualizado al archivo `inventario_equipos.xlsx`.
    *   Los campos del formulario deben limpiarse automáticamente tras un guardado exitoso.

**RF-02: Persistencia de Datos**
*   **RF-02.1:** La ruta al archivo Excel será gestionada desde `src/config.py` para facilitar su cambio a una ruta de red.
*   **RF-02.2:** Al iniciar la aplicación, el `data_manager` debe verificar si el archivo Excel existe. Si no, debe crearlo con las cabeceras definidas en el Modelo de Datos.
*   **RF-02.3:** Todas las operaciones de lectura y escritura se realizarán a través de la librería `pandas` para garantizar la integridad del formato `.xlsx`.

**RF-03: Consulta por Número de Serie**
*   **RF-03.1:** La interfaz principal debe incluir una vista de búsqueda que permita consultar equipos por número de serie exacto.
*   **RF-03.2:** Al realizar una búsqueda exitosa, el sistema debe mostrar todos los datos del registro encontrado de forma legible y organizada.
*   **RF-03.3:** Si no se encuentra el número de serie, el sistema debe mostrar un mensaje informativo claro al usuario.
*   **RF-03.4:** La funcionalidad de búsqueda debe estar disponible desde la navegación principal de la aplicación.
*   **RF-03.5:** El método `find_by_serial` del `DataManager` debe estar cubierto por pruebas unitarias que verifiquen búsquedas exitosas y casos sin resultados.

**RF-04: Interfaz de Usuario (UI/UX)**
*   **RF-04.1:** La aplicación cargará al inicio el archivo `resources/styles.qss` para aplicar globalmente la identidad visual de CFE.
*   **RF-04.2:** El layout de la ventana principal estará compuesto por un `QFormLayout` para el formulario y un `QHBoxLayout` para los botones, asegurando un orden lógico y limpio.
*   **RF-04.3:** Existirá un botón "Limpiar Formulario" (`secondary_button`) que vaciará todos los campos de entrada.

### 5. Requisitos No Funcionales

*   **RNF-01 (Rendimiento):** La aplicación debe iniciarse y estar lista para usarse en menos de 5 segundos. Una operación de guardado debe completarse en menos de 3 segundos.
*   **RNF-02 (Usabilidad):** La navegación entre los campos del formulario debe ser posible usando la tecla `Tab`. Los mensajes de error deben ser claros y descriptivos.
*   **RNF-03 (Mantenibilidad):** La lógica de negocio (interacción con Excel) estará completamente aislada en el módulo `src/data_manager.py`. La lógica de la UI estará en `src/main_app.py`. Las configuraciones estarán en `src/config.py`.
*   **RNF-04 (Fiabilidad):** La aplicación debe manejar excepciones de E/S (p. ej., archivo no encontrado, permisos de escritura denegados) y notificar al usuario sin cerrarse inesperadamente. 