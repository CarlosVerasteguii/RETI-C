"""
Data Manager module for RETI-C application.
Handles all Excel file operations and data persistence.

Author: Carlos Verastegui
Version: 1.0
Date: 02/08/2025
"""

import pandas as pd
import os
from pathlib import Path
from typing import Dict, List, Optional
from .config import Config


class DataManager:
    """Manages Excel file operations for RETI-C application."""
    
    def __init__(self):
        """Initialize the data manager with auto-fallback functionality."""
        self.active_path: Path = None
        self.is_network_mode: bool = False
        self.connection_error: str | None = None
        self.columns = Config.COLUMNS
        
        self._initialize_path()
        self._ensure_excel_exists()
    
    def _initialize_path(self):
        """Intenta establecer la ruta de red. Si falla, hace fallback a la local."""
        try:
            network_dir = Config.EXCEL_NETWORK_PATH.parent
            # Validación de existencia y permisos de escritura (más robusta)
            if network_dir.exists() and os.access(network_dir, os.W_OK):
                self.active_path = Config.EXCEL_NETWORK_PATH
                self.is_network_mode = True
                print("INFO: Conexión de red exitosa. Usando ruta de producción.")
            else:
                raise ConnectionError("Directorio de red no existe o no hay permisos de escritura.")
        except Exception as e:
            self.connection_error = str(e)
            print(f"ADVERTENCIA: No se pudo usar la ruta de red ({self.connection_error}). Haciendo fallback a modo local.")
            self.active_path = Config.EXCEL_LOCAL_PATH
            self.is_network_mode = False

    def _ensure_excel_exists(self):
        """Verifica que el archivo Excel exista en la ruta activa; si no, lo crea."""
        if not self.active_path.exists():
            df = pd.DataFrame(columns=self.columns)
            self.active_path.parent.mkdir(parents=True, exist_ok=True)
            df.to_excel(self.active_path, index=False)
    
    def load_data(self) -> pd.DataFrame:
        """
        Load data from Excel file.
        
        Returns:
            pd.DataFrame: The loaded data
        """
        try:
            return pd.read_excel(self.active_path)
        except Exception as e:
            print(f"Error loading data: {e}")
            return pd.DataFrame(columns=self.columns)
    
    def save_data(self, df: pd.DataFrame) -> bool:
        """
        Save data to Excel file.
        
        Args:
            df (pd.DataFrame): Data to save
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            df.to_excel(self.active_path, index=False)
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False
    
    def get_next_id(self) -> int:
        """
        Get the next available ID for a new record.
        
        Returns:
            int: Next available ID
        """
        df = self.load_data()
        if df.empty:
            return 1
        return df['ID'].max() + 1 if 'ID' in df.columns else 1
    
    def add_record(self, record_data: Dict) -> bool:
        """
        Add a new record to the Excel file.
        
        Args:
            record_data (Dict): Record data to add
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            df = self.load_data()
            
            # Add ID if not present
            if 'ID' not in record_data:
                record_data['ID'] = self.get_next_id()
            
            # Create new row
            new_row = pd.DataFrame([record_data])
            df = pd.concat([df, new_row], ignore_index=True)
            
            return self.save_data(df)
        except Exception as e:
            print(f"Error adding record: {e}")
            return False
    
    def find_by_serial(self, serial_number: str) -> Optional[Dict]:
        """
        Find a record by serial number.
        
        Args:
            serial_number (str): Serial number to search for
            
        Returns:
            Optional[Dict]: Record data if found, None otherwise
            
        Raises:
            ValueError: If serial_number is None or empty
        """
        # Validación de entrada para robustez
        if not serial_number or not str(serial_number).strip():
            raise ValueError(Config.MSG_ERROR_SERIAL_VACIO)
        
        try:
            # Usar el método existente para mantener consistencia arquitectónica
            df = self.load_data()
            
            # Validar DataFrame vacío
            if df.empty:
                return None
            
            # Búsqueda eficiente y exacta sin modificar el DataFrame original
            search_term = str(serial_number).strip()
            result = df[df['Numero de Serie'].astype(str).str.strip() == search_term]
            
            if not result.empty:
                return result.iloc[0].to_dict()
            return None
            
        except Exception as e:
            # Mantener consistencia con el patrón de logging existente
            print(f"Error finding record: {e}")
            return None 