# Fitness Tracker - Verificación de Dependencias
# =============================================
# Este archivo verifica e instala las dependencias necesarias

import subprocess
import sys
import importlib
import os

def check_dependencies():
    """Verificar e instalar dependencias faltantes"""
    print("🔍 Verificando dependencias...")
    
    # Lista de dependencias requeridas
    required_packages = [
        'streamlit',
        'plotly', 
        'pandas',
        'requests'
    ]
    
    missing_packages = []
    
    # Verificar qué paquetes están instalados
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package} - Instalado")
        except ImportError:
            print(f"❌ {package} - No instalado")
            missing_packages.append(package)
    
    # Instalar paquetes faltantes
    if missing_packages:
        print(f"\n📦 Instalando {len(missing_packages)} paquetes faltantes...")
        
        try:
            for package in missing_packages:
                print(f"Instalando {package}...")
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", package
                ])
                print(f"✅ {package} instalado correctamente")
            
            print("\n🎉 Todas las dependencias han sido instaladas!")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"\n❌ Error al instalar dependencias: {e}")
            print("Por favor, instala manualmente con: pip install -r requirements.txt")
            return False
    else:
        print("\n🎉 Todas las dependencias están instaladas!")
        return True

def install_from_requirements():
    """Instalar dependencias desde requirements.txt"""
    requirements_file = "requirements.txt"
    
    if not os.path.exists(requirements_file):
        print(f"❌ No se encontró {requirements_file}")
        return False
    
    try:
        print("📦 Instalando dependencias desde requirements.txt...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", requirements_file
        ])
        print("✅ Dependencias instaladas correctamente")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al instalar dependencias: {e}")
        return False

if __name__ == "__main__":
    # Si se ejecuta directamente, verificar dependencias
    check_dependencies()
