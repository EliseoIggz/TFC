#!/bin/bash

echo "========================================"
echo "   🏃‍♂️ FITNESS TRACKER - LAUNCHER"
echo "========================================"
echo

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ ERROR: Python3 no está instalado"
    echo "Por favor, instala Python 3.8 o superior"
    exit 1
fi

echo "✅ Python encontrado"
python3 --version

# Verificar si el entorno virtual existe
if [ ! -d "venv" ]; then
    echo
    echo "🔧 Creando entorno virtual..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Error al crear el entorno virtual"
        exit 1
    fi
    echo "✅ Entorno virtual creado"
else
    echo "✅ Entorno virtual encontrado"
fi

# Activar entorno virtual
echo
echo "🚀 Activando entorno virtual..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "❌ Error al activar el entorno virtual"
    exit 1
fi

# Verificar si las dependencias están instaladas
echo
echo "🔍 Verificando dependencias..."
python -c "import streamlit, plotly, pandas, requests" &> /dev/null
if [ $? -ne 0 ]; then
    echo "📦 Instalando dependencias..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Error al instalar dependencias"
        exit 1
    fi
    echo "✅ Dependencias instaladas"
else
    echo "✅ Dependencias ya están instaladas"
fi

# Ejecutar la aplicación
echo
echo "🎯 Lanzando Fitness Tracker..."
echo
echo "========================================"
echo "   🌐 La aplicación se abrirá en tu navegador"
echo "   📱 Si no se abre automáticamente, ve a: http://localhost:8501"
echo "   🛑 Para cerrar: Ctrl+C en esta terminal"
echo "========================================"
echo

streamlit run app.py

# Si llegamos aquí, la aplicación se cerró
echo
echo "👋 Fitness Tracker se ha cerrado"
