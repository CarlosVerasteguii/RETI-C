# Product Requirements Document (PRD) - RETI-C
**Versión:** 1.0
**Fecha:** 02/08/2025
**Responsable:** Carlos Verastegui

---

### 1. Resumen Ejecutivo

RETI-C (Registro de Equipos de Tecnologías de Información - Carlos) es una aplicación de escritorio diseñada para el departamento de TI de CFE. Su objetivo es reemplazar el proceso manual actual de seguimiento en hojas de cálculo por un sistema centralizado, rápido y a prueba de errores para registrar, gestionar y consultar el historial de los equipos que ingresan para mantenimiento. La primera versión (MVP) utilizará un archivo Excel en una ubicación compartida como backend, con un plan claro de migración a una base de datos robusta en el futuro.

### 2. El Problema

**2.1. Situación Actual:**
El proceso actual se basa en una hoja de cálculo compartida en la red. Aunque funcional, es propensa a errores humanos y carece de eficiencia. La información crítica del historial de un equipo se encuentra dispersa, lo que dificulta el diagnóstico y la toma de decisiones.

**2.2. Puntos de Dolor:**
*   **Inconsistencia de Datos:** No hay validación de entradas, lo que lleva a múltiples formas de escribir la misma información (p. ej., "HP" vs "Hewlett-Packard").
*   **Lentitud en Consultas:** Encontrar el historial de un equipo específico requiere búsquedas manuales (Ctrl+F) en un archivo que crece constantemente, volviéndose lento e ineficiente.
*   **Riesgo de Corrupción:** La edición simultánea o un cierre inesperado pueden corromper el archivo, resultando en pérdida de datos.
*   **Falta de Trazabilidad:** Es imposible saber quién realizó una modificación específica o cuándo se hizo.

### 3. Objetivos del Producto

*   **Centralizar** toda la información de mantenimiento de equipos en un único repositorio fiable.
*   **Agilizar** el registro de un nuevo equipo (< 1 minuto) y la consulta de su historial (< 10 segundos).
*   **Estandarizar** los datos capturados mediante una interfaz controlada.
*   **Establecer** una base tecnológica sólida y escalable que se alinee con la guía de estilo de CFE.

### 4. Usuarios y Roles

*   **Técnico de TI (Usuario Principal - 4 usuarios):**
    *   **Necesidades:** Requiere una forma rápida y sin errores de registrar la entrada de equipos, documentar las acciones realizadas y consultar el historial completo de un equipo por su número de serie.
    *   **Permisos (MVP):** Acceso completo para crear y leer todos los registros. No se implementarán roles diferenciados en la versión inicial.

### 5. Características y Alcance

**5.1. Alcance del MVP (Versión 1.0):**
*   **F1: Creación de Registro de Equipo:** El sistema permitirá crear un nuevo registro con campos predefinidos. El ID será autogenerado y consecutivo, garantizando unicidad.
*   **F2: Almacenamiento en Excel:** Todos los registros se guardarán como filas en un único archivo `.xlsx` ubicado en una ruta de red configurable.
*   **F3: Consulta por Número de Serie:** La funcionalidad de búsqueda esencial permitirá encontrar un registro de equipo específico introduciendo su número de serie exacto.
*   **F4: Interfaz Gráfica Alineada a Marca CFE:** La aplicación tendrá una interfaz de usuario limpia, funcional y que cumpla con las directrices de la "Guía Maestra de Estilo Visual y Esencia de Marca para Aplicaciones CFE".

**5.2. Características Futuras (Post-MVP):**
*   Edición y actualización de registros existentes.
*   Consulta avanzada (filtrado por tipo, estado, fechas).
*   Gestión y adjunto de imágenes por registro.
*   Exportación de reportes a PDF.
*   Migración de la persistencia a una base de datos (MySQL o similar).

### 6. Criterios de Éxito

*   **Adopción Total:** El 100% del equipo de técnicos (4/4) utiliza RETI-C como su herramienta exclusiva para el registro una semana después del lanzamiento.
*   **Eficiencia Medible:** El tiempo promedio para consultar un historial se reduce en un 80% en comparación con el método anterior.
*   **Cero Incidentes:** No se reportan incidentes de pérdida o corrupción de datos durante los primeros 3 meses de uso.

### 7. Riesgos y Supuestos

*   **Riesgo 1 (MVP):** Conflictos de edición simultánea del archivo Excel.
    *   **Mitigación (MVP):** Se asume que, dado el tamaño reducido del equipo, los usuarios se coordinarán verbalmente para no guardar cambios al mismo tiempo. La aplicación no gestionará bloqueos de archivo en su primera versión.
*   **Riesgo 2:** La ruta de red donde reside el archivo Excel puede no estar disponible.
    *   **Mitigación (MVP):** La aplicación mostrará un mensaje de error claro al usuario si no puede acceder al archivo de datos al iniciar o al guardar. 