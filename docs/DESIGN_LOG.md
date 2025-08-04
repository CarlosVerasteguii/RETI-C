# DESIGN_LOG.md - Registro de Diseño Arquitectónico

Este archivo es el registro canónico y estructurado de decisiones de diseño, patrones de código, convenciones y componentes reutilizables del proyecto RETI-C. Sirve como la "memoria" del proyecto para garantizar la coherencia y la calidad a largo plazo.

---

id: 20250803-220000
type: Decision
title: "Decisión: Implementación de Framework de Pruebas Automatizadas"
status: Implemented
references:
  - file: "tests/test_data_manager.py"
    symbol: "Pruebas unitarias del DataManager"
  - file: "pytest.ini"
    symbol: "Configuración de pytest"
  - file: "requirements.txt"
    symbol: "Dependencias de testing"
---

### 1. Contexto y Problema
El proyecto carecía de pruebas automatizadas, lo que representaba un riesgo crítico para el desarrollo futuro. Sin una red de seguridad, cualquier cambio podría introducir regresiones sin detectarse, dificultando el mantenimiento y la evolución del código.

### 2. Solución y Razón de Ser
Se implementó un framework completo de pruebas automatizadas utilizando pytest y pytest-qt:
1. **Estructura de Pruebas:** Se creó el directorio `tests/` con archivo `__init__.py` para hacerlo un paquete Python.
2. **Configuración de Pytest:** Se añadió `pytest.ini` con configuración específica para el proyecto (pythonpath, testpaths).
3. **Dependencias de Testing:** Se agregaron `pytest` y `pytest-qt` a `requirements.txt`.
4. **Pruebas Unitarias Iniciales:** Se implementaron pruebas para el `DataManager` que verifican:
   - Creación automática del archivo Excel con columnas correctas
   - Funcionalidad de añadir registros con IDs autoincrementales
   - Persistencia correcta de datos

Este enfoque se eligió porque establece una base sólida para la calidad del código, facilita la detección de regresiones y mejora la confianza en futuras modificaciones.

### 3. Implicaciones y Guía de Uso
Esta decisión establece reglas fundamentales para el desarrollo futuro:
- **Todas las nuevas funcionalidades DEBEN incluir pruebas unitarias** que verifiquen su comportamiento esperado.
- **Las pruebas deben usar fixtures de pytest** para aislamiento y reutilización.
- **Se debe usar archivos temporales** para pruebas que involucren persistencia de datos.
- **El patrón AAA (Arrange, Act, Assert)** debe seguirse en todas las pruebas.

### 4. Alternativas Consideradas
- **Sin Pruebas Automatizadas:** Se descartó por el alto riesgo de regresiones y dificultad de mantenimiento.
- **Otros Frameworks de Testing:** Se consideró unittest, pero pytest ofrece mejor sintaxis, fixtures y plugins especializados para PyQt.

---

id: 20250804-212000
type: Decision
title: "Decisión: Refactor a Arquitectura de Vistas e Inyección de Dependencias"
status: Implemented
references:
  - file: "src/main_app.py"
    symbol: "MainApp"
  - file: "src/views/registration_view.py"
    symbol: "RegistrationView"
  - file: "src/data_manager.py"
    symbol: "DataManager"
---

### 1. Contexto y Problema
La arquitectura inicial era monolítica, con toda la lógica de la UI y el manejo de datos centralizada en la clase `MainApp`. Este enfoque violaba el Principio de Responsabilidad Única (SRP), dificultaba las pruebas y no era escalable para añadir futuras funcionalidades (como búsqueda o reportes) sin aumentar exponencialmente la complejidad.

### 2. Solución y Razón de Ser
Se decidió refactorizar la aplicación para adoptar una arquitectura de vistas desacopladas, utilizando el patrón de **Inyección de Dependencias**.
1.  **Aislamiento de la Vista:** Toda la UI y la lógica del formulario de registro se movieron a su propia clase, `RegistrationView`, ubicada en `src/views/`.
2.  **Contenedor Principal:** La clase `MainApp` se simplificó para actuar como un contenedor. Su responsabilidad principal ahora es inicializar los servicios (como `DataManager`) y cargar la vista activa.
3.  **Inyección de Dependencias:** En lugar de que la vista cree su propia instancia de `DataManager`, la instancia se crea en `MainApp` y se "inyecta" en el constructor de `RegistrationView` (`__init__`).

