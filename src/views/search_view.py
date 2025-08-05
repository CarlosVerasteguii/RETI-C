# src/views/search_view.py
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QTextEdit, QFrame)
from PyQt6.QtCore import Qt
from src.config import Config

class SearchView(QWidget):
    """
    Vista para búsqueda de equipos por número de serie.
    Permite consultar el historial completo de un equipo.
    """
    
    def __init__(self, data_manager):
        super().__init__()
        self.data_manager = data_manager
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz de usuario de búsqueda."""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(Config.UI_LAYOUT_SPACING)
        main_layout.setContentsMargins(*Config.UI_VIEW_MARGINS)
        
        # Header
        self.create_header_section(main_layout)
        
        # Search Section
        self.create_search_section(main_layout)
        
        # Results Section
        self.create_results_section(main_layout)
        
        # Spacer
        main_layout.addStretch()
    
    def create_header_section(self, parent_layout):
        """Crea la sección de encabezado."""
        header_layout = QVBoxLayout()
        header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title_label = QLabel("🔍 Consulta de Equipos")
        title_label.setObjectName("search_title")
        title_label.setStyleSheet(f"""
            #search_title {{
                color: {Config.COLOR_CFE_GREEN};
                font-size: 28px;
                font-weight: bold;
                margin-bottom: 10px;
            }}
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        subtitle_label = QLabel("Busca el historial completo de un equipo por su número de serie")
        subtitle_label.setObjectName("search_subtitle")
        subtitle_label.setStyleSheet(f"""
            #search_subtitle {{
                color: {Config.COLOR_GRAY_TEXT};
                font-size: 14px;
                margin-bottom: 20px;
            }}
        """)
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        header_layout.addWidget(title_label)
        header_layout.addWidget(subtitle_label)
        parent_layout.addLayout(header_layout)
    
    def create_search_section(self, parent_layout):
        """Crea la sección de búsqueda."""
        search_frame = QFrame()
        search_frame.setObjectName("search_frame")
        search_frame.setStyleSheet(f"""
            #search_frame {{
                background-color: {Config.COLOR_GRAY_LIGHT_BG};
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 20px;
            }}
        """)
        
        search_layout = QVBoxLayout(search_frame)
        search_layout.setSpacing(15)
        
        # Input Section
        input_layout = QHBoxLayout()
        
        label = QLabel("Número de Serie:")
        label.setStyleSheet("font-weight: bold; font-size: 14px;")
        
        self.serial_input = QLineEdit()
        self.serial_input.setPlaceholderText("Ej: SN-001-ABC123")
        self.serial_input.setStyleSheet(f"""
            QLineEdit {{
                padding: 10px;
                border: 2px solid #dee2e6;
                border-radius: 4px;
                font-size: 14px;
            }}
            QLineEdit:focus {{
                border-color: {Config.COLOR_CFE_GREEN};
            }}
        """)
        
        self.search_button = QPushButton("🔍 Buscar")
        self.search_button.setObjectName("primary_button")
        self.search_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {Config.COLOR_CFE_GREEN};
                color: {Config.COLOR_CFE_TEXT_ON_GREEN};
                border: none;
                padding: 10px 20px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 14px;
                min-width: 100px;
            }}
            QPushButton:hover {{
                background-color: {Config.COLOR_CFE_GREEN_DARK};
            }}
            QPushButton:pressed {{
                background-color: {Config.COLOR_CFE_GREEN_VERY_DARK};
            }}
        """)
        
        input_layout.addWidget(label)
        input_layout.addWidget(self.serial_input)
        input_layout.addWidget(self.search_button)
        input_layout.addStretch()
        
        search_layout.addLayout(input_layout)
        parent_layout.addWidget(search_frame)
        
        # Conectar señales
        self.search_button.clicked.connect(self.perform_search)
        self.serial_input.returnPressed.connect(self.perform_search)
    
    def create_results_section(self, parent_layout):
        """Crea la sección de resultados."""
        results_frame = QFrame()
        results_frame.setObjectName("results_frame")
        results_frame.setStyleSheet("""
            #results_frame {
                background-color: white;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 20px;
            }
        """)
        
        results_layout = QVBoxLayout(results_frame)
        
        # Results Header
        self.results_header = QLabel("Resultados de la búsqueda")
        self.results_header.setObjectName("results_header")
        self.results_header.setStyleSheet(f"""
            #results_header {{
                color: {Config.COLOR_CFE_GREEN};
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 10px;
            }}
        """)
        
        # Results Content
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setMaximumHeight(300)
        self.results_text.setStyleSheet(f"""
            QTextEdit {{
                border: 1px solid #dee2e6;
                border-radius: 4px;
                padding: 10px;
                font-family: 'Consolas', monospace;
                font-size: 12px;
                background-color: {Config.COLOR_GRAY_LIGHT_BG};
            }}
        """)
        
        results_layout.addWidget(self.results_header)
        results_layout.addWidget(self.results_text)
        parent_layout.addWidget(results_frame)
    
    def perform_search(self):
        """Ejecuta la búsqueda y muestra los resultados."""
        serial_number = self.serial_input.text().strip()
        
        if not serial_number:
            self.show_message("Por favor, ingresa un número de serie.", "warning")
            return
        
        try:
            result = self.data_manager.find_by_serial(serial_number)
            
            if result:
                self.display_result(result)
            else:
                self.show_message(f"No se encontró ningún equipo con el número de serie: {serial_number}", "info")
                
        except Exception as e:
            self.show_message(f"Error al realizar la búsqueda: {str(e)}", "error")
    
    def display_result(self, record):
        """Muestra el resultado de la búsqueda."""
        self.results_header.setText("✅ Equipo Encontrado")
        
        # Formatear resultado
        result_text = f"""
📋 INFORMACIÓN DEL EQUIPO
═══════════════════════════════════════════════════════════════════════════════

🆔 ID: {record.get('ID', 'N/A')}
💻 Tipo de Equipo: {record.get('Tipo de Equipo', 'N/A')}
🏷️  Marca y Modelo: {record.get('Marca y Modelo', 'N/A')}
🔢 Número de Serie: {record.get('Numero de Serie', 'N/A')}
📅 Fecha de Recepción: {record.get('Fecha de Recepcion', 'N/A')}
📤 Fecha de Entrega: {record.get('Fecha de Entrega', 'N/A')}
👤 Responsable: {record.get('Responsable Recepcion', 'N/A')}
📊 Estado: {record.get('Estado', 'N/A')}

🔧 DESCRIPCIÓN DEL PROBLEMA
═══════════════════════════════════════════════════════════════════════════════
{record.get('Descripcion del Problema', 'No especificado')}

📦 COMPONENTES ENTREGADOS
═══════════════════════════════════════════════════════════════════════════════
{record.get('Componentes Entregados', 'No especificado')}

📝 HISTORIAL DE INTERVENCIONES
═══════════════════════════════════════════════════════════════════════════════
{record.get('Historial Intervenciones', 'Sin intervenciones registradas')}
"""
        
        self.results_text.setPlainText(result_text)
    
    def show_message(self, message, message_type="info"):
        """Muestra un mensaje al usuario."""
        self.results_header.setText("ℹ️ Información")
        
        if message_type == "warning":
            self.results_text.setPlainText(f"⚠️ {message}")
        elif message_type == "error":
            self.results_text.setPlainText(f"❌ {message}")
        else:
            self.results_text.setPlainText(f"ℹ️ {message}")