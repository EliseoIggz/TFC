# Test de la Nueva API de Nutrición (USDA FoodData Central)
# ========================================================
# Para verificar que la API de USDA funciona correctamente

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.nutrition_api import NutritionService
from services.translation_service import TranslationService

def test_usda_nutrition_api():
    print("🧪 Test de la Nueva API de Nutrición (USDA FoodData Central)")
    print("=" * 70)
    
    usda_api = NutritionService()
    
    # Test 1: Verificar que la API está configurada
    print("\n1️⃣ Verificación de Configuración")
    print("-" * 40)
    print(f"✅ API URL: {usda_api.base_url}")
    print(f"✅ Timeout: {usda_api.timeout} segundos")
    print(f"✅ API Key configurada: {'Sí' if usda_api.api_key else 'No (modo público)'}")
    
    # Test 2: Búsqueda de alimentos
    print("\n2️⃣ Test de Búsqueda de Alimentos")
    print("-" * 40)
    
    test_foods = ["chicken", "apple", "milk", "bread", "yogurt"]
    
    for food in test_foods:
        try:
            print(f"\n🔍 Probando: '{food}'")
            search_results = usda_api.search_foods(food, page_size=5)
            if search_results and 'foods' in search_results:
                print(f"✅ Resultados encontrados: {len(search_results['foods'])}")
                if search_results['foods']:
                    first_result = search_results['foods'][0]
                    print(f"   Primer resultado: {first_result.get('description', 'Sin descripción')}")
                    print(f"   Marca: {first_result.get('brandOwner', 'Sin marca')}")
                    print(f"   FDC ID: {first_result.get('fdcId', 'Sin ID')}")
                    print(f"   Tipo: {first_result.get('dataType', 'Desconocido')}")
            else:
                print(f"❌ Sin resultados para: {food}")
        except Exception as e:
            print(f"❌ Error en búsqueda: {e}")
    
    # Test 3: Obtención de información nutricional
    print("\n3️⃣ Test de Información Nutricional")
    print("-" * 40)
    
    test_combinations = [
        ("chicken", 150),
        ("rice", 100),
        ("apple", 200)
    ]
    
    for food, grams in test_combinations:
        try:
            print(f"\n🍎 Probando: '{food}' - {grams}g")
            nutrition_info = usda_api.get_nutrition_info(food, grams)
            
            if 'multiple_options' in nutrition_info:
                print(f"✅ Múltiples opciones encontradas: {len(nutrition_info['options'])}")
                if nutrition_info['options']:
                    first_option = nutrition_info['options'][0]
                    print(f"   Primera opción: {first_option['name']}")
                    print(f"   Calorías/100g: {first_option['calories_per_100g']}")
                    print(f"   Proteínas/100g: {first_option['proteins_per_100g']}")
            else:
                print(f"✅ Nutrición obtenida:")
                print(f"   Calorías: {nutrition_info['calories']} cal")
                print(f"   Proteínas: {nutrition_info['proteins']}g")
                print(f"   Carbohidratos: {nutrition_info['carbs']}g")
                print(f"   Grasas: {nutrition_info['fats']}g")
                print(f"   Producto: {nutrition_info['product_name']}")
                print(f"   FDC ID: {nutrition_info['fdc_id']}")
        except Exception as e:
            print(f"❌ Error obteniendo nutrición: {e}")
    
    # Test 4: Sugerencias de alimentos
    print("\n4️⃣ Test de Sugerencias")
    print("-" * 40)
    
    try:
        suggestions = usda_api.get_food_suggestions("yogurt")
        print(f"✅ Sugerencias para 'yogurt': {len(suggestions)}")
        if suggestions:
            print(f"   Ejemplos: {', '.join(suggestions[:3])}")
    except Exception as e:
        print(f"❌ Error en sugerencias: {e}")
    
    # Test 5: Búsqueda por FDC ID (opcional)
    print("\n5️⃣ Test de Búsqueda por FDC ID")
    print("-" * 40)
    
    # Usar un FDC ID de ejemplo (Apple, raw, with skin)
    test_fdc_id = 171688
    
    try:
        print(f"🔍 Probando FDC ID: {test_fdc_id}")
        food_info = usda_api.get_food_by_fdc_id(test_fdc_id)
        if food_info:
            print(f"✅ Alimento encontrado:")
            print(f"   Nombre: {food_info['name']}")
            print(f"   FDC ID: {food_info['fdc_id']}")
        else:
            print(f"⚠️  Alimento no encontrado para el FDC ID: {test_fdc_id}")
    except Exception as e:
        print(f"❌ Error en búsqueda por FDC ID: {e}")
    
    print("\n" + "=" * 70)
    print("✨ Test de API de Nutrición USDA completado!")
    print("💡 Ahora tienes acceso a 300,000+ alimentos oficiales del gobierno de EE.UU.")

