"""
Configuration module for RETI-C application.
Manages application settings and file paths.

Author: Carlos Verastegui
Version: 1.0
Date: 02/08/2025
"""

import os
from pathlib import Path


class Config:
    """Configuration class for RETI-C application."""
    
    # Application Info
    APP_NAME = "RETI-C"
    APP_VERSION = "1.0"
    ORGANIZATION = "CFE"
    
    # File Paths
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "data"
    RESOURCES_DIR = BASE_DIR / "resources"
    STYLES_FILE = RESOURCES_DIR / "styles.qss"
    
    # Excel Configuration
    EXCEL_FILENAME = "inventario_equipos.xlsx"
    EXCEL_PATH = DATA_DIR / EXCEL_FILENAME
    
    # Excel Column Headers (as per SRS)
    COLUMNS = [
        "ID",
        "Tipo de Equipo", 
        "Marca y Modelo",
        "Numero de Serie",
        "Fecha de Recepcion",
        "Fecha de Entrega", 
        "Descripcion del Problema",
        "Componentes Entregados",
        "Responsable Recepcion",
        "Historial Intervenciones",
        "Estado"
    ]
    
    # Required Fields (as per SRS)
    REQUIRED_FIELDS = [
        "Tipo de Equipo",
        "Marca y Modelo", 
        "Numero de Serie",
        "Fecha de Recepcion",
        "Descripcion del Problema",
        "Responsable Recepcion",
        "Estado"
    ]
    
    # --- Mensajes y Textos de la UI ---
    MSG_ERROR_SERIAL_VACIO = "El número de serie no puede ser nulo o estar vacío."
    MSG_CAMPO_REQUERIDO = "El campo '{field_name}' es obligatorio."
    MSG_EXITO_REGISTRO = "Equipo con S/N '{serial_number}' ha sido registrado."
    MSG_ERROR_GUARDADO = "No se pudo guardar el registro en el archivo Excel. Verifique los permisos o si el archivo está en uso."

    # Títulos de MessageBox
    MSG_TITULO_CAMPOS_REQUERIDOS = "Campos Requeridos"
    MSG_TITULO_EXITO = "Éxito"
    MSG_TITULO_ERROR_GUARDADO = "Error de Guardado"

    # Textos de botones
    MSG_BTN_LIMPIAR = "Limpiar Formulario"
    MSG_BTN_GUARDAR = "Guardar Registro"
    
    # Valores por defecto y Formatos
    DEFAULT_ESTADO = "Recibido"
    FORMATO_FECHA = "yyyy-MM-dd"

    # --- Constantes de Estilos y UI ---
    # Paleta de Colores Corporativa CFE (Referencia: CFE_Style_Guide.md - Sección 2.1)
    COLOR_CFE_GREEN = "#008E5A"          # Verde principal CFE
    COLOR_CFE_GREEN_DARK = "#006B47"     # Verde oscuro CFE  
    COLOR_CFE_GREEN_VERY_DARK = "#004D33" # Verde muy oscuro CFE
    COLOR_CFE_TEXT_ON_GREEN = "#FFFFFF"   # Texto sobre verde CFE
    COLOR_CFE_BLACK = "#111111"          # Negro CFE
    COLOR_GRAY_TEXT = "#666666"          # Gris para texto secundario
    COLOR_GRAY_LIGHT_BG = "#f8f9fa"      # Gris claro para fondos

    # Geometría de Ventanas
    WINDOW_MAIN_GEOMETRY = (100, 100, 950, 750)  # x, y, width, height

    # Dimensiones de Componentes UI
    UI_TEXTEDIT_MAX_HEIGHT = 60
    UI_VIEW_MARGINS = (40, 40, 40, 40)  # left, top, right, bottom
    UI_LAYOUT_SPACING = 20
    
    @classmethod
    def ensure_directories(cls):
        """Ensure all required directories exist."""
        cls.DATA_DIR.mkdir(exist_ok=True)
        cls.RESOURCES_DIR.mkdir(exist_ok=True)
        cls.RESOURCES_DIR.mkdir(exist_ok=True) 