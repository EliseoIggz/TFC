@echo off
echo ========================================
echo    TEST SIMPLE - FITNESS TRACKER
echo ========================================
echo.

echo 1. Verificando directorio actual...
echo Directorio: %CD%
echo.

echo 2. Verificando archivos...
if exist "requirements.txt" (
    echo ✅ requirements.txt encontrado
) else (
    echo ❌ requirements.txt NO encontrado
)

if exist "app.py" (
    echo ✅ app.py encontrado
) else (
    echo ❌ app.py NO encontrado
)

if exist "venv\" (
    echo ✅ venv encontrado
) else (
    echo ❌ venv NO encontrado
)
echo.

echo 3. Verificando Python...
python --version
if errorlevel 1 (
    echo ❌ Python NO encontrado
    pause
    exit /b 1
) else (
    echo ✅ Python encontrado
)
echo.

echo 4. Verificando entorno virtual...
if exist "venv\Scripts\activate" (
    echo ✅ activate encontrado
    echo Activando entorno virtual...
    call venv\Scripts\activate
    if errorlevel 1 (
        echo ❌ Error al activar entorno virtual
        pause
        exit /b 1
    ) else (
        echo ✅ Entorno virtual activado
    )
) else (
    echo ❌ activate NO encontrado
    pause
    exit /b 1
)
echo.

echo 5. Verificando dependencias...
python -c "import streamlit"
if errorlevel 1 (
    echo ❌ streamlit NO instalado
    echo Intentando instalar...
    pip install streamlit
    if errorlevel 1 (
        echo ❌ Error al instalar streamlit
        pause
        exit /b 1
    )
) else (
    echo ✅ streamlit instalado
)
echo.

echo 6. Todo OK - Lanzando app...
echo ========================================
streamlit run app.py

echo.
echo Test completado.
pause
