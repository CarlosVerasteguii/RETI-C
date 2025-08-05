# tests/test_data_manager.py
import pytest
import os
import pandas as pd
from src.data_manager import DataManager
from src.config import Config

# --- Fixtures de Pytest ---

@pytest.fixture
def temp_excel_path(tmp_path):
    """Crea una ruta de archivo temporal para un Excel de prueba."""
    return tmp_path / "test_inventario.xlsx"

@pytest.fixture
def data_manager_con_ruta_temporal(temp_excel_path, monkeypatch):
    """Crea una instancia de DataManager que usa la ruta de archivo temporal."""
    # Actualizado para el sistema auto-fallback: forzar modo red con ruta temporal
    monkeypatch.setattr(Config, 'EXCEL_NETWORK_PATH', temp_excel_path)
    monkeypatch.setattr(Config, 'EXCEL_LOCAL_PATH', temp_excel_path)
    # Simular que siempre hay acceso de red para las pruebas existentes
    monkeypatch.setattr('os.access', lambda path, mode: True)
    
    dm = DataManager()
    return dm

# --- Tests ---

def test_inicializacion_crea_excel_si_no_existe(data_manager_con_ruta_temporal):
    """
    Verifica que al inicializar DataManager, se crea un archivo Excel
    con las columnas correctas.
    """
    # ARRANGE
    dm = data_manager_con_ruta_temporal
    # Actualizado: Usar active_path en lugar de excel_path
    excel_path = dm.active_path

    # ACT (La acción ocurrió en la fixture al crear la instancia)
    
    # ASSERT
    assert os.path.exists(excel_path), "El archivo Excel no fue creado."
    
    df = pd.read_excel(excel_path)
    # CORRECCIÓN: Usar Config.COLUMNS en lugar de Config.EXCEL_COLUMNS
    assert list(df.columns) == Config.COLUMNS, "Las columnas del Excel no coinciden con la configuración."
    assert df.empty, "El Excel recién creado debería tener cero filas."


def test_add_record_funciona_correctamente(data_manager_con_ruta_temporal):
    """
    Verifica que el método add_record añade registros y asigna IDs
    autoincrementales correctamente.
    """
    # ARRANGE
    dm = data_manager_con_ruta_temporal
    # Actualizado: Usar active_path en lugar de excel_path
    excel_path = dm.active_path

    # Datos completos para el primer registro
    nuevo_registro_1 = {
        'Tipo de Equipo': 'Laptop', 
        'Marca y Modelo': 'Dell XPS 15',
        'Numero de Serie': 'TEST-SN-001', 
        'Fecha de Recepcion': '2025-08-04',
        'Descripcion del Problema': 'Pantalla azul.', 
        'Responsable Recepcion': 'Carlos V.',
        'Estado': 'Recibido'
    }

    # ACT 1
    # CORRECCIÓN: Usar add_record en lugar de anadir_registro
    dm.add_record(nuevo_registro_1)

    # ASSERT 1
    df1 = pd.read_excel(excel_path)
    assert len(df1) == 1, "No se añadió la primera fila al DataFrame."
    
    # CORRECCIÓN: Sintaxis correcta para acceder a la primera fila (índice 0)
    registro_guardado_1 = df1.iloc[0]
    assert registro_guardado_1['ID'] == 1, "El primer ID no fue asignado correctamente."
    assert registro_guardado_1['Numero de Serie'] == 'TEST-SN-001'

    # ARRANGE 2: Datos completos para el segundo registro
    nuevo_registro_2 = {
        'Tipo de Equipo': 'Impresora', 
        'Marca y Modelo': 'HP LaserJet',
        'Numero de Serie': 'TEST-SN-002', 
        'Fecha de Recepcion': '2025-08-04',
        'Descripcion del Problema': 'No imprime.', 
        'Responsable Recepcion': 'Carlos V.',
        'Estado': 'Recibido'
    }

    # ACT 2
    # CORRECCIÓN: Usar add_record en lugar de anadir_registro
    dm.add_record(nuevo_registro_2)

    # ASSERT 2
    df2 = pd.read_excel(excel_path)
    assert len(df2) == 2, "La segunda fila no fue añadida."
    
    # CORRECCIÓN: Sintaxis correcta para acceder a la segunda fila (índice 1)
    registro_guardado_2 = df2.iloc[1]
    assert registro_guardado_2['ID'] == 2, "El ID autoincremental no funcionó."


