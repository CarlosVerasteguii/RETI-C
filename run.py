#!/usr/bin/env python3
"""
RETI-C - Registro de Equipos de Tecnologías de Información - Carlos
Entry point for the desktop application.

Author: Carlos Verastegui
Version: 1.0
Date: 02/08/2025
"""

import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QSplashScreen, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QFont, QPainter
from PyQt6.QtSvg import QSvgRenderer
from src.main_app import MainApp
from src.data_manager_initializer import DataManagerInitializer
from src.config import Config


class CustomSplashScreen(QWidget):
    """
    Splash screen personalizado que replica exactamente el estilo de Microsoft PowerPoint.
    """
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RETI-C - Iniciando...")
        self.setFixedSize(600, 400)
        
        # Configurar como ventana estándar (sin efectos de transparencia)
        self.setWindowFlags(Qt.WindowType.Window)
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Área principal para el logo (centrada)
        logo_container = QWidget()
        logo_container.setFixedHeight(320)  # Área principal para logo
        logo_layout = QVBoxLayout(logo_container)
        logo_layout.setContentsMargins(0, 0, 0, 0)
        logo_layout.setSpacing(0)
        
        # Logo CFE centrado
        self.logo_label = QLabel()
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logo_label.setFixedSize(400, 160)
        logo_layout.addWidget(self.logo_label, 0, Qt.AlignmentFlag.AlignCenter)
        
        # Agregar área de logo al layout principal
        main_layout.addWidget(logo_container)
        
        # Barra de estado inferior (altura fija)
        status_container = QWidget()
        status_container.setFixedHeight(80)
        status_container.setStyleSheet("""
            QWidget {
                background-color: #FFFFFF;
                border-top: 1px solid #E0E0E0;
            }
        """)
        
        status_layout = QHBoxLayout(status_container)
        status_layout.setContentsMargins(20, 10, 20, 20)
        status_layout.setSpacing(0)
        
        # Mensaje de estado (esquina inferior izquierda)
        self.status_label = QLabel("Iniciando RETI-C...")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)
        self.status_label.setStyleSheet("""
            QLabel {
                color: #666666;
                font-size: 12pt;
                font-family: "Segoe UI", Arial, sans-serif;
                background-color: transparent;
            }
        """)
        status_layout.addWidget(self.status_label)
        status_layout.addStretch()  # Espacio a la derecha
        
        # Agregar barra de estado al layout principal
        main_layout.addWidget(status_container)
        
        # Cargar logo
        self._load_logo()
        
        # Centrar en pantalla
        self._center_on_screen()
        
        # Aplicar estilos (fondo blanco puro, sin bordes)
        self.setStyleSheet("""
            QWidget {
                background-color: #FFFFFF;
            }
        """)
    
    def _load_logo(self):
        """Carga el logo CFE desde el archivo SVG."""
        logo_path = Path("resources/cfe_logo.svg")
        
        if logo_path.exists():
            try:
                # Usar QSvgRenderer para cargar SVG
                renderer = QSvgRenderer(str(logo_path))
                if renderer.isValid():
                    # Crear pixmap con tamaño fijo
                    logo_pixmap = QPixmap(400, 160)
                    logo_pixmap.fill(Qt.GlobalColor.transparent)
                    
                    # Renderizar SVG en el pixmap
                    painter = QPainter(logo_pixmap)
                    renderer.render(painter)
                    painter.end()
                    
                    self.logo_label.setPixmap(logo_pixmap)
                else:
                    self._set_fallback_logo()
            except Exception as e:
                print(f"Error cargando logo CFE: {e}")
                self._set_fallback_logo()
        else:
            self._set_fallback_logo()
    
    def _set_fallback_logo(self):
        """Establece un logo de fallback si no se puede cargar el SVG."""
        fallback_text = "CFE\nComisión Federal de Electricidad"
        self.logo_label.setText(fallback_text)
        self.logo_label.setStyleSheet("""
            QLabel {
                color: #008E5A;
                font-size: 24pt;
                font-weight: bold;
                background-color: transparent;
        }
    """)
    
    def _center_on_screen(self):
        """Centra la ventana en la pantalla."""
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)
    
    def update_message(self, message):
        """Actualiza el mensaje de estado."""
        self.status_label.setText(f"Iniciando RETI-C...\n{message}")
        QApplication.processEvents()


def show_splash_screen():
    """
    Crea y muestra el splash screen personalizado con logo CFE.
    
    Returns:
        CustomSplashScreen: Instancia del splash screen personalizado
    """
    return CustomSplashScreen()


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
    splash.close()


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


def main():
    """
    Función principal que inicia la aplicación con splash screen personalizado.
    """
    global app, splash
    
    # Crear aplicación
    app = QApplication(sys.argv)
    
    # Mostrar splash screen personalizado
    splash = show_splash_screen()
    splash.show()
    
    # Procesar eventos para mostrar el splash screen inmediatamente
    app.processEvents()
    
    # Crear inicializador de DataManager en hilo separado
    initializer = DataManagerInitializer()
    
    # Conectar señales
    initializer.finished.connect(on_data_manager_ready)
    initializer.error.connect(on_data_manager_error)
    
    # Iniciar inicialización en hilo separado
    initializer.start()
    
    # Ejecutar aplicación
    sys.exit(app.exec())


if __name__ == "__main__":
    main() 