# src/views/registration_view.py
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QLabel,
    QHBoxLayout,
    QMessageBox,
    QDateEdit,
    QTextEdit,
    QGroupBox,
    QFrame,
    QScrollArea,
    QSplitter,
    QListView,
    QComboBox,
)
from PyQt6.QtCore import QDate, Qt, QSize, QRect, QAbstractListModel, QModelIndex, QTimer
from PyQt6.QtGui import QPainter, QPen, QFont
from PyQt6.QtWidgets import QStyledItemDelegate
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
        
        # Layout raíz con scroll para contenido y footer fijo abajo
        self.outer_layout = QVBoxLayout(self)
        self.outer_layout.setContentsMargins(0, 0, 0, 0)
        self.outer_layout.setSpacing(0)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.page_widget = QWidget()
        self.page_layout = QVBoxLayout(self.page_widget)
        l, t, r, b = Config.UI_PAGE_MARGINS
        self.page_layout.setContentsMargins(l, t, r, 0)
        self.page_layout.setSpacing(Config.UI_PAGE_SPACING)
        self.scroll_area.setWidget(self.page_widget)

        # Construir contenido principal y footer
        self._build_content()
        self.outer_layout.addWidget(self.scroll_area)
        self._create_action_panel()

    def _build_content(self):
        """Construye el contenido dentro del área con scroll.

        Márgenes, espaciados y tamaños provienen de constantes centralizadas en `Config`
        para evitar números mágicos y asegurar consistencia visual.
        """
        self.fields = {}

        # Crear layout de dos columnas con QSplitter (8/4)
        self.main_splitter = self._create_main_layout()
        self.page_layout.addWidget(self.main_splitter)

        # Crear tarjetas en columnas
        self._create_identification_card()
        self._create_reception_card()
        self._create_problem_card()
        self._create_status_card()
        self._create_history_card()

        # Valores por defecto
        self._setup_default_values()

        # Inicializar tamaños del splitter (8/4) tras mostrar
        QTimer.singleShot(0, self._init_splitter_sizes)
        
    def _create_main_layout(self):
        """Crea el layout principal de dos columnas con QSplitter (8/4)."""
        splitter = QSplitter(Qt.Orientation.Horizontal)

        self.left_widget = QWidget()
        self.left_column = QVBoxLayout(self.left_widget)
        self.left_column.setContentsMargins(0, 0, 8, 0)
        self.left_column.setSpacing(Config.UI_FIELD_SPACING)

        self.right_widget = QWidget()
        self.right_column = QVBoxLayout(self.right_widget)
        self.right_column.setContentsMargins(8, 0, 0, 0)
        self.right_column.setSpacing(Config.UI_FIELD_SPACING)

        splitter.addWidget(self.left_widget)
        splitter.addWidget(self.right_widget)
        splitter.setStretchFactor(0, 2)  # ~8/12
        splitter.setStretchFactor(1, 1)  # ~4/12
        return splitter
    
    def _create_identification_card(self):
        """Crea la tarjeta de identificación del equipo."""
        identification_group = QGroupBox("📋 Identificación del Equipo")
        identification_group.setAccessibleName("Tarjeta de identificación del equipo")
        
        # Usar QVBoxLayout para mejor control del espaciado
        card_layout = QVBoxLayout(identification_group)
        card_layout.setContentsMargins(10, 15, 10, 10)  # Márgenes internos
        card_layout.setSpacing(10)  # Espacio entre elementos
        
        # Crear QFormLayout para los campos
        identification_layout = QFormLayout()
        identification_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)  # Alinear etiquetas a la derecha
        identification_layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)
        identification_layout.setSpacing(8)  # Espacio entre filas
        
        # Crear campo combo para Tipo de Equipo (usando Config centralizado)
        self.fields['Tipo de Equipo'] = QComboBox()
        self.fields['Tipo de Equipo'].addItems(Config.EQUIPMENT_TYPES)
        self.fields['Tipo de Equipo'].setCurrentIndex(-1)  # Sin selección inicial
        
        # Crear campos de texto
        self.fields['Marca y Modelo'] = QLineEdit()
        self.fields['Numero de Serie'] = QLineEdit()
        
        # Configurar campos con altura estándar
        self.fields['Tipo de Equipo'].setMinimumHeight(Config.UI_FIELD_HEIGHT)
        self.fields['Marca y Modelo'].setMinimumHeight(Config.UI_FIELD_HEIGHT)
        self.fields['Numero de Serie'].setMinimumHeight(Config.UI_FIELD_HEIGHT)
        
        # Añadir tooltips informativos
        self.fields['Tipo de Equipo'].setToolTip("Seleccione el tipo de equipo del inventario")
        self.fields['Marca y Modelo'].setToolTip("Se completa automáticamente según el tipo")
        self.fields['Numero de Serie'].setToolTip("Número de serie único del equipo")
        
        # Conectar autocompletado de Marca y Modelo
        self.fields['Tipo de Equipo'].currentTextChanged.connect(self._on_tipo_equipo_changed)
        
        # Añadir campos al layout
        identification_layout.addRow(QLabel("Tipo de Equipo:"), self.fields['Tipo de Equipo'])
        identification_layout.addRow(QLabel("Marca y Modelo:"), self.fields['Marca y Modelo'])
        identification_layout.addRow(QLabel("Número de Serie:"), self.fields['Numero de Serie'])
        
        # Añadir el form layout al card layout
        card_layout.addLayout(identification_layout)
        
        # Añadir tarjeta a la columna izquierda
        self.left_column.addWidget(identification_group)
    
    def _create_reception_card(self):
        """Crea la tarjeta de detalles del ingreso."""
        reception_group = QGroupBox("📦 Detalles del Ingreso")
        reception_group.setAccessibleName("Tarjeta de detalles del ingreso")
        
        # Usar QVBoxLayout para mejor control del espaciado
        card_layout = QVBoxLayout(reception_group)
        card_layout.setContentsMargins(10, 15, 10, 10)  # Márgenes internos
        card_layout.setSpacing(10)  # Espacio entre elementos
        
        # Crear QFormLayout para los campos
        reception_layout = QFormLayout()
        reception_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)  # Alinear etiquetas a la derecha
        reception_layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)
        reception_layout.setSpacing(8)  # Espacio entre filas
        
        # Crear campos
        self.fields['Responsable Recepcion'] = QLineEdit()
        self.fields['Fecha de Recepcion'] = QDateEdit()
        self.fields['Componentes Entregados'] = QLineEdit()
        
        # Configurar campos con altura estándar
        self.fields['Responsable Recepcion'].setMinimumHeight(Config.UI_FIELD_HEIGHT)
        self.fields['Fecha de Recepcion'].setMinimumHeight(Config.UI_FIELD_HEIGHT)
        self.fields['Componentes Entregados'].setMinimumHeight(Config.UI_FIELD_HEIGHT)
        
        # Añadir tooltips informativos
        self.fields['Responsable Recepcion'].setToolTip("Nombre del técnico que recibe el equipo")
        self.fields['Fecha de Recepcion'].setToolTip("Fecha en que se recibe el equipo")
        self.fields['Componentes Entregados'].setToolTip("Accesorios recibidos con el equipo")
        
        # Añadir campos al layout
        reception_layout.addRow(QLabel("Responsable Recepción:"), self.fields['Responsable Recepcion'])
        reception_layout.addRow(QLabel("Fecha de Recepción:"), self.fields['Fecha de Recepcion'])

        # Campo de componentes + barra de chips interactivos
        reception_layout.addRow(QLabel("Componentes Entregados:"), self.fields['Componentes Entregados'])

        chips_bar = QWidget()
        chips_layout = QHBoxLayout(chips_bar)
        chips_layout.setContentsMargins(0, 0, 0, 0)
        chips_layout.setSpacing(6)
        self.component_chips = []
        for label in ["Cargador", "Cable AC", "Cable USB", "Maletín", "Mouse"]:
            chip = QPushButton(label)
            chip.setCheckable(True)
            chip.setProperty("variant", "chip")
            chip.clicked.connect(self._on_component_chip_toggled)
            self.component_chips.append(chip)
            chips_layout.addWidget(chip)
        card_layout.addWidget(chips_bar)
        
        # Añadir el form layout al card layout
        card_layout.addLayout(reception_layout)
        
        # Añadir tarjeta a la columna izquierda
        self.left_column.addWidget(reception_group)
    
    def _create_problem_card(self):
        """Crea la tarjeta de descripción del problema."""
        problem_group = QGroupBox("📝 Descripción del Problema")
        problem_group.setAccessibleName("Tarjeta de descripción del problema")
        
        # Usar QVBoxLayout para mejor control del espaciado
        card_layout = QVBoxLayout(problem_group)
        card_layout.setContentsMargins(10, 15, 10, 10)  # Márgenes internos
        card_layout.setSpacing(8)  # Espacio entre elementos
        
        # Crear etiqueta explicativa
        description_label = QLabel("Describa detalladamente el problema reportado por el usuario:")
        description_label.setWordWrap(True)
        
        # Crear campo
        self.fields['Descripcion del Problema'] = QTextEdit()
        self.fields['Descripcion del Problema'].setMinimumHeight(Config.UI_TEXTEDIT_PROBLEM_HEIGHT)
        self.fields['Descripcion del Problema'].setToolTip("Descripción detallada del problema reportado")
        
        # Añadir elementos al layout
        card_layout.addWidget(description_label)
        card_layout.addWidget(self.fields['Descripcion del Problema'])
        
        # Añadir tarjeta a la columna izquierda
        self.left_column.addWidget(problem_group)
        # No añadir stretch para mejor distribución del espacio
    
    def _create_status_card(self):
        """Crea la tarjeta de estado y seguimiento."""
        status_group = QGroupBox("📊 Estado y Seguimiento")
        status_group.setAccessibleName("Tarjeta de estado y seguimiento")
        
        # Usar QVBoxLayout para mejor control del espaciado
        card_layout = QVBoxLayout(status_group)
        card_layout.setContentsMargins(10, 15, 10, 10)  # Márgenes internos
        card_layout.setSpacing(10)  # Espacio entre elementos
        
        # Crear QFormLayout para los campos
        status_layout = QFormLayout()
        status_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)  # Alinear etiquetas a la derecha
        status_layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)
        status_layout.setSpacing(8)  # Espacio entre filas
        
        # Crear campos
        self.fields['Estado'] = QLineEdit()
        self.fields['Fecha de Entrega'] = QDateEdit()
        
        # Configurar campos con altura estándar
        self.fields['Estado'].setMinimumHeight(Config.UI_FIELD_HEIGHT)
        self.fields['Fecha de Entrega'].setMinimumHeight(Config.UI_FIELD_HEIGHT)
        
        # Añadir tooltips informativos
        self.fields['Estado'].setToolTip("Estado actual del equipo")
        self.fields['Fecha de Entrega'].setToolTip("Fecha en que se entrega el equipo reparado")
        
        # Añadir campos al layout
        status_layout.addRow(QLabel("Estado:"), self.fields['Estado'])
        status_layout.addRow(QLabel("Fecha de Entrega:"), self.fields['Fecha de Entrega'])
        
        # Añadir el form layout al card layout
        card_layout.addLayout(status_layout)
        
        # Añadir tarjeta a la columna derecha
        self.right_column.addWidget(status_group)
    
    def _create_history_card(self):
        """Crea la tarjeta de bitácora de intervenciones."""
        history_group = QGroupBox("🛠️ Bitácora de Intervenciones")
        history_group.setAccessibleName("Tarjeta de bitácora de intervenciones")
        
        # Usar QVBoxLayout para mejor control del espaciado
        card_layout = QVBoxLayout(history_group)
        card_layout.setContentsMargins(10, 15, 10, 10)  # Márgenes internos
        card_layout.setSpacing(8)  # Espacio entre elementos
        
        # Crear etiqueta explicativa
        history_label = QLabel("Registre las acciones realizadas en el equipo (formato recomendado: YYYY-MM-DD - Acción):")
        history_label.setWordWrap(True)
        
        # Timeline: QListView con modelo y delegate personalizados
        card_layout.addWidget(history_label)
        self.timeline_view = QListView()
        self.timeline_view.setObjectName("timeline_list")
        self.timeline_view.setUniformItemSizes(False)
        self.timeline_view.setMinimumHeight(260)
        self.timeline_view.setMaximumHeight(360)
        self.timeline_model = LogItemModel([])
        self.timeline_view.setModel(self.timeline_model)
        self.timeline_delegate = TimelineDelegate(self.timeline_view)
        self.timeline_view.setItemDelegate(self.timeline_delegate)
        self._seed_demo_timeline()
        card_layout.addWidget(self.timeline_view)

        # Añadir tarjeta a la columna derecha
        self.right_column.addWidget(history_group)
    
    def _setup_default_values(self):
        """Configura los valores por defecto de los campos."""
        self.fields['Fecha de Recepcion'].setDate(QDate.currentDate())
        self.fields['Estado'].setText(Config.DEFAULT_ESTADO)
        self.fields['Estado'].setReadOnly(True)

    def _create_action_panel(self):
        """Crea el panel de acciones (footer) con altura coherente.

        La altura final resulta de: botón (Config.UI_BUTTON_MIN_H) +
        padding vertical superior/inferior (Config.UI_FOOTER_PADDING_V),
        y se asegura con Config.UI_ACTION_PANEL_HEIGHT.
        """
        action_panel = QFrame()
        action_panel.setObjectName("action_panel")
        action_panel.setFrameShape(QFrame.Shape.StyledPanel)
        action_panel.setFrameShadow(QFrame.Shadow.Raised)
        action_panel.setMinimumHeight(Config.UI_ACTION_PANEL_HEIGHT)
        action_panel.setContentsMargins(0, 0, 0, 0)  # Eliminar márgenes extra
        
        button_layout = QHBoxLayout(action_panel)
        button_layout.setContentsMargins(
            Config.UI_FOOTER_PADDING_H,
            Config.UI_FOOTER_PADDING_V,
            Config.UI_FOOTER_PADDING_H,
            Config.UI_FOOTER_PADDING_V,
        )
        button_layout.setSpacing(Config.UI_PAGE_SPACING)
        button_layout.addStretch()

        self.btn_limpiar = QPushButton(Config.MSG_BTN_LIMPIAR)
        self.btn_limpiar.setObjectName("secondary_button")
        self.btn_limpiar.setMinimumWidth(Config.UI_BUTTON_MIN_WIDTH)
        self.btn_limpiar.setMinimumHeight(Config.UI_BUTTON_MIN_H)
        self.btn_limpiar.setToolTip("Limpia todos los campos del formulario")
        self.btn_limpiar.clicked.connect(self.clear_form)
        button_layout.addWidget(self.btn_limpiar)
        
        self.btn_guardar = QPushButton(Config.MSG_BTN_GUARDAR)
        self.btn_guardar.setObjectName("primary_button")
        self.btn_guardar.setMinimumWidth(Config.UI_BUTTON_MIN_WIDTH)
        self.btn_guardar.setMinimumHeight(Config.UI_BUTTON_MIN_H)
        self.btn_guardar.setToolTip("Guarda el registro en la base de datos")
        self.btn_guardar.clicked.connect(self.save_record)
        button_layout.addWidget(self.btn_guardar)
        
        # Añadir el panel como footer fijo (fuera del scroll)
        self.outer_layout.addWidget(action_panel)
        self.outer_layout.addSpacing(10)

    def _on_component_chip_toggled(self):
        """Sincroniza el campo de componentes con los chips seleccionados."""
        selected = [c.text() for c in getattr(self, 'component_chips', []) if c.isChecked()]
        free_text = self.fields.get('Componentes Entregados').text()
        parts = []
        if free_text:
            parts.append(free_text)
        if selected:
            parts.append(", ".join(selected))
        self.fields['Componentes Entregados'].setText(", ".join(parts))

    def _seed_demo_timeline(self):
        """Establece timeline vacío para nuevo registro."""
        # En nuevo registro, la bitácora inicia vacía
        self.timeline_model.setItems([])

    def _init_splitter_sizes(self):
        """Establece tamaños iniciales del splitter ~8/4 sin fijarlos."""
        total = max(1, self.width())
        # Nota: el atributo es main_splitter
        self.main_splitter.setSizes([int(total * 0.66), int(total * 0.34)])
        self.main_splitter.setChildrenCollapsible(False)

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
        
        self.fields['Estado'].setText(Config.DEFAULT_ESTADO)
        self.fields['Fecha de Recepcion'].setDate(QDate.currentDate())
        # Limpiar chips seleccionados y timeline (vacío para nuevo registro)
        for chip in getattr(self, 'component_chips', []):
            chip.setChecked(False)
        self._seed_demo_timeline()


    def save_record(self):
        """Valida y guarda los datos del formulario utilizando el DataManager."""
        data = self.get_form_data()
        
        # Validación completa usando la lista de Config
        for required_field in Config.REQUIRED_FIELDS:
            if not data.get(required_field, '').strip():
                QMessageBox.warning(self.window(), Config.MSG_TITULO_CAMPOS_REQUERIDOS, 
                                   Config.MSG_CAMPO_REQUERIDO.format(field_name=required_field))
                return

        # Usar el método correcto del data_manager y manejar el resultado
        if self.data_manager.add_record(data):
            serial_number = data.get('Numero de Serie', '')
            QMessageBox.information(self.window(), Config.MSG_TITULO_EXITO, 
                                   Config.MSG_EXITO_REGISTRO.format(serial_number=serial_number))
            self.clear_form()
        else:
            QMessageBox.critical(self.window(), Config.MSG_TITULO_ERROR_GUARDADO, Config.MSG_ERROR_GUARDADO)
    
    def _on_tipo_equipo_changed(self, tipo_selected: str):
        """Autocompletado de Marca y Modelo basado en Tipo de Equipo."""
        if tipo_selected in Config.EQUIPMENT_BRAND_MODEL_MAPPING:
            self.fields['Marca y Modelo'].setText(Config.EQUIPMENT_BRAND_MODEL_MAPPING[tipo_selected])
        else:
            self.fields['Marca y Modelo'].clear()
    
    def get_form_data(self) -> dict:
        """Recopila los datos de todos los widgets del formulario en un diccionario."""
        data = {}
        for field_name, field_widget in self.fields.items():
            if isinstance(field_widget, QLineEdit):
                data[field_name] = field_widget.text()
            elif isinstance(field_widget, QComboBox):
                data[field_name] = field_widget.currentText()
            elif isinstance(field_widget, QDateEdit):
                data[field_name] = field_widget.date().toString(Config.FORMATO_FECHA)
            elif isinstance(field_widget, QTextEdit):
                data[field_name] = field_widget.toPlainText()
        return data 


