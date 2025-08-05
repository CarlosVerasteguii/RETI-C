"""
Data Manager Initializer for RETI-C application.
Handles asynchronous initialization of DataManager to prevent UI blocking.

Author: Carlos Verastegui
Version: 1.0
Date: 05/08/2025
"""

from PyQt6.QtCore import QThread, pyqtSignal
from src.data_manager import DataManager


class DataManagerInitializer(QThread):
    """
    Thread para inicializar DataManager de forma asíncrona.
    Previene el bloqueo de la UI durante la inicialización.
    """
    
    # Señal emitida cuando la inicialización se completa exitosamente
    finished = pyqtSignal(DataManager)
    
    # Señal emitida si ocurre un error durante la inicialización
    error = pyqtSignal(str)
    
    def __init__(self):
        """Inicializa el thread de inicialización."""
        super().__init__()
        self.data_manager = None
    
    def run(self):
        """
        Ejecuta la inicialización del DataManager en el hilo secundario.
        Emite señales según el resultado.
        """
        try:
            # Inicializar DataManager (operación potencialmente lenta)
            self.data_manager = DataManager()
            
            # Emitir señal de éxito con el DataManager inicializado
            self.finished.emit(self.data_manager)
            
        except Exception as e:
            # Emitir señal de error con el mensaje de excepción
            self.error.emit(str(e)) 