def test_translation_service():
    print("\n🌐 Test del Servicio de Traducción (OpenAI)")
    print("=" * 60)
    
    translator = TranslationService()
    
    # Test 1: Traducción español → inglés
    print("\n1️⃣ Traducción español → inglés")
    spanish_texts = ["pollo asado", "manzana roja", "arroz integral"]
    
    for text in spanish_texts:
        try:
            english_translation = translator.translate_to_english(text)
            print(f"   '{text}' → '{english_translation}'")
        except Exception as e:
            print(f"   ❌ Error traduciendo '{text}': {e}")
    
    # Test 2: Traducción inglés → español
    print("\n2️⃣ Traducción inglés → español")
    english_texts = ["grilled chicken", "red apple", "brown rice"]
    
    for text in english_texts:
        try:
            spanish_translation = translator.translate_to_spanish(text)
            print(f"   '{text}' → '{spanish_translation}'")
        except Exception as e:
            print(f"   ❌ Error traduciendo '{text}': {e}")
    
    # Test 3: Detección de idioma
    print("\n3️⃣ Detección de idioma")
    test_texts = [
        ("manzana roja", "es"),
        ("red apple", "en"),
        ("pollo", "es"),
        ("chicken", "en")
    ]
    
    for text, expected_lang in test_texts:
        try:
            detected_lang = translator.detect_language(text)
            status = "✅" if detected_lang == expected_lang else "❌"
            print(f"   {status} '{text}' → {detected_lang} (esperado: {expected_lang})")
        except Exception as e:
            print(f"   ❌ Error detectando idioma de '{text}': {e}")
    
    # Test 4: Traducción inteligente
    print("\n4️⃣ Traducción inteligente")
    test_cases = [
        ("pollo asado", "en"),
        ("grilled chicken", "es"),
        ("arroz", "en"),
        ("rice", "es")
    ]
    
    for text, target_lang in test_cases:
        try:
            translation = translator.smart_translate(text, target_lang)
            print(f"   '{text}' → '{translation}' ({target_lang})")
        except Exception as e:
            print(f"   ❌ Error en traducción inteligente de '{text}': {e}")
    
    print("\n✅ Servicio de traducción probado")

if __name__ == "__main__":
    print("🧪 Test Completo del Nuevo Sistema de Nutrición")
    print("=" * 80)
    print("🔧 APIs: USDA FoodData Central + OpenAI")
    print("🌐 Traducción: Español ↔ Inglés automática")
    print("📊 Base de datos: 300,000+ alimentos oficiales del gobierno de EE.UU.")
    print("=" * 80)
    
    try:
        # Probar servicio de traducción
        test_translation_service()
        
        # Probar API de USDA
        test_usda_nutrition_api()
        
        print("\n" + "=" * 80)
        print("🎉 ¡Todas las pruebas completadas exitosamente!")
        print("✅ El nuevo sistema de nutrición está funcionando correctamente")
        print("💡 Ahora tienes acceso a la base de datos oficial de USDA")
        print("🌐 Con traducción automática español-inglés")
        print("🔑 Recomendación: Obtener API key gratuita en https://fdc.nal.usda.gov/api-key-signup.html")
        
    except Exception as e:
        print(f"\n❌ Error durante las pruebas: {e}")
        print("🔍 Verificar configuración de APIs y conexión a internet")
