@echo off
echo ========================================
echo    🏃‍♂️ FITNESS TRACKER - LAUNCHER
echo ========================================
echo.

:: Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python no está instalado o no está en el PATH
    echo Por favor, instala Python 3.8 o superior
    pause
    exit /b 1
)

echo ✅ Python encontrado
python --version

:: Verificar si el entorno virtual existe
if not exist "venv\" (
    echo.
    echo 🔧 Creando entorno virtual...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Error al crear el entorno virtual
        pause
        exit /b 1
    )
    echo ✅ Entorno virtual creado
) else (
    echo ✅ Entorno virtual encontrado
)

:: Activar entorno virtual
echo.
echo 🚀 Activando entorno virtual...
call venv\Scripts\activate
if errorlevel 1 (
    echo ❌ Error al activar el entorno virtual
    pause
    exit /b 1
)

:: Verificar si las dependencias están instaladas
echo.
echo 🔍 Verificando dependencias...
python -c "import streamlit, plotly, pandas, requests" >nul 2>&1
if errorlevel 1 (
    echo 📦 Instalando dependencias...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Error al instalar dependencias
        pause
        exit /b 1
    )
    echo ✅ Dependencias instaladas
) else (
    echo ✅ Dependencias ya están instaladas
)

:: Ejecutar la aplicación
echo.
echo 🎯 Lanzando Fitness Tracker...
echo.
echo ========================================
echo    🌐 La aplicación se abrirá en tu navegador
echo    📱 Si no se abre automáticamente, ve a: http://localhost:8501
echo    🛑 Para cerrar: Ctrl+C en esta ventana
echo ========================================
echo.

streamlit run app.py

:: Si llegamos aquí, la aplicación se cerró
echo.
echo 👋 Fitness Tracker se ha cerrado
pause
