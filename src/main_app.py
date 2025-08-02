"""
Main Application module for RETI-C.
Contains the main window and UI logic.

Author: Carlos Verastegui
Version: 1.0
Date: 02/08/2025
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QFormLayout, QLineEdit, QPushButton, QMessageBox,
    QLabel, QDateEdit, QTextEdit
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
from datetime import datetime
from typing import Dict

from .config import Config
from .data_manager import DataManager


class MainWindow(QMainWindow):
    """Main window for RETI-C application."""
    
    def __init__(self):
        """Initialize the main window."""
        super().__init__()
        self.data_manager = DataManager()
        self.init_ui()
        self.load_styles()
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle(f"{Config.APP_NAME} v{Config.APP_VERSION}")
        self.setGeometry(100, 100, 800, 600)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Add title
        title_label = QLabel("Registro de Equipos de Tecnologías de Información")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        main_layout.addWidget(title_label)
        
        # Create form
        self.create_form(main_layout)
        
        # Create buttons
        self.create_buttons(main_layout)
    
    def create_form(self, parent_layout):
        """Create the form layout."""
        form_layout = QFormLayout()
        
        # Create form fields
        self.fields = {}
        
        # Required fields
        self.fields['Tipo de Equipo'] = QLineEdit()
        self.fields['Marca y Modelo'] = QLineEdit()
        self.fields['Numero de Serie'] = QLineEdit()
        self.fields['Fecha de Recepcion'] = QDateEdit()
        self.fields['Descripcion del Problema'] = QTextEdit()
        self.fields['Responsable Recepcion'] = QLineEdit()
        self.fields['Estado'] = QLineEdit()
        
        # Optional fields
        self.fields['Fecha de Entrega'] = QDateEdit()
        self.fields['Componentes Entregados'] = QLineEdit()
        self.fields['Historial Intervenciones'] = QTextEdit()
        
        # Set default values
        self.fields['Fecha de Recepcion'].setDate(QDate.currentDate())
        self.fields['Estado'].setText("Recibido")
        
        # Add fields to form
        for field_name, field_widget in self.fields.items():
            if isinstance(field_widget, QTextEdit):
                field_widget.setMaximumHeight(60)
            form_layout.addRow(field_name, field_widget)
        
        parent_layout.addLayout(form_layout)
    
    def create_buttons(self, parent_layout):
        """Create the button layout."""
        button_layout = QHBoxLayout()
        
        # Save button
        self.save_button = QPushButton("Guardar Registro")
        self.save_button.clicked.connect(self.save_record)
        button_layout.addWidget(self.save_button)
        
        # Clear button
        self.clear_button = QPushButton("Limpiar Formulario")
        self.clear_button.clicked.connect(self.clear_form)
        button_layout.addWidget(self.clear_button)
        
        parent_layout.addLayout(button_layout)
    
    def load_styles(self):
        """Load CFE styles if available."""
        if Config.STYLES_FILE.exists():
            try:
                with open(Config.STYLES_FILE, 'r') as f:
                    self.setStyleSheet(f.read())
            except Exception as e:
                print(f"Error loading styles: {e}")
    
    def get_form_data(self) -> Dict:
        """Get data from form fields."""
        data = {}
        
        for field_name, field_widget in self.fields.items():
            if isinstance(field_widget, QLineEdit):
                data[field_name] = field_widget.text()
            elif isinstance(field_widget, QDateEdit):
                data[field_name] = field_widget.date().toString("yyyy-MM-dd")
            elif isinstance(field_widget, QTextEdit):
                data[field_name] = field_widget.toPlainText()
        
        return data
    
    def validate_form(self) -> bool:
        """Validate required fields."""
        data = self.get_form_data()
        
        for required_field in Config.REQUIRED_FIELDS:
            if not data.get(required_field, '').strip():
                QMessageBox.warning(
                    self,
                    "Campos Requeridos",
                    f"El campo '{required_field}' es obligatorio."
                )
                return False
        
        return True
    
    def save_record(self):
        """Save the current record."""
        if not self.validate_form():
            return
        
        data = self.get_form_data()
        
        if self.data_manager.add_record(data):
            QMessageBox.information(
                self,
                "Éxito",
                "Registro guardado correctamente."
            )
            self.clear_form()
        else:
            QMessageBox.critical(
                self,
                "Error",
                "Error al guardar el registro."
            )
    
    def clear_form(self):
        """Clear all form fields."""
        for field_widget in self.fields.values():
            if isinstance(field_widget, QLineEdit):
                field_widget.clear()
            elif isinstance(field_widget, QDateEdit):
                field_widget.setDate(QDate.currentDate())
            elif isinstance(field_widget, QTextEdit):
                field_widget.clear()
        
        # Reset default values
        self.fields['Fecha de Recepcion'].setDate(QDate.currentDate())
        self.fields['Estado'].setText("Recibido") 