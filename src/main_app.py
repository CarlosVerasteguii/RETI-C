# src/main_app.py
import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QStackedWidget, QStatusBar)
from PyQt6.QtCore import Qt
from src.config import Config
from src.data_manager import DataManager
from src.views.registration_view import RegistrationView
from src.views.dashboard_view import DashboardView
from src.views.search_view import SearchView

class MainApp(QMainWindow):
    """
    La ventana principal de la aplicación RETI-C.
    Actúa como el contenedor principal, gestionando la navegación entre vistas.
    """
    def __init__(self, data_manager=None):
        super().__init__()
        self.setWindowTitle(f"{Config.APP_NAME} v{Config.APP_VERSION}")
        self.setGeometry(*Config.WINDOW_MAIN_GEOMETRY)

        # Inicializar servicios (DataManager puede ser None inicialmente)
        self.data_manager = data_manager
        
        # Cargar estilos CFE
        self.load_styles()
        
        # Configurar UI
        self.setup_ui()
        
        # Conectar señales de navegación
        self.setup_navigation_signals()
        
        # Iniciar en la vista del Dashboard
        self.stacked_widget.setCurrentIndex(0)
        
        # Configurar estado de conexión en la barra de estado (solo si DataManager está disponible)
        if self.data_manager:
            self.update_connection_status()

    def setup_ui(self):
        """Configura la interfaz de usuario principal."""
        # Widget central y layout principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Barra de navegación superior
        self.setup_navigation_bar()

        # Área de contenido con vistas apiladas
        self.setup_stacked_widget()

        # Barra de estado
        self.setup_status_bar()

    def setup_navigation_bar(self):
        """Crea y configura la barra de navegación superior con estilos CFE."""
        nav_bar = QWidget()
        nav_bar.setObjectName("nav_bar")
        nav_bar.setStyleSheet(f"""
            #nav_bar {{ 
                background-color: {Config.COLOR_CFE_GREEN}; 
                border-bottom: 2px solid {Config.COLOR_CFE_GREEN_DARK};
                min-height: 50px;
            }}
        """)
        
        nav_layout = QHBoxLayout(nav_bar)
        nav_layout.setContentsMargins(15, 8, 15, 8)
        nav_layout.setSpacing(10)

        # Botones de navegación
        self.btn_dashboard = QPushButton("🏠 Dashboard")
        self.btn_registro = QPushButton("➕ Registrar Equipo")
        self.btn_busqueda = QPushButton("🔍 Consultar")
        
        # Aplicar estilos CFE a los botones de navegación
        nav_button_style = f"""
            QPushButton {{
                background-color: transparent;
                color: {Config.COLOR_CFE_TEXT_ON_GREEN};
                border: 1px solid transparent;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 14px;
                border-radius: 4px;
                min-width: 140px;
            }}
            QPushButton:hover {{
                background-color: {Config.COLOR_CFE_GREEN_DARK};
                border: 1px solid {Config.COLOR_CFE_GREEN_VERY_DARK};
            }}
            QPushButton:pressed {{
                background-color: {Config.COLOR_CFE_GREEN_VERY_DARK};
            }}
            QPushButton:checked {{
                background-color: {Config.COLOR_CFE_GREEN_DARK};
                border: 1px solid {Config.COLOR_CFE_GREEN_VERY_DARK};
            }}
        """
        
        self.btn_dashboard.setObjectName("nav_button")
        self.btn_registro.setObjectName("nav_button")
        self.btn_busqueda.setObjectName("nav_button")
        self.btn_dashboard.setStyleSheet(nav_button_style)
        self.btn_registro.setStyleSheet(nav_button_style)
        self.btn_busqueda.setStyleSheet(nav_button_style)
        
        # Hacer los botones checkables para mostrar estado activo
        self.btn_dashboard.setCheckable(True)
        self.btn_registro.setCheckable(True)
        self.btn_busqueda.setCheckable(True)
        self.btn_dashboard.setChecked(True)  # Dashboard activo por defecto
        
        nav_layout.addWidget(self.btn_dashboard)
        nav_layout.addWidget(self.btn_registro)
        nav_layout.addWidget(self.btn_busqueda)
        nav_layout.addStretch()

        self.main_layout.addWidget(nav_bar)
        
    def setup_stacked_widget(self):
        """Crea el QStackedWidget y añade todas las vistas."""
        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)

        # Crear instancias de las vistas con manejo de errores
        try:
            self.dashboard_page = DashboardView()
            
            # Crear vistas que requieren DataManager (pueden ser None inicialmente)
            self.registration_page = RegistrationView(self.data_manager) if self.data_manager else None
            self.search_page = SearchView(self.data_manager) if self.data_manager else None

            # Añadir las vistas al QStackedWidget en el orden deseado
            self.stacked_widget.addWidget(self.dashboard_page)    # Índice 0
            
            # Añadir placeholders si las vistas no están disponibles
            if self.registration_page:
                self.stacked_widget.addWidget(self.registration_page) # Índice 1
            else:
                from PyQt6.QtWidgets import QLabel
                placeholder_reg = QLabel("Cargando vista de registro...")
                placeholder_reg.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.stacked_widget.addWidget(placeholder_reg)
                
            if self.search_page:
                self.stacked_widget.addWidget(self.search_page)       # Índice 2
            else:
                from PyQt6.QtWidgets import QLabel
                placeholder_search = QLabel("Cargando vista de búsqueda...")
                placeholder_search.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.stacked_widget.addWidget(placeholder_search)
            
        except Exception as e:
            print(f"Error al crear las vistas: {e}")
            # En caso de error, mostrar mensaje pero no crashear
            from PyQt6.QtWidgets import QLabel
            error_label = QLabel(f"Error al cargar las vistas: {e}")
            error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.stacked_widget.addWidget(error_label)

    def setup_navigation_signals(self):
        """Conecta las señales de navegación entre vistas."""
        self.btn_dashboard.clicked.connect(lambda: self.navigate_to_view(0))
        self.btn_registro.clicked.connect(lambda: self.navigate_to_view(1))
        self.btn_busqueda.clicked.connect(lambda: self.navigate_to_view(2))

    def navigate_to_view(self, index: int):
        """
        Navega a la vista especificada y actualiza el estado visual de los botones.
        
        Args:
            index: Índice de la vista en el QStackedWidget
        """
        try:
            if 0 <= index < self.stacked_widget.count():
                self.stacked_widget.setCurrentIndex(index)
                
                # Actualizar estado visual de botones
                self.btn_dashboard.setChecked(index == 0)
                self.btn_registro.setChecked(index == 1)
                self.btn_busqueda.setChecked(index == 2)
            else:
                print(f"Error: Índice de vista inválido: {index}")
        except Exception as e:
            print(f"Error al navegar a la vista {index}: {e}")
    
    def setup_status_bar(self):
        """Configura la barra de estado para mostrar información de conexión."""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
    
    def update_connection_status(self):
        """Actualiza la barra de estado con el estado de conexión actual."""
        if not self.data_manager:
            self.status_bar.showMessage("⏳ Inicializando...")
            self.status_bar.setStyleSheet("background-color: #FFA500; color: black; font-weight: bold;")
            return
            
        if self.data_manager.is_network_mode:
            self.status_bar.showMessage("✅ Conectado a la Red Corporativa")
            self.status_bar.setStyleSheet(f"background-color: {Config.COLOR_CFE_GREEN}; color: white; font-weight: bold;")
        else:
            message = f"⚠️ Trabajando en Modo Local. Causa: {self.data_manager.connection_error}"
            self.status_bar.showMessage(message)
            self.status_bar.setStyleSheet("background-color: #FFA500; color: black; font-weight: bold;")
    
    def load_styles(self):
        """Carga los estilos CFE si están disponibles."""
        if Config.STYLES_FILE.exists():
            try:
                with open(Config.STYLES_FILE, 'r') as f:
                    self.setStyleSheet(f.read())
            except Exception as e:
                print(f"Error loading styles: {e}") 