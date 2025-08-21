# Limen - Aplicación Principal
# =====================================
# Este es el punto de entrada de la aplicación

import sys
import os

# Añadir el directorio actual al path para importaciones
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.check_dependencies import check_dependencies
from views.dashboard_view import DashboardView
import config

def main():
    """Función principal de la aplicación"""
    print("🏃‍♂️ Limen - Iniciando...")
    print(f"Versión: {config.APP_VERSION}")
    print(f"Autor: {config.APP_AUTHOR}")
    print("=" * 50)
    
    # Verificar dependencias
    print("\n🔍 Verificando dependencias...")
    if not check_dependencies():
        print("❌ Error al verificar dependencias")
        print("Por favor, ejecuta: pip install -r requirements.txt")
        return False
    
    # Inicializar base de datos
    print("\n🗄️ Inicializando base de datos...")
    try:
        from models.database import Database
        db = Database()
        print("✅ Base de datos inicializada correctamente")
    except Exception as e:
        print(f"❌ Error al inicializar base de datos: {e}")
        return False
    
    # Lanzar dashboard
    print("\n🚀 Lanzando dashboard...")
    try:
        dashboard = DashboardView()
        dashboard.render()
        print("✅ Dashboard iniciado correctamente")
        return True
    except Exception as e:
        print(f"❌ Error al iniciar dashboard: {e}")
        return False

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n👋 Aplicación cerrada por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)
