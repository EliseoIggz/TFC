# Fitness Tracker - Verificación de Dependencias
# =============================================
# Este archivo verifica e instala las dependencias necesarias

import subprocess
import sys
import importlib
import os
import pkg_resources
import logging
from typing import Dict, List, Tuple, Optional

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

class DependencyChecker:
    """Clase para verificar e instalar dependencias del proyecto"""
    
    def __init__(self):
        """Inicializar el verificador de dependencias"""
        self.requirements_file = "requirements.txt"
        self.required_packages = {
            # Framework principal
            'streamlit': {'min_version': '1.28.0', 'description': 'Framework web para el dashboard'},
            
            # Visualización y datos
            'plotly': {'min_version': '5.15.0', 'description': 'Gráficas interactivas'},
            'pandas': {'min_version': '2.0.0', 'description': 'Manipulación de datos'},
            'numpy': {'min_version': '1.24.0', 'description': 'Operaciones numéricas'},
            
            # APIs y conexiones
            'requests': {'min_version': '2.31.0', 'description': 'Peticiones HTTP'},
            'openai': {'min_version': '1.0.0', 'description': 'API de OpenAI para traducción'},
            
            # Utilidades
            'dateutil': {'min_version': '2.8.0', 'description': 'Utilidades de fecha'},
            
            # Base de datos (incluida en Python)
            'sqlite3': {'min_version': None, 'description': 'Base de datos SQLite (incluida en Python)'}
        }
        
        # Dependencias opcionales (no críticas)
        self.optional_packages = {
            'pytest': {'min_version': '7.4.0', 'description': 'Testing (desarrollo)'},
            'pytest-cov': {'min_version': '4.1.0', 'description': 'Cobertura de tests (desarrollo)'}
        }
    
    def check_dependencies(self, install_missing: bool = True, check_versions: bool = True) -> Dict[str, any]:
        """Verificar e instalar dependencias faltantes"""
        print("🔍 **VERIFICACIÓN DE DEPENDENCIAS**")
        print("=" * 50)
        
        results = {
            'all_installed': True,
            'missing_packages': [],
            'version_issues': [],
            'installation_errors': [],
            'summary': {}
        }
        
        # Verificar paquetes requeridos
        print("\n📦 **Paquetes Requeridos:**")
        for package, info in self.required_packages.items():
            status = self._check_package(package, info, check_versions)
            
            if status['installed']:
                if status['version_ok']:
                    print(f"   ✅ {package} - {status['version']} - {info['description']}")
                else:
                    print(f"   ⚠️  {package} - {status['version']} (requiere {info['min_version']}+) - {info['description']}")
                    results['version_issues'].append(package)
                    results['all_installed'] = False
            else:
                print(f"   ❌ {package} - No instalado - {info['description']}")
                results['missing_packages'].append(package)
                results['all_installed'] = False
        
        # Verificar paquetes opcionales
        print("\n🎯 **Paquetes Opcionales:**")
        for package, info in self.optional_packages.items():
            status = self._check_package(package, info, check_versions)
            
            if status['installed']:
                if status['version_ok']:
                    print(f"   ✅ {package} - {status['version']} - {info['description']}")
                else:
                    print(f"   ⚠️  {package} - {status['version']} (requiere {info['min_version']}+) - {info['description']}")
            else:
                print(f"   ⚪ {package} - No instalado - {info['description']} (opcional)")
        
        # Instalar paquetes faltantes si se solicita
        if install_missing and results['missing_packages']:
            print(f"\n📥 **Instalando {len(results['missing_packages'])} paquetes faltantes...**")
            installation_success = self._install_packages(results['missing_packages'])
            
            if not installation_success:
                results['installation_errors'] = results['missing_packages']
                results['all_installed'] = False
        
        # Resumen final
        self._print_summary(results)
        
        return results
    
    def _check_package(self, package: str, info: Dict, check_versions: bool) -> Dict:
        """Verificar un paquete específico"""
        result = {
            'installed': False,
            'version': None,
            'version_ok': True
        }
        
        try:
            # Caso especial para sqlite3 (incluido en Python)
            if package == 'sqlite3':
                import sqlite3
                result['installed'] = True
                result['version'] = sqlite3.sqlite_version
                return result
            
            # Verificar si el paquete está instalado
            module = importlib.import_module(package)
            result['installed'] = True
            
            # Obtener versión del paquete
            try:
                version = pkg_resources.get_distribution(package).version
                result['version'] = version
                
                # Verificar versión mínima si se requiere
                if check_versions and info['min_version']:
                    result['version_ok'] = self._compare_versions(version, info['min_version'])
                    
            except pkg_resources.DistributionNotFound:
                result['version'] = 'versión desconocida'
                
        except ImportError:
            result['installed'] = False
        
        return result
    
    def _compare_versions(self, current_version: str, min_version: str) -> bool:
        """Comparar versiones de paquetes"""
        try:
            current = pkg_resources.parse_version(current_version)
            minimum = pkg_resources.parse_version(min_version)
            return current >= minimum
        except Exception:
            # Si no se puede comparar, asumir que está bien
            return True
    
    def _install_packages(self, packages: List[str]) -> bool:
        """Instalar paquetes usando pip"""
        success_count = 0
        
        for package in packages:
            try:
                print(f"   📦 Instalando {package}...")
                
                # Instalar el paquete
                result = subprocess.run([
                    sys.executable, "-m", "pip", "install", package
                ], capture_output=True, text=True, check=True)
                
                print(f"      ✅ {package} instalado correctamente")
                success_count += 1
                
            except subprocess.CalledProcessError as e:
                print(f"      ❌ Error instalando {package}: {e}")
                print(f"      📄 Detalles: {e.stderr}")
                
                # Intentar instalación alternativa
                if self._try_alternative_installation(package):
                    success_count += 1
                else:
                    print(f"      💡 Sugerencia: instalar manualmente con 'pip install {package}'")
        
        print(f"\n📊 **Resumen de instalación:** {success_count}/{len(packages)} paquetes instalados")
        return success_count == len(packages)
    
    def _try_alternative_installation(self, package: str) -> bool:
        """Intentar métodos alternativos de instalación"""
        print(f"      🔄 Intentando método alternativo para {package}...")
        
        try:
            # Intentar con --user flag
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", "--user", package
            ], capture_output=True, text=True, check=True)
            
            print(f"      ✅ {package} instalado con --user")
            return True
            
        except subprocess.CalledProcessError:
            try:
                # Intentar con --upgrade
                result = subprocess.run([
                    sys.executable, "-m", "pip", "install", "--upgrade", package
                ], capture_output=True, text=True, check=True)
                
                print(f"      ✅ {package} actualizado")
                return True
                
            except subprocess.CalledProcessError:
                return False
    
    def install_from_requirements(self, upgrade: bool = False) -> bool:
        """Instalar dependencias desde requirements.txt"""
        if not os.path.exists(self.requirements_file):
            print(f"❌ No se encontró {self.requirements_file}")
            return False
        
        try:
            print(f"📦 Instalando dependencias desde {self.requirements_file}...")
            
            cmd = [sys.executable, "-m", "pip", "install", "-r", self.requirements_file]
            if upgrade:
                cmd.append("--upgrade")
                print("   🔄 Modo actualización activado")
            
            subprocess.check_call(cmd)
            print("✅ Dependencias instaladas correctamente")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error al instalar dependencias: {e}")
            return False
    
    def check_environment(self) -> Dict[str, any]:
        """Verificar el entorno de desarrollo"""
        print("🔍 **VERIFICACIÓN DEL ENTORNO**")
        print("=" * 40)
        
        env_info = {
            'python_version': sys.version,
            'python_executable': sys.executable,
            'working_directory': os.getcwd(),
            'virtual_env': os.environ.get('VIRTUAL_ENV', 'No detectado'),
            'pip_version': None
        }
        
        # Verificar versión de pip
        try:
            result = subprocess.run([
                sys.executable, "-m", "pip", "--version"
            ], capture_output=True, text=True, check=True)
            env_info['pip_version'] = result.stdout.strip()
        except:
            env_info['pip_version'] = 'No disponible'
        
        # Mostrar información del entorno
        print(f"🐍 **Python:** {env_info['python_version']}")
        print(f"📍 **Ejecutable:** {env_info['python_executable']}")
        print(f"📁 **Directorio:** {env_info['working_directory']}")
        print(f"🌍 **Entorno Virtual:** {env_info['virtual_env']}")
        print(f"📦 **Pip:** {env_info['pip_version']}")
        
        return env_info
    
    def _print_summary(self, results: Dict):
        """Imprimir resumen de la verificación"""
        print("\n" + "=" * 50)
        print("📊 **RESUMEN DE VERIFICACIÓN**")
        print("=" * 50)
        
        if results['all_installed']:
            print("🎉 **ESTADO: TODAS LAS DEPENDENCIAS ESTÁN INSTALADAS**")
        else:
            print("⚠️  **ESTADO: HAY PROBLEMAS CON LAS DEPENDENCIAS**")
        
        if results['missing_packages']:
            print(f"\n❌ **Paquetes faltantes:** {', '.join(results['missing_packages'])}")
        
        if results['version_issues']:
            print(f"\n⚠️  **Problemas de versión:** {', '.join(results['version_issues'])}")
        
        if results['installation_errors']:
            print(f"\n💥 **Errores de instalación:** {', '.join(results['installation_errors'])}")
        
        # Recomendaciones
        if results['missing_packages'] or results['installation_errors']:
            print(f"\n💡 **RECOMENDACIONES:**")
            print(f"   1. Ejecutar: pip install -r {self.requirements_file}")
            print(f"   2. Verificar conexión a internet")
            print(f"   3. Actualizar pip: python -m pip install --upgrade pip")
            print(f"   4. Activar entorno virtual si es necesario")

def check_dependencies(install_missing: bool = True, check_versions: bool = True) -> bool:
    """Función de conveniencia para verificar dependencias"""
    checker = DependencyChecker()
    results = checker.check_dependencies(install_missing, check_versions)
    return results['all_installed']

def install_from_requirements(upgrade: bool = False) -> bool:
    """Función de conveniencia para instalar desde requirements.txt"""
    checker = DependencyChecker()
    return checker.install_from_requirements(upgrade)

if __name__ == "__main__":
    # Si se ejecuta directamente, verificar dependencias
    checker = DependencyChecker()
    
    print("🚀 **INICIANDO VERIFICACIÓN COMPLETA**")
    print("=" * 60)
    
    # Verificar entorno
    checker.check_environment()
    
    # Verificar dependencias
    results = checker.check_dependencies(install_missing=True, check_versions=True)
    
    # Instalar desde requirements si hay problemas
    if not results['all_installed']:
        print(f"\n🔄 **Intentando instalación desde requirements.txt...**")
        checker.install_from_requirements()
    
    print(f"\n🏁 **VERIFICACIÓN COMPLETADA**")
    print(f"   Estado final: {'✅ ÉXITO' if results['all_installed'] else '❌ PROBLEMAS'}")
