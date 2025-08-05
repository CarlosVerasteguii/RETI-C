# tests/test_auto_fallback.py
import pytest
import os
from unittest.mock import patch
from src.data_manager import DataManager
from src.config import Config

# --- Fixtures de Pytest ---

@pytest.fixture
def temp_excel_path(tmp_path):
    """Crea una ruta de archivo temporal para un Excel de prueba."""
    return tmp_path / "test_inventario.xlsx"

# --- Tests del Sistema Auto-Fallback ---

@patch('pathlib.Path.exists', return_value=True)
@patch('os.access', return_value=True)
def test_network_connection_success(mock_os_access, mock_path_exists, temp_excel_path, monkeypatch):
    """Prueba que el DataManager usa la ruta de red cuando la conexión es exitosa."""
    # ARRANGE
    monkeypatch.setattr(Config, 'EXCEL_NETWORK_PATH', temp_excel_path)
    
    # ACT
    dm = DataManager()
    
    # ASSERT
    assert dm.is_network_mode is True, "DataManager debería estar en modo red cuando la conexión es exitosa"
    assert dm.active_path == temp_excel_path, "DataManager debería usar la ruta de red"
    assert dm.connection_error is None, "No debería haber error de conexión"

@patch('pathlib.Path.exists', return_value=False)
@patch('os.access', return_value=False)
def test_network_connection_failure_fallbacks_to_local(mock_os_access, mock_path_exists, temp_excel_path, monkeypatch):
    """Prueba que el DataManager hace fallback a la ruta local cuando la conexión falla."""
    # ARRANGE
    monkeypatch.setattr(Config, 'EXCEL_LOCAL_PATH', temp_excel_path)
    
    # ACT
    dm = DataManager()
    
    # ASSERT
    assert dm.is_network_mode is False, "DataManager debería estar en modo local cuando la conexión falla"
    assert dm.active_path == temp_excel_path, "DataManager debería usar la ruta local"
    assert dm.connection_error is not None, "Debería haber un error de conexión registrado"

@patch('pathlib.Path.exists', return_value=True)
@patch('os.access', return_value=False)  # Sin permisos de escritura
def test_network_no_write_permissions_fallbacks_to_local(mock_os_access, mock_path_exists, temp_excel_path, monkeypatch):
    """Prueba que el DataManager hace fallback cuando no hay permisos de escritura en la red."""
    # ARRANGE
    monkeypatch.setattr(Config, 'EXCEL_LOCAL_PATH', temp_excel_path)
    
    # ACT
    dm = DataManager()
    
    # ASSERT
    assert dm.is_network_mode is False, "DataManager debería hacer fallback sin permisos de escritura"
    assert dm.active_path == temp_excel_path, "DataManager debería usar la ruta local"
    assert "permisos de escritura" in dm.connection_error.lower(), "El error debería mencionar permisos de escritura"

def test_fallback_creates_excel_file_in_local_path(temp_excel_path, monkeypatch):
    """Prueba que el fallback crea correctamente el archivo Excel en la ruta local."""
    # ARRANGE
    monkeypatch.setattr(Config, 'EXCEL_LOCAL_PATH', temp_excel_path)
    
    # Simular fallo de red
    with patch('pathlib.Path.exists', return_value=False):
        with patch('os.access', return_value=False):
            # ACT
            dm = DataManager()
    
    # ASSERT
    assert dm.active_path.exists(), "El archivo Excel debería haberse creado en la ruta local"
    assert dm.is_network_mode is False, "Debería estar en modo local"
    
    # Verificar que el archivo tiene la estructura correcta
    import pandas as pd
    df = pd.read_excel(dm.active_path)
    assert list(df.columns) == Config.COLUMNS, "Las columnas del Excel deberían coincidir con la configuración"
    assert df.empty, "El Excel recién creado debería estar vacío"