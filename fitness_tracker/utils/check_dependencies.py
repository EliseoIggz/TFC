# Limen - Verificación de Dependencias
# =============================================
# Verifica las dependencias necesarias para el funcionamiento completo

import subprocess
import sys
import importlib
from typing import Dict, List
import os

class DependencyChecker:
    """Verificador de dependencias del proyecto Limen"""
    
    def __init__(self):
        """Inicializar verificador leyendo requirements.txt automáticamente"""
        self.required_packages = self._read_requirements_file()
        self.dev_packages = {
            'pytest': 'Framework de testing',
            'pytest-cov': 'Cobertura de código en tests'
        }
    
    def _read_requirements_file(self) -> Dict[str, str]:
        """Leer requirements.txt automáticamente para obtener paquetes requeridos"""
        packages = {}
        requirements_path = os.path.join(os.path.dirname(__file__), '..', 'requirements.txt')
        
        with open(requirements_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # Ignorar líneas vacías, comentarios y paquetes de desarrollo
                if (line and 
                    not line.startswith('#') and 
                    '>=' in line and
                    not line.startswith('pytest')):
                    
                    # Extraer nombre del paquete (antes del >=)
                    package = line.split('>=')[0].strip()
                    
                    # Mapear nombres de paquetes a descripciones
                    descriptions = {
                        'streamlit': 'Framework web para el dashboard',
                        'plotly': 'Gráficas interactivas y visualizaciones',
                        'pandas': 'Manipulación y análisis de datos',
                        'requests': 'Peticiones HTTP para APIs externas',
                        'python-dateutil': 'Utilidades avanzadas de fecha y tiempo',
                        'openai': 'API de OpenAI para traducción automática (español-inglés)'
                    }
                    
                    packages[package] = descriptions.get(package, f'Paquete {package}')
        
        return packages
    
    def check_dependencies(self) -> Dict[str, any]:
        """Verificar estado de todas las dependencias"""
        print("Verificando dependencias del Limen...")
        print("=" * 60)
        print(f"📋 Leyendo paquetes desde requirements.txt...")
        print(f"📦 Paquetes requeridos encontrados: {len(self.required_packages)}")
        
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
            # Mapear nombres de paquetes a módulos de importación
            import_mapping = {
                'python-dateutil': 'dateutil',
                'openai': 'openai',
                'streamlit': 'streamlit',
                'plotly': 'plotly',
                'pandas': 'pandas',
                'requests': 'requests'
            }
            
            # Usar el nombre de importación correcto
            import_name = import_mapping.get(package, package)
            importlib.import_module(import_name)
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
