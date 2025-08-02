@echo off
title Lanzador de RETI-C

echo ===========================================
echo   Lanzador de Aplicacion RETI-C (CFE)
echo ===========================================
echo.

REM --- Activa el entorno virtual de Python ---
echo Activando entorno virtual...
call ".\venv\Scripts\activate.bat"

REM --- Verifica que el entorno se activo y ejecuta la aplicacion ---
if exist ".\venv\Scripts\python.exe" (
    echo Entorno activado. Iniciando aplicacion...
    python run.py
) else (
    echo ERROR: No se pudo encontrar el entorno virtual.
    echo Asegurate de haber ejecutado 'python -m venv venv' en la raiz del proyecto.
)

echo.
echo La aplicacion se ha cerrado. Puedes cerrar esta ventana.
pause 