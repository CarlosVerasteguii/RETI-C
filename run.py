#!/usr/bin/env python3
"""
RETI-C - Registro de Equipos de Tecnologías de Información - Carlos
Entry point for the desktop application.

Author: Carlos Verastegui
Version: 1.0
Date: 02/08/2025
"""

import sys
from PyQt6.QtWidgets import QApplication, QSplashScreen
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QFont
from src.main_app import MainApp
from src.data_manager_initializer import DataManagerInitializer
from src.config import Config


def show_splash_screen():
    """
    Crea y muestra el splash screen inicial.
    
    Returns:
        QSplashScreen: Instancia del splash screen configurado
    """
    # Crear splash screen simple (Fase 1)
    splash = QSplashScreen()
    splash.setWindowTitle("RETI-C - Iniciando...")
    
    # Configurar mensaje inicial
    splash.showMessage(
        "Iniciando RETI-C...\nVerificando conexión de red...",
        Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom,
        Qt.GlobalColor.white
    )
    
    # Configurar fuente y estilos
    font = QFont()
    font.setPointSize(10)
    font.setBold(True)
    splash.setFont(font)
    
    # Configurar geometría y estilo
    splash.setGeometry(100, 100, 400, 200)
    splash.setStyleSheet("""
        QSplashScreen {
            background-color: #008E5A;
            color: white;
            border: 2px solid #006B47;
            border-radius: 10px;
        }
    """)
    
    return splash


def on_data_manager_ready(data_manager):
    """
    Callback ejecutado cuando DataManager está listo.
    
    Args:
        data_manager: Instancia inicializada de DataManager
    """
    # Crear ventana principal con DataManager listo
    main_window = MainApp(data_manager)
    
    # Actualizar estado de conexión
    main_window.update_connection_status()
    
    # Mostrar ventana principal
    main_window.show()
    
    # Cerrar splash screen
    splash.finish(main_window)


def on_data_manager_error(error_message):
    """
    Callback ejecutado si hay error en la inicialización.
    
    Args:
        error_message: Mensaje de error
    """
    from PyQt6.QtWidgets import QMessageBox
    
    # Mostrar mensaje de error
    QMessageBox.critical(
        None,
        "Error de Inicialización",
        f"No se pudo inicializar la aplicación:\n{error_message}"
    )
    
    # Cerrar aplicación
    app.quit()


def main():
    """Main entry point for the RETI-C application."""
    global app, splash
    
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("RETI-C")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("CFE")
    
    # Mostrar splash screen inmediatamente
    splash = show_splash_screen()
    splash.show()
    
    # Procesar eventos para mostrar splash screen
    app.processEvents()
    
    # Crear thread de inicialización
    initializer = DataManagerInitializer()
    
    # Conectar señales
    initializer.finished.connect(on_data_manager_ready)
    initializer.error.connect(on_data_manager_error)
    
    # Iniciar inicialización asíncrona
    initializer.start()
    
    # Start the application
    sys.exit(app.exec())


if __name__ == "__main__":
    main() 