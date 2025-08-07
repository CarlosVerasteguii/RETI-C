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
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QIcon

# Mantener los imports del sistema de hilos y la app principal
from src.main_app import MainApp
from src.data_manager_initializer import DataManagerInitializer
from src.config import Config


class ProfessionalSplashScreen(QWidget):
    """
    La implementación visualmente superior del splash screen, ahora integrada en producción.
    """
    def __init__(self):
        super().__init__()
        
        # --- Configuración de la Ventana ---
        self.setFixedSize(*Config.SPLASH_WINDOW_SIZE)
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowTitle("RETI-C - Iniciando...")

        icon_path = Config.RESOURCES_DIR / "app_icon.ico"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))

        # --- Layouts y Contenedor ---
        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        container = QWidget()
        container.setStyleSheet("background-color: white;")
        main_layout.addWidget(container)
        
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(1, 1, 1, 1)
        container_layout.setSpacing(0)

        center_area = QWidget()
        center_layout = QVBoxLayout(center_area)
        center_layout.addStretch()
        
        self.logo_label = QLabel()
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logo_label.setFixedSize(*Config.SPLASH_LOGO_SIZE)
        center_layout.addWidget(self.logo_label, alignment=Qt.AlignmentFlag.AlignCenter)
        center_layout.addStretch()
        
        status_bar = QWidget()
        status_bar.setFixedHeight(Config.SPLASH_STATUS_BAR_HEIGHT)
        status_bar_layout = QHBoxLayout(status_bar)
        status_bar_layout.setContentsMargins(*Config.SPLASH_STATUS_BAR_MARGINS)

        self.message_label = QLabel("Iniciando RETI-C...")
        self.message_label.setStyleSheet(f"""
            color: {Config.COLOR_GRAY_TEXT}; 
            font-size: {Config.SPLASH_STATUS_FONT_SIZE};
            font-weight: normal;
            font-family: "Segoe UI", Arial, sans-serif;
        """)
        status_bar_layout.addWidget(self.message_label, alignment=Qt.AlignmentFlag.AlignVCenter)
        status_bar_layout.addStretch()

        container_layout.addWidget(center_area)
        container_layout.addWidget(status_bar)
        
        self._load_logo()
        self._center_on_screen()

    def _load_logo(self):
        """Carga el logo RETI-C desde el archivo PNG."""
        logo_path = Config.RESOURCES_DIR / "logo-retic.png"  # Usar el logo correcto
        
        if logo_path.exists():
            try:
                logo_pixmap = QPixmap(str(logo_path))
                if not logo_pixmap.isNull():
                    scaled_pixmap = logo_pixmap.scaled(*Config.SPLASH_LOGO_SIZE, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                    self.logo_label.setPixmap(scaled_pixmap)
                else:
                    self._set_fallback_logo()
            except Exception as e:
                print(f"Error cargando logo RETI-C: {e}")
                self._set_fallback_logo()
        else:
            self._set_fallback_logo()
    
    def _set_fallback_logo(self):
        """Establece un logo de fallback si no se puede cargar el PNG."""
        fallback_text = Config.MSG_FALLBACK_LOGO_TEXT
        self.logo_label.setText(fallback_text)
        self.logo_label.setStyleSheet(f"""
            QLabel {{
                color: {Config.COLOR_CFE_GREEN};
                font-size: 18pt;
                font-weight: bold;
                background-color: transparent;
            }}
        """)

    def _center_on_screen(self):
        """Centra la ventana en la pantalla."""
        screen_geometry = QApplication.primaryScreen().geometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)

    def update_message(self, message: str):
        """Actualiza el mensaje de estado (para ser llamado por el inicializador)."""
        self.message_label.setText(message)
        QApplication.processEvents()


def on_data_manager_ready(data_manager):
    """Callback de éxito del inicializador."""
    global main_window  # Hacer main_window global para evitar garbage collection
    main_window = MainApp(data_manager)
    main_window.update_connection_status()
    main_window.show()
    splash.close()


def on_data_manager_error(error_message):
    """Callback de error del inicializador."""
    from PyQt6.QtWidgets import QMessageBox
    QMessageBox.critical(None, "Error de Inicialización", f"No se pudo iniciar la aplicación:\n{error_message}")
    # Asegurarse de cerrar el splash en caso de error para no dejarlo colgado
    splash.close()


def main():
    """Punto de entrada principal que integra el splash screen profesional."""
    global app, splash, main_window
    
    app = QApplication(sys.argv)
    
    # Usar la nueva y unificada clase de splash screen
    splash = ProfessionalSplashScreen()
    splash.show()
    app.processEvents()
    
    # El sistema de hilos y señales de `run.py` se mantiene, es la parte robusta.
    initializer = DataManagerInitializer()
    
    # Conectar señales
    initializer.finished.connect(on_data_manager_ready)
    initializer.error.connect(on_data_manager_error)
    
    initializer.start()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main() 