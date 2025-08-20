# Fitness Tracker - Verificación de Dependencias
# =============================================
# Verifica las dependencias necesarias para el funcionamiento completo

import subprocess
import sys
import importlib
from typing import Dict, List

class DependencyChecker:
    """Verificador de dependencias del proyecto Fitness Tracker"""
    
    def __init__(self):
        """Inicializar verificador con todas las dependencias necesarias"""
        self.required_packages = {
            'streamlit': 'Framework web para el dashboard',
            'plotly': 'Gráficas interactivas y visualizaciones',
            'pandas': 'Manipulación y análisis de datos',
            'requests': 'Peticiones HTTP para APIs externas',
            'dateutil': 'Utilidades avanzadas de fecha y tiempo',
            'openai': 'API de OpenAI para traducción automática (español-inglés)'
        }
        
        self.dev_packages = {
            'pytest': 'Framework de testing',
            'pytest-cov': 'Cobertura de código en tests'
        }
    
    def check_dependencies(self) -> Dict[str, any]:
        """Verificar estado de todas las dependencias"""
        print("Verificando dependencias del Fitness Tracker...")
        print("=" * 60)
        
        results = {
            'all_required_installed': True,
            'missing_required': [],
            'missing_dev': [],
            'installed_packages': []
        }
        
        # Verificar dependencias requeridas
        print("\nDependencias Requeridas:")
        for package, description in self.required_packages.items():
            if self._is_package_installed(package):
                print(f"   [OK] {package} - {description}")
                results['installed_packages'].append(package)
            else:
                print(f"   [FALTA] {package} - {description}")
                results['missing_required'].append(package)
                results['all_required_installed'] = False
        
        # Verificar dependencias de desarrollo
        print("\nDependencias de Desarrollo:")
        for package, description in self.dev_packages.items():
            if self._is_package_installed(package):
                print(f"   [OK] {package} - {description}")
                results['installed_packages'].append(package)
            else:
                print(f"   [DEV] {package} - {description}")
                results['missing_dev'].append(package)
        
        # Mostrar resumen
        self._print_summary(results)
        
        return results
    
    def _is_package_installed(self, package: str) -> bool:
        """Verificar si un paquete está instalado y accesible"""
        try:
            importlib.import_module(package)
            return True
        except ImportError:
            return False
    
    def install_missing_dependencies(self) -> bool:
        """Instalar dependencias faltantes desde requirements.txt"""
        results = self.check_dependencies()
        
        if results['missing_required']:
            print(f"\nInstalando {len(results['missing_required'])} dependencias faltantes...")
            return self._install_from_requirements()
        
        return True
    
    def _install_from_requirements(self) -> bool:
        """Instalar dependencias desde requirements.txt"""
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("Dependencias instaladas correctamente")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error al instalar dependencias: {e}")
            return False
    
    def _print_summary(self, results: Dict):
        """Imprimir resumen del estado de las dependencias"""
        print("\n" + "=" * 60)
        print("RESUMEN DE DEPENDENCIAS")
        print("=" * 60)
        
        if results['all_required_installed']:
            print("TODAS LAS DEPENDENCIAS REQUERIDAS ESTAN INSTALADAS")
            print("La aplicación puede ejecutarse con funcionalidad completa")
        else:
            print(f"FALTAN {len(results['missing_required'])} DEPENDENCIAS REQUERIDAS")
            print(f"Paquetes faltantes: {', '.join(results['missing_required'])}")
            print("\nLa aplicación NO puede ejecutarse correctamente")
            print("Para instalar: pip install -r requirements.txt")
        
        if results['missing_dev']:
            print(f"\nDependencias de desarrollo faltantes: {', '.join(results['missing_dev'])}")
            print("Solo afecta testing y desarrollo")

def check_dependencies() -> bool:
    """Verificar si todas las dependencias requeridas están instaladas"""
    checker = DependencyChecker()
    results = checker.check_dependencies()
    return results['all_required_installed']

def install_dependencies() -> bool:
    """Instalar dependencias faltantes"""
    checker = DependencyChecker()
    return checker.install_missing_dependencies()

def get_dependency_status() -> Dict:
    """Obtener estado completo de las dependencias"""
    checker = DependencyChecker()
    return checker.check_dependencies()

if __name__ == "__main__":
    # Ejecutar verificación si se llama directamente
    checker = DependencyChecker()
    results = checker.check_dependencies()
    
    print(f"\nVERIFICACION COMPLETADA")
    print(f"Estado: {'OK' if results['all_required_installed'] else 'ERROR'}")
