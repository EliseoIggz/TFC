#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test del Servicio de Traducción OpenAI
Prueba las funciones básicas de traducción español-inglés
"""
import sys
import os
import subprocess

def check_and_activate_venv():
    """Verificar y activar entorno virtual si es necesario"""
    try:
        # Verificar si ya estamos en un entorno virtual
        if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            print("✅ Entorno virtual ya activado")
            return True
        
        # Verificar si existe el entorno virtual
        venv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "venv")
        
        if os.path.exists(venv_path):
            print("🔄 Activando entorno virtual...")
            
            # En Windows
            if os.name == 'nt':
                activate_script = os.path.join(venv_path, "Scripts", "activate.bat")
                if os.path.exists(activate_script):
                    print("💡 Para activar el entorno virtual en Windows, ejecuta:")
                    print(f"   {activate_script}")
                    print("💡 O usa: run_tests.bat")
            else:
                # En Linux/Mac
                activate_script = os.path.join(venv_path, "bin", "activate")
                if os.path.exists(activate_script):
                    print("💡 Para activar el entorno virtual en Linux/Mac, ejecuta:")
                    print(f"   source {activate_script}")
                    print("💡 O usa: ./run_tests.sh")
            
            print("⚠️  No se puede activar automáticamente desde Python")
            print("💡 Ejecuta el script correspondiente a tu sistema operativo")
            return False
        else:
            print("❌ No se encontró el entorno virtual")
            print("💡 Crea el entorno virtual con: python -m venv venv")
            return False
            
    except Exception as e:
        print(f"❌ Error verificando entorno virtual: {e}")
        return False

def test_translation_service():
    """Test básico del servicio de traducción"""
    print("🔤 TEST DEL SERVICIO DE TRADUCCIÓN")
    print("=" * 50)
    
    # Verificar entorno virtual
    if not check_and_activate_venv():
        return
    
    try:
        # Importar el servicio de traducción
        from services.translation_service import TranslationService
        print("✅ TranslationService importado correctamente")
        
        # Crear instancia
        translation_service = TranslationService()
        print("✅ Instancia creada correctamente")
        
        # Verificar disponibilidad de OpenAI
        is_available = translation_service.is_available()
        print(f"✅ OpenAI disponible: {is_available}")
        
        if not is_available:
            print("❌ OpenAI no está disponible. Verifica tu API key.")
            return
        
        # Test de traducción español a inglés
        print("\n🇪🇸 → 🇬🇧 Traducción español a inglés:")
        spanish_words = ['pollo', 'manzana', 'leche', 'pan']
        
        for word in spanish_words:
            try:
                translation = translation_service.translate_to_english(word)
                if translation:
                    print(f"   ✅ '{word}' → '{translation}'")
                else:
                    print(f"   ❌ '{word}' → Error en traducción")
            except Exception as e:
                print(f"   ❌ '{word}' → Error: {e}")
        
        # Test de traducción inglés a español
        print("\n🇬🇧 → 🇪🇸 Traducción inglés a español:")
        english_words = ['chicken', 'apple', 'milk', 'bread']
        
        for word in english_words:
            try:
                translation = translation_service.translate_to_spanish(word)
                if translation:
                    print(f"   ✅ '{word}' → '{translation}'")
                else:
                    print(f"   ❌ '{word}' → Error en traducción")
            except Exception as e:
                print(f"   ❌ '{word}' → Error: {e}")
        
        print("\n🎯 Test completado exitosamente")
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        print("💡 Asegúrate de que el entorno virtual esté activado")
        print("💡 Y que las dependencias estén instaladas: pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Error general: {e}")

if __name__ == "__main__":
    test_translation_service()
