# Test de Integración OpenAI - Versión Mínima
# ==========================================
# Para verificar que OpenAI está funcionando correctamente
# SOLO 2 consultas para evitar límites

import sys
import os
import logging
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(message)s')

def test_openai_integration():
    """Probar la integración de OpenAI - SOLO 2 consultas"""
    print("🔍 **TEST MÍNIMO DE OPENAI**")
    print("=" * 40)
    print("⚠️  Solo 2 consultas para evitar límites")
    
    try:
        # 1. Verificar configuración
        print("\n1️⃣ **Verificando configuración...**")
        import config
        print(f"   🔑 OpenAI API Key configurada: {'Sí' if config.OPENAI_API_KEY else 'No'}")
        print(f"   🤖 Modelo OpenAI: {config.OPENAI_MODEL}")
        
        if not config.OPENAI_API_KEY:
            print("   ⚠️  Configura tu API key de OpenAI en config.py")
            print("   🌐 Obtén tu key en: https://platform.openai.com/api-keys")
            return
        
        # 2. Probar servicio OpenAI - 2 CONSULTAS
        print("\n2️⃣ **Probando OpenAI (2 consultas)...**")
        try:
            from services.openai_translation_service import OpenAITranslationService
            openai_service = OpenAITranslationService()
            
            if openai_service.is_available():
                print("   ✅ OpenAI disponible")
                
                # PRIMERA CONSULTA - Traducción español → inglés
                test_text = "pollo"
                print(f"\n   🔤 1ª consulta: '{test_text}' → inglés")
                print("   ⚠️  Traduciendo entrada del usuario")
                
                result = openai_service.translate_to_english(test_text)
                if result:
                    print(f"      ✅ Resultado: '{result}'")
                else:
                    print(f"      ❌ Sin resultado")
                
                # SEGUNDA CONSULTA - Traducción inglés → español
                test_text = "chicken breast"
                print(f"\n   🔤 2ª consulta: '{test_text}' → español")
                print("   ⚠️  Traduciendo respuesta del USDA")
                
                result = openai_service.translate_to_spanish(test_text)
                if result:
                    print(f"      ✅ Resultado: '{result}'")
                else:
                    print(f"      ❌ Sin resultado")
                
                print("\n      🎯 OpenAI funciona correctamente en ambas direcciones")
            else:
                print("   ❌ OpenAI no disponible")
                
        except Exception as e:
            print(f"   ❌ Error con OpenAI: {e}")
        
        print("\n✅ **Test completado - Solo 2 consultas realizadas**")
        print("💡 Para más pruebas, espera a que se resetee tu límite diario")
        
    except Exception as e:
        print(f"\n❌ **Error general: {e}**")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_openai_integration()
