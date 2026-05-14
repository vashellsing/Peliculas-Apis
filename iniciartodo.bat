@echo off
REM ================================
REM Ir a la carpeta raíz del proyecto
REM ================================
cd /d "%~dp0"

REM ================================
REM Definir Python del venv
REM ================================
set PYTHON=%~dp0venv\Scripts\python.exe

REM ================================
REM Verificar que exista el venv
REM ================================
if not exist "%PYTHON%" (
    echo ERROR: No se encuentra el Python del venv
    echo Ruta buscada:
    echo %PYTHON%
    pause
    exit /b
)

echo Usando Python:
echo %PYTHON%
echo.

REM ================================
REM Ir a BackendApis
REM ================================
cd ApisVue\BackendApis

REM ================================
REM Levantar APIs REST
REM ================================
echo Levantando APIs REST...
start "REST Cartelera" cmd /k "%PYTHON% api_rest\app_cartelera.py"
start "REST Peliculas"  cmd /k "%PYTHON% api_rest\app_peliculas.py"
start "REST Resenas"    cmd /k "%PYTHON% api_rest\app_resenas.py"
start "REST Series"    cmd /k "%PYTHON% api_rest\app_series.py"

REM ================================
REM Levantar API SOAP
REM ================================
echo Levantando API SOAP...
start "SOAP Autenticacion" cmd /k "%PYTHON% api_soap\api_autenticacion.py"

pause