@echo off
echo ========================================
echo    FITNESS TRACKER - LAUNCHER
echo ========================================
echo.

:: Verificar si Python esta instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo Python no encontrado.
    echo.
    echo Intentando instalar Python con winget...
    winget install Python.Python.3.11 --accept-package-agreements --accept-source-agreements
    if errorlevel 1 (
        echo.
        echo Error: No se pudo instalar Python con winget.
        echo.
        echo Posibles causas:
        echo - Winget no esta disponible en tu sistema
        echo - Sin permisos de administrador
        echo - Sin conexion a internet
        echo.
        echo Solucion: Instala Python manualmente desde python.org
        echo.
        pause
        exit /b 1
    )
    echo.
    echo Python instalado correctamente!
    echo.
    echo IMPORTANTE: Cierra esta ventana y ejecuta el script nuevamente
    echo para que Python sea reconocido por el sistema.
    echo.
    pause
    exit /b 0
)

echo Python encontrado
python --version

:: Verificar si el entorno virtual existe
if not exist "venv\" (
    echo.
    echo Creando entorno virtual...
    python -m venv venv
    if errorlevel 1 (
        echo  Error al crear el entorno virtual
        pause
        exit /b 1
    )
    echo Entorno virtual creado
) else (
    echo Entorno virtual encontrado
)

:: Activar entorno virtual
echo.
echo Activando entorno virtual...
call venv\Scripts\activate
if errorlevel 1 (
    echo Error al activar el entorno virtual
    pause
    exit /b 1
)

:: Verificar si las dependencias estan instaladas
echo.
echo Verificando dependencias...
python -c "import streamlit, plotly, pandas, requests" >nul 2>&1
if errorlevel 1 (
    echo Instalando dependencias...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Error al instalar dependencias
        pause
        exit /b 1
    )
    echo Dependencias instaladas
) else (
    echo Dependencias ya estan instaladas
)

:: Ejecutar la aplicación
echo.
echo Lanzando Fitness Tracker...
echo.
echo ========================================
echo     La aplicacion se abrira en tu navegador
echo     Si no se abre automaticamente, ve a: http://localhost:8501
echo     Para cerrar: Ctrl+C en esta ventana
echo ========================================
echo.

streamlit run app.py

:: Si llegamos aquí, la aplicación se cerró
echo.
echo 👋 Fitness Tracker se ha cerrado
pause
