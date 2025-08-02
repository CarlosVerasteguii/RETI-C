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
    
    @classmethod
    def ensure_directories(cls):
        """Ensure all required directories exist."""
        cls.DATA_DIR.mkdir(exist_ok=True)
        cls.RESOURCES_DIR.mkdir(exist_ok=True)
        cls.RESOURCES_DIR.mkdir(exist_ok=True) 