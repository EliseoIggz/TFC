@echo off
echo ========================================
echo       LIMEN - LAUNCHER
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
    echo Refrescando variables de entorno...
    
    :: Intentar usar refreshenv si está disponible (Chocolatey)
    call refreshenv 2>nul
    if errorlevel 1 (
        echo Refrescando PATH manualmente...
        :: Añadir Python al PATH de la sesión actual
        set "PATH=%PATH%;%LOCALAPPDATA%\Programs\Python\Python311\;%LOCALAPPDATA%\Programs\Python\Python311\Scripts\"
        set "PATH=%PATH%;%PROGRAMFILES%\Python311\;%PROGRAMFILES%\Python311\Scripts\"
        set "PATH=%PATH%;%USERPROFILE%\AppData\Local\Programs\Python\Python311\;%USERPROFILE%\AppData\Local\Programs\Python\Python311\Scripts\"
        
        echo PATH actualizado para esta sesión
    ) else (
        echo Variables de entorno refrescadas con refreshenv
    )
    
    echo.
    echo Verificando que Python sea accesible...
    python --version >nul 2>&1
    if errorlevel 1 (
        echo.
        echo ⚠️  Python aún no es accesible en esta sesión
        echo Cierra esta ventana y ejecuta el script nuevamente
        echo para que Python sea reconocido completamente.
        echo.
        pause
        exit /b 0
    ) else (
        echo ✅ Python es accesible y puede continuar
    )
)

echo Python encontrado
python --version

:: Verificar si el entorno virtual existe
if exist "venv\" (
    echo Entorno virtual encontrado
    echo Verificando si esta corrupto...
    
    :: Verificar si el entorno virtual funciona correctamente
    call venv\Scripts\activate >nul 2>&1
    if errorlevel 1 (
        echo El entorno virtual parece estar corrupto.
        echo Eliminando y recreando...
        rmdir /s /q "venv" 2>nul
        if exist "venv\" (
            echo Error: No se pudo eliminar el directorio venv
            echo Por favor, elimina manualmente la carpeta 'venv' y ejecuta el script nuevamente
            pause
            exit /b 1
        )
        goto :create_venv
    )
) else (
    :create_venv
    echo.
    echo Creando entorno virtual...
    python -m venv venv
    if errorlevel 1 (
        echo Error al crear el entorno virtual
        echo.
        echo Posibles soluciones:
        echo 1. Ejecuta este script como administrador
        echo 2. Verifica que no haya otros procesos usando Python
        echo 3. Elimina manualmente la carpeta 'venv' si existe
        echo.
        pause
        exit /b 1
    )
    echo Entorno virtual creado correctamente
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
echo Lanzando Limen...
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
echo 👋 Limen se ha cerrado
pause
