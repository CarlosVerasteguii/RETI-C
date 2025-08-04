# src/views/registration_view.py
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QLineEdit, 
                             QPushButton, QLabel, QHBoxLayout, QMessageBox,
                             QDateEdit, QTextEdit)
from PyQt6.QtCore import QDate
from src.data_manager import DataManager
from src.config import Config

class RegistrationView(QWidget):
    """
    Encapsula toda la UI y la lógica para el registro de nuevos equipos.
    """
    def __init__(self, data_manager: DataManager):
        """
        Inicializa la vista de registro.

        Args:
            data_manager: Una instancia de la clase DataManager para la interacción con los datos.
        """
        super().__init__()
        self.data_manager = data_manager
        
        main_layout = QVBoxLayout(self)
        self.create_form_and_buttons(main_layout)

    def create_form_and_buttons(self, parent_layout: QVBoxLayout):
        """Crea el formulario completo y los botones de acción."""
        self.form_layout = QFormLayout()
        self.fields = {}

        # Recrear todos los campos para asegurar consistencia
        all_fields = ['Tipo de Equipo', 'Marca y Modelo', 'Numero de Serie', 'Fecha de Recepcion',
                      'Descripcion del Problema', 'Responsable Recepcion', 'Estado', 'Fecha de Entrega',
                      'Componentes Entregados', 'Historial Intervenciones']
        
        for field_name in all_fields:
            if field_name in ['Fecha de Recepcion', 'Fecha de Entrega']:
                self.fields[field_name] = QDateEdit()
            elif field_name in ['Descripcion del Problema', 'Historial Intervenciones']:
                self.fields[field_name] = QTextEdit()
                self.fields[field_name].setMaximumHeight(60)
            else:
                self.fields[field_name] = QLineEdit()
            
            self.form_layout.addRow(QLabel(f"{field_name}:"), self.fields[field_name])

        # Configurar valores por defecto
        self.fields['Fecha de Recepcion'].setDate(QDate.currentDate())
        self.fields['Estado'].setText("Recibido")
        self.fields['Estado'].setReadOnly(True)

        parent_layout.addLayout(self.form_layout)
        parent_layout.addStretch()

        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self.btn_limpiar = QPushButton("Limpiar Formulario")
        self.btn_limpiar.setObjectName("secondary_button")
        self.btn_limpiar.clicked.connect(self.clear_form)
        button_layout.addWidget(self.btn_limpiar)
        
        self.btn_guardar = QPushButton("Guardar Registro")
        self.btn_guardar.setObjectName("primary_button")
        self.btn_guardar.clicked.connect(self.save_record)
        button_layout.addWidget(self.btn_guardar)
        
        parent_layout.addLayout(button_layout)

    def clear_form(self):
        """Limpia todos los campos del formulario, reseteando los valores por defecto."""
        for field_name, field_widget in self.fields.items():
            if isinstance(field_widget, QLineEdit) and not field_widget.isReadOnly():
                field_widget.clear()
            elif isinstance(field_widget, QDateEdit):
                if field_name == 'Fecha de Entrega':
                    field_widget.clear() # Permitir que la fecha de entrega esté vacía
                else:
                    field_widget.setDate(QDate.currentDate())
            elif isinstance(field_widget, QTextEdit):
                field_widget.clear()
        
        self.fields['Estado'].setText("Recibido")
        self.fields['Fecha de Recepcion'].setDate(QDate.currentDate())


    def save_record(self):
        """Valida y guarda los datos del formulario utilizando el DataManager."""
        data = self.get_form_data()
        
        # Validación completa usando la lista de Config
        for required_field in Config.REQUIRED_FIELDS:
            if not data.get(required_field, '').strip():
                QMessageBox.warning(self, "Campos Requeridos", f"El campo '{required_field}' es obligatorio.")
                return

        # Usar el método correcto del data_manager y manejar el resultado
        if self.data_manager.add_record(data):
            QMessageBox.information(self, "Éxito", f"Equipo con S/N '{data.get('Numero de Serie', '')}' ha sido registrado.")
            self.clear_form()
        else:
            QMessageBox.critical(self, "Error de Guardado", "No se pudo guardar el registro en el archivo Excel. Verifique los permisos o si el archivo está en uso.")
    
    def get_form_data(self) -> dict:
        """Recopila los datos de todos los widgets del formulario en un diccionario."""
        data = {}
        for field_name, field_widget in self.fields.items():
            if isinstance(field_widget, QLineEdit):
                data[field_name] = field_widget.text()
            elif isinstance(field_widget, QDateEdit):
                data[field_name] = field_widget.date().toString("yyyy-MM-dd")
            elif isinstance(field_widget, QTextEdit):
                data[field_name] = field_widget.toPlainText()
        return data 