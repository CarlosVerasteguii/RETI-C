"""
Tests de integración para RETI-C.
Verifica flujos completos de la aplicación.

Author: Carlos Verastegui
Version: 1.0
Date: 05/08/2025
"""

import pytest
import os
import tempfile
import pandas as pd
from pathlib import Path
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication
from PyQt6.QtTest import QTest

from src.main_app import MainApp
from src.data_manager import DataManager
from src.config import Config


@pytest.fixture
def app(qtbot):
    """Fixture que crea una instancia de QApplication."""
    return QApplication.instance()


@pytest.fixture
def temp_excel_path():
    """Crea una ruta de archivo temporal para un Excel de prueba."""
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
        yield tmp.name
    # Limpiar después de la prueba
    if os.path.exists(tmp.name):
        os.unlink(tmp.name)


@pytest.fixture
def main_app_with_data(qtbot, monkeypatch, temp_excel_path):
    """
    Crea una instancia de MainApp con datos de prueba.
    """
    # Configurar ruta temporal para Excel (sistema auto-fallback)
    monkeypatch.setattr(Config, 'EXCEL_NETWORK_PATH', Path(temp_excel_path))
    monkeypatch.setattr(Config, 'EXCEL_LOCAL_PATH', Path(temp_excel_path))
    # Simular que siempre hay acceso de red para las pruebas de integración
    monkeypatch.setattr('os.access', lambda path, mode: True)
    
    # Crear DataManager y añadir datos de prueba
    dm = DataManager()
    
    # Datos de prueba
    test_records = [
        {
            'Tipo de Equipo': 'Laptop',
            'Marca y Modelo': 'Dell XPS 15',
            'Numero de Serie': 'TEST-SN-001',
            'Fecha de Recepcion': '2025-08-04',
            'Descripcion del Problema': 'Pantalla azul.',
            'Responsable Recepcion': 'Carlos V.',
            'Estado': 'Recibido'
        },
        {
            'Tipo de Equipo': 'Monitor',
            'Marca y Modelo': 'Samsung 24"',
            'Numero de Serie': 'TEST-SN-002',
            'Fecha de Recepcion': '2025-08-04',
            'Descripcion del Problema': 'No enciende.',
            'Responsable Recepcion': 'Carlos V.',
            'Estado': 'En Reparacion'
        }
    ]
    
    for record in test_records:
        dm.add_record(record)
    
    # Crear MainApp
    main_app = MainApp()
    
    # Reemplazar DataManager con nuestra instancia con datos
    main_app.data_manager = dm
    
    # Asegurar que las vistas usen el DataManager correcto
    if hasattr(main_app, 'registration_page'):
        main_app.registration_page.data_manager = dm
    if hasattr(main_app, 'search_page'):
        main_app.search_page.data_manager = dm
    
    # Mostrar la aplicación (necesario para que los widgets estén listos)
    main_app.show()
    
    return main_app


def test_navegacion_a_search_view(main_app_with_data, qtbot):
    """
    Verifica que la navegación a la vista de búsqueda funciona correctamente.
    """
    # Verificar que inicialmente estamos en la vista Dashboard (índice 0)
    assert main_app_with_data.stacked_widget.currentIndex() == 0
    
    # Simular clic en el botón de búsqueda usando el método directo
    main_app_with_data.btn_busqueda.click()
    
    # Verificar que ahora estamos en la vista de búsqueda (índice 2)
    assert main_app_with_data.stacked_widget.currentIndex() == 2
    
    # Verificar que el botón de búsqueda está marcado como activo
    assert main_app_with_data.btn_busqueda.isChecked()
    assert not main_app_with_data.btn_dashboard.isChecked()
    assert not main_app_with_data.btn_registro.isChecked()


def test_busqueda_por_serial_exitosa(main_app_with_data, qtbot):
    """
    Verifica que la búsqueda por número de serie funciona correctamente.
    """
    # Navegar a la vista de búsqueda
    main_app_with_data.btn_busqueda.click()
    
    # Acceder a la vista de búsqueda
    search_view = main_app_with_data.search_page
    
    # Verificar que la vista existe
    assert search_view is not None
    
    # Ingresar número de serie en el campo
    search_view.serial_input.setText("TEST-SN-002")
    
    # Hacer clic en el botón de búsqueda
    search_view.search_button.click()
    
    # Verificar que se muestra el resultado correcto
    results_text = search_view.results_text.toPlainText()
    assert "Monitor" in results_text
    assert "Samsung 24\"" in results_text
    assert "En Reparacion" in results_text


def test_busqueda_por_serial_no_encontrado(main_app_with_data, qtbot):
    """
    Verifica que se muestra un mensaje apropiado cuando no se encuentra el número de serie.
    """
    # Navegar a la vista de búsqueda
    main_app_with_data.btn_busqueda.click()
    
    # Acceder a la vista de búsqueda
    search_view = main_app_with_data.search_page
    
    # Verificar que la vista existe
    assert search_view is not None
    
    # Ingresar número de serie inexistente
    search_view.serial_input.setText("SERIAL-INEXISTENTE")
    
    # Hacer clic en el botón de búsqueda
    search_view.search_button.click()
    
    # Verificar que se muestra mensaje de no encontrado
    results_text = search_view.results_text.toPlainText()
    assert "No se encontró" in results_text