Este enfoque se eligió porque separa limpiamente las responsabilidades, mejora drásticamente la testabilidad (se puede pasar un `DataManager` falso o "mock" a la vista durante las pruebas) y establece un patrón escalable para el futuro.

### 3. Implicaciones y Guía de Uso
Esta decisión establece reglas fundamentales para el desarrollo futuro:
- **Las vistas no deben crear sus propias dependencias de servicios** (como `DataManager`). Deben declararlas como argumentos en su constructor (`__init__`) para que les sean inyectadas desde un nivel superior (ej. `MainApp`).
- **Toda nueva sección principal de la aplicación DEBE crearse como una clase de vista separada en `src/views/`** y ser cargada por `MainApp`.
- Este patrón facilita la adición de un `QStackedWidget` en el futuro para gestionar múltiples vistas, ya que `MainApp` actuará como el coordinador.

### 4. Alternativas Consideradas
- **Mantener Arquitectura Monolítica:** Se descartó por ser insostenible a largo plazo y dificultar las pruebas.
- **Usar Patrón Observer/Eventos:** Se consideró un sistema de señales y slots para la comunicación entre componentes. Se descartó por ser demasiado complejo para las necesidades actuales del proyecto, mientras que la inyección de dependencias ofrece un balance ideal entre desacoplamiento y simplicidad.

---

id: 20250127-120000
type: Convention
title: "Convención: Mantenimiento del Registro de Diseño (DESIGN_LOG.md)"
status: Implemented
references:
  - file: "DESIGN_LOG.md"
    symbol: "Archivo principal de registro arquitectónico"
    line: "L1"
---

### 1. Contexto y Problema
El proyecto RETI-C requiere un sistema de documentación arquitectónica que trascienda un simple changelog. Se necesita un registro estructurado que capture decisiones de diseño, patrones establecidos, componentes reutilizables y convenciones del proyecto. Este archivo debe servir como fuente de verdad para mantener coherencia en el desarrollo a largo plazo y como referencia para futuras decisiones de diseño.

### 2. Solución y Razón de Ser
Se establece el archivo `DESIGN_LOG.md` como el registro canónico del proyecto con un formato estructurado que incluye:
- **Metadatos YAML**: Para información estructurada y búsqueda eficiente
- **Tipos de entrada**: Decision, Pattern, Component, Service, Convention, Warning
- **Estados**: Implemented, Proposed, Deprecated
- **Referencias**: Enlaces a archivos y símbolos específicos del código

Esta solución se eligió porque:
- Proporciona trazabilidad completa de decisiones arquitectónicas
- Facilita la consulta rápida de patrones establecidos
- Permite la evolución controlada de la arquitectura
- Sirve como guía para la IA y desarrolladores futuros

### 3. Implicaciones y Guía de Uso
**Para la IA (Guardian del Conocimiento Arquitectónico):**
- Consultar este archivo ANTES de proponer cualquier cambio nuevo
- Verificar que las sugerencias se alineen con patrones establecidos
- Actualizar el log cuando se implementen nuevas decisiones de diseño

**Para desarrolladores:**
- Revisar este archivo antes de implementar nuevas funcionalidades
- Seguir los patrones y convenciones documentados
- Proponer actualizaciones al log cuando se establezcan nuevos patrones

**Estructura de entrada obligatoria:**
```yaml
---
id: YYYYMMDD-HHMMSS
type: [Decision|Pattern|Component|Service|Convention|Warning]
title: "Título descriptivo"
status: [Implemented|Proposed|Deprecated]
references:
  - file: "ruta/al/archivo.ext"
    symbol: "NombreDeLaFuncionOClase"
    line: "L<numero>"
---
```