def test_find_by_serial_devuelve_registro_correcto(data_manager_con_ruta_temporal):
    """
    Verifica que el método find_by_serial encuentra y devuelve
    el registro correcto como un diccionario.
    """
    # ARRANGE
    dm = data_manager_con_ruta_temporal
    
    # Datos completos según SRS
    registro_1 = {
        'Tipo de Equipo': 'Laptop',
        'Marca y Modelo': 'Dell XPS 15',
        'Numero de Serie': 'SN-EXIST-001',
        'Fecha de Recepcion': '2025-08-04',
        'Descripcion del Problema': 'Pantalla azul.',
        'Responsable Recepcion': 'Carlos V.',
        'Estado': 'Recibido'
    }
    
    registro_2 = {
        'Tipo de Equipo': 'Monitor',
        'Marca y Modelo': 'Samsung 24"',
        'Numero de Serie': 'SN-EXIST-002',
        'Fecha de Recepcion': '2025-08-04',
        'Descripcion del Problema': 'No enciende.',
        'Responsable Recepcion': 'Carlos V.',
        'Estado': 'En Reparacion'
    }
    
    dm.add_record(registro_1)
    dm.add_record(registro_2)

    # ACT
    resultado_encontrado = dm.find_by_serial('SN-EXIST-002')
    resultado_no_encontrado = dm.find_by_serial('SN-NON-EXIST-999')

    # ASSERT
    assert resultado_encontrado is not None, "No se encontró un registro que debería existir."
    assert isinstance(resultado_encontrado, dict), "El resultado devuelto no es un diccionario."
    assert resultado_encontrado['Tipo de Equipo'] == 'Monitor', "Se encontró el registro incorrecto."
    assert resultado_encontrado['Estado'] == 'En Reparacion', "El estado no coincide."
    
    assert resultado_no_encontrado is None, "Se devolvió un registro cuando no debería haberse encontrado nada."


def test_find_by_serial_validaciones_entrada(data_manager_con_ruta_temporal):
    """
    Verifica que el método find_by_serial maneja correctamente las validaciones de entrada
    y lanza ValueError para entradas inválidas.
    """
    # ARRANGE
    dm = data_manager_con_ruta_temporal
    
    # Añadir un registro de prueba
    registro_test = {
        'Tipo de Equipo': 'Laptop',
        'Marca y Modelo': 'Dell XPS 15',
        'Numero de Serie': 'SN-VALID-001',
        'Fecha de Recepcion': '2025-08-04',
        'Descripcion del Problema': 'Pantalla azul.',
        'Responsable Recepcion': 'Carlos V.',
        'Estado': 'Recibido'
    }
    dm.add_record(registro_test)

    # ACT & ASSERT - Casos que deben lanzar ValueError
    with pytest.raises(ValueError, match="El número de serie no puede ser nulo o estar vacío"):
        dm.find_by_serial("")  # String vacío
        
    with pytest.raises(ValueError, match="El número de serie no puede ser nulo o estar vacío"):
        dm.find_by_serial("   ")  # Solo espacios
        
    with pytest.raises(ValueError, match="El número de serie no puede ser nulo o estar vacío"):
        dm.find_by_serial(None)  # None
    
    # ACT & ASSERT - Casos que deben funcionar correctamente
    # Búsqueda exitosa con espacios extra
    resultado_con_espacios = dm.find_by_serial("  SN-VALID-001  ")
    assert resultado_con_espacios is not None, "No se encontró registro con espacios extra"
    assert resultado_con_espacios['Numero de Serie'] == 'SN-VALID-001', "No se normalizó correctamente la búsqueda"
    
    # Búsqueda sin resultados (debe devolver None, no lanzar error)
    resultado_inexistente = dm.find_by_serial("SN-INEXISTENTE")
    assert resultado_inexistente is None, "Debería devolver None para registros inexistentes"