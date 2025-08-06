#!/usr/bin/env python3
"""
Script temporal para probar el splash screen con refinamientos finales.
"""

import sys
import time
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QPainter, QIcon
from PyQt6.QtSvg import QSvgRenderer


class ProfessionalSplashScreen(QWidget):
    """
    Un widget de splash screen personalizado que replica el layout limpio y
    profesional del splash screen de Microsoft PowerPoint, con refinamiento final.
    """
    
    def __init__(self):
        super().__init__()
        
        # --- Configuración de la Ventana ---
        self.setFixedSize(700, 650)  # Ventana más grande para acomodar el logo
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowTitle("RETI-C - Iniciando...")
        
        # 1. Branding: Establecer el icono de la aplicación en la barra de título
        icon_path = Path("resources/app_icon.ico")
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))

        # --- Layout Principal y Contenedor Blanco ---
        # Este es nuestro "lienzo" principal
        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        container = QWidget()
        container.setStyleSheet("background-color: white;")
        main_layout.addWidget(container)
        
        # --- Layout Interno del Contenedor ---
        # Este layout organizará los elementos DENTRO del lienzo blanco
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(1, 1, 1, 1) # Margen sutil
        container_layout.setSpacing(0)

        # --- 1. Área Central para el Logo ---
        # Usamos un widget y un layout para centrar el logo perfectamente
        center_area = QWidget()
        center_layout = QVBoxLayout(center_area)
        center_layout.addStretch() # Empuja el logo hacia abajo
        
        # Logo CFE centrado
        self.logo_label = QLabel()
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logo_label.setFixedSize(630, 600) # Tamaño mucho más grande para máxima prominencia
        center_layout.addWidget(self.logo_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        center_layout.addStretch() # Empuja el logo hacia arriba
        
        # --- 2. Barra de Estado Inferior para el Mensaje ---
        # Un widget con altura fija para el área del mensaje
        status_bar = QWidget()
        status_bar.setFixedHeight(40)
        status_bar_layout = QHBoxLayout(status_bar)
        
        # 2. Refinamiento de Padding: Aumentar los márgenes para dar más "aire" al texto
        status_bar_layout.setContentsMargins(20, 0, 20, 5) # Mayor margen izquierdo e inferior

        self.message_label = QLabel("Iniciando RETI-C...")
        
        # 3. Refinamiento de Fuente: Hacer el texto más sutil y profesional
        self.message_label.setStyleSheet("""
            QLabel {
                color: #666666; 
                font-size: 10pt;
                font-weight: normal;
                font-family: "Segoe UI", Arial, sans-serif;
            }
        """)
        
        status_bar_layout.addWidget(self.message_label, alignment=Qt.AlignmentFlag.AlignVCenter) # Alineado a la izquierda por defecto
        status_bar_layout.addStretch() # Empuja el texto a la izquierda

        # --- Ensamblar el Layout del Contenedor ---
        container_layout.addWidget(center_area)
        container_layout.addWidget(status_bar)
        
        # Cargar logo
        self._load_logo()
        
        # Centrar en pantalla
        self._center_on_screen()
        
        # Configurar timer para cerrar después de 5 segundos
        self.timer = QTimer()
        self.timer.timeout.connect(self.close)
        self.timer.start(5000)  # 5 segundos
    
    def _load_logo(self):
        """Carga el logo RETI-C desde el archivo PNG."""
        logo_path = Path("resources/logo-retic.png")
        
        if logo_path.exists():
            try:
                # Cargar PNG directamente
                logo_pixmap = QPixmap(str(logo_path))
                if not logo_pixmap.isNull():
                    # Escalar al tamaño mucho más grande para máxima prominencia
                    logo_pixmap = logo_pixmap.scaled(630, 600, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                    self.logo_label.setPixmap(logo_pixmap)
                else:
                    self._set_fallback_logo()
            except Exception as e:
                print(f"Error cargando logo RETI-C: {e}")
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
                font-size: 18pt;
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


def main():
    """Función principal para probar el splash screen refinado."""
    app = QApplication(sys.argv)
    
    # Crear y mostrar splash screen
    splash = ProfessionalSplashScreen()
    splash.show()
    
    print("Splash screen refinado mostrado por 5 segundos...")
    
    # Ejecutar aplicación
    sys.exit(app.exec())


if __name__ == "__main__":
    main() 