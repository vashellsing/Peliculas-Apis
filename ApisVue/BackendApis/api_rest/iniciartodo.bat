@echo off
echo === Iniciando Backend APIs ===

REM Ir a la carpeta donde está este .bat
cd /d "%~dp0"

REM Definir python del venv (un nivel arriba)
set PYTHON="%~dp0..\venv\Scripts\python.exe"

REM Verificar que exista
if not exist %PYTHON% (
    echo ERROR: No se encuentra el Python del venv
    echo Ruta buscada:
    echo %PYTHON%
    pause
    exit /b
)

echo Usando Python:
echo %PYTHON%
echo.

REM Levantar APIs REST
start cmd /k %PYTHON% app_cartelera.py
start cmd /k %PYTHON% app_peliculas.py
start cmd /k %PYTHON% app_resenas.py
start cmd /k %PYTHON% app_series.py