@echo off
echo 🧪 ACTIVANDO TESTS DE LIMEN FITNESS TRACKER
echo ============================================

REM Verificar si existe el entorno virtual
if not exist "venv\Scripts\activate.bat" (
    echo 🔄 No se encontró el entorno virtual, creándolo...
    echo 💡 Creando entorno virtual...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ ERROR: No se pudo crear el entorno virtual
        echo 💡 Verifica que Python esté instalado y en el PATH
        pause
        exit /b 1
    )
    echo ✅ Entorno virtual creado exitosamente
)

REM Activar entorno virtual
echo 🔄 Activando entorno virtual...
call venv\Scripts\activate.bat

REM Verificar dependencias
echo 🔍 Verificando dependencias...
python -c "import requests, openai" 2>nul
if errorlevel 1 (
    echo ❌ ERROR: Faltan dependencias
    echo 💡 Instalando dependencias...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ ERROR: No se pudieron instalar las dependencias
        pause
        exit /b 1
    )
)

echo ✅ Entorno virtual activado
echo ✅ Dependencias verificadas
echo.

echo 🚀 EJECUTANDO TESTS...
echo ======================

REM Ejecutar tests uno por uno
echo.
echo 🔤 TEST 1: Servicio de Traducción
python tests/test_translation_service.py

echo.
echo 🏃‍♂️ TEST 2: Base de Datos de Deportes
python tests/test_sports_database.py

echo.
echo 🔍 TEST 3: Búsqueda USDA
python tests/test_usda_search.py

echo.
echo 🎯 TODOS LOS TESTS COMPLETADOS
echo 💡 Revisa los resultados arriba
echo.
pause
