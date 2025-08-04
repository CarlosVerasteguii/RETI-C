# src/views/dashboard_view.py
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame
from PyQt6.QtCore import Qt
from src.config import Config

class DashboardView(QWidget):
    """
    Vista de bienvenida o panel principal de RETI-C.
    Proporciona información general y acceso rápido a funcionalidades principales.
    """
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        """Configura la interfaz de usuario del dashboard."""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(30)
        main_layout.setContentsMargins(40, 40, 40, 40)
        
        # Header Section
        self.create_header_section(main_layout)
        
        # Stats/Info Section (placeholder para futuras métricas)
        self.create_info_section(main_layout)
        
        # Spacer para centrar verticalmente
        main_layout.addStretch()

    def create_header_section(self, parent_layout):
        """Crea la sección de encabezado con título y bienvenida."""
        header_layout = QVBoxLayout()
        header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Título principal
        title_label = QLabel(f"Sistema {Config.APP_NAME}")
        title_label.setObjectName("dashboard_title")
        title_label.setStyleSheet("""
            #dashboard_title {
                color: #008E5A;
                font-size: 32px;
                font-weight: bold;
                margin-bottom: 10px;
            }
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Subtítulo descriptivo
        subtitle_label = QLabel("Registro de Equipos de Tecnologías de Información")
        subtitle_label.setObjectName("dashboard_subtitle")
        subtitle_label.setStyleSheet("""
            #dashboard_subtitle {
                color: #666666;
                font-size: 16px;
                margin-bottom: 20px;
            }
        """)
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Mensaje de bienvenida
        welcome_label = QLabel("Seleccione una opción de la barra de navegación para comenzar")
        welcome_label.setObjectName("dashboard_welcome")
        welcome_label.setStyleSheet("""
            #dashboard_welcome {
                color: #333333;
                font-size: 14px;
                font-style: italic;
            }
        """)
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        header_layout.addWidget(title_label)
        header_layout.addWidget(subtitle_label)
        header_layout.addWidget(welcome_label)
        
        parent_layout.addLayout(header_layout)

    def create_info_section(self, parent_layout):
        """Crea la sección de información del sistema."""
        info_frame = QFrame()
        info_frame.setObjectName("info_frame")
        info_frame.setStyleSheet("""
            #info_frame {
                background-color: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 8px;
                padding: 20px;
                margin: 20px 0px;
            }
        """)
        info_frame.setMaximumWidth(600)
        info_frame.setFixedHeight(150)
        
        info_layout = QVBoxLayout(info_frame)
        info_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Información de la versión
        version_label = QLabel(f"Versión {Config.APP_VERSION}")
        version_label.setStyleSheet("font-weight: bold; color: #008E5A; font-size: 14px;")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Información organizacional
        org_label = QLabel(f"{Config.ORGANIZATION} - Departamento de TI")
        org_label.setStyleSheet("color: #666666; font-size: 12px; margin-top: 5px;")
        org_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Funcionalidades disponibles
        features_label = QLabel("✓ Registro de equipos\n✓ Gestión de inventario\n✓ Historial de intervenciones")
        features_label.setStyleSheet("""
            color: #333333; 
            font-size: 12px; 
            margin-top: 15px;
            line-height: 1.4;
        """)
        features_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        info_layout.addWidget(version_label)
        info_layout.addWidget(org_label)
        info_layout.addWidget(features_label)
        
        # Centrar el frame horizontalmente
        frame_container = QHBoxLayout()
        frame_container.addStretch()
        frame_container.addWidget(info_frame)
        frame_container.addStretch()
        
        parent_layout.addLayout(frame_container)