# src/main_app.py
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from src.config import Config  # Usar la clase Config existente
from src.data_manager import DataManager
from src.views.registration_view import RegistrationView

class MainApp(QMainWindow):
    """
    La ventana principal de la aplicación RETI-C.
    Carga la vista de registro del MVP.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{Config.APP_NAME} v{Config.APP_VERSION}")
        self.setGeometry(100, 100, 800, 700) # Ajustar altura para todos los campos

        # Crear instancia del DataManager
        self.data_manager = DataManager()

        # Cargar estilos CFE usando el método existente
        self.load_styles()
            
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        main_layout = QVBoxLayout(self.central_widget)

        # Cargar la vista de registro con inyección de dependencias
        self.registration_page = RegistrationView(self.data_manager)
        main_layout.addWidget(self.registration_page)
    
    def load_styles(self):
        """Carga los estilos CFE si están disponibles."""
        if Config.STYLES_FILE.exists():
            try:
                with open(Config.STYLES_FILE, 'r') as f:
                    self.setStyleSheet(f.read())
            except Exception as e:
                print(f"Error loading styles: {e}") 