class LogItemModel(QAbstractListModel):
    """Modelo simple para items de bitácora en timeline."""

    def __init__(self, items: list[dict] | None = None):
        super().__init__()
        self._items: list[dict] = items or []

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self._items)

    def data(self, index: QModelIndex, role: int):
        if not index.isValid():
            return None
        if role == Qt.ItemDataRole.DisplayRole:
            return self._items[index.row()]
        return None

    def setItems(self, items: list[dict]) -> None:
        self.beginResetModel()
        self._items = items
        self.endResetModel()


class TimelineDelegate(QStyledItemDelegate):
    """Delegate para pintar items del timeline con avatar, fecha y acción.

    Colores y dimensiones provienen de `Config` para evitar hardcoding.
    """

    AVATAR_RADIUS = Config.UI_TIMELINE_AVATAR_RADIUS
    AVATAR_DIAM = AVATAR_RADIUS * 2
    LINE_WIDTH = Config.UI_TIMELINE_LINE_WIDTH

    def paint(self, painter: QPainter, option, index: QModelIndex) -> None:
        data = index.data(Qt.ItemDataRole.DisplayRole) or {}
        rect: QRect = option.rect

        painter.save()

        # Zona izquierda: avatar + línea vertical
        center_x = rect.left() + 20
        center_y = rect.top() + 18

        from src.config import qcolor
        pen = QPen(qcolor(Config.COLOR_CFE_BORDER), self.LINE_WIDTH)
        painter.setPen(pen)
        # Línea vertical continua a lo largo del item
        painter.drawLine(center_x, rect.top(), center_x, rect.bottom())

        # Avatar circular en CFE green
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(qcolor(Config.COLOR_CFE_GREEN))
        painter.drawEllipse(center_x - self.AVATAR_RADIUS, center_y - self.AVATAR_RADIUS, self.AVATAR_DIAM, self.AVATAR_DIAM)

        # Texto: fecha y acción
        painter.setPen(qcolor(Config.COLOR_GRAY_TEXT))
        date_text = str(data.get("fecha", ""))
        painter.setFont(QFont(painter.font().family(), painter.font().pointSize()))
        painter.drawText(rect.left() + 44, rect.top() + 16, date_text)

        painter.setPen(qcolor(Config.COLOR_CFE_BLACK))
        painter.setFont(QFont(painter.font().family(), painter.font().pointSize() + 1))
        action_text = str(data.get("accion", ""))
        painter.drawText(rect.left() + 44, rect.top() + 36, action_text)

        painter.restore()

    def sizeHint(self, option, index: QModelIndex) -> QSize:
        return QSize(option.rect.width(), 56)