# Test de la Nueva API de Nutrición (Open Food Facts)
# ==================================================
# Para verificar que la API real funciona correctamente

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.nutrition_api import NutritionAPI

def test_nutrition_api():
    print("🧪 Test de la Nueva API de Nutrición (Open Food Facts)")
    print("=" * 60)
    
    nutrition_api = NutritionAPI()
    
    # Test 1: Verificar que la API está configurada
    print("\n1️⃣ Verificación de Configuración")
    print("-" * 40)
    print(f"✅ API URL: {nutrition_api.api_url}")
    print(f"✅ Timeout: {nutrition_api.timeout} segundos")
    print(f"✅ Usando API real: {nutrition_api.use_real_api}")
    
    # Test 2: Búsqueda de alimentos
    print("\n2️⃣ Test de Búsqueda de Alimentos")
    print("-" * 40)
    
    test_foods = ["pollo", "manzana", "leche", "pan", "yogur"]
    
    for food in test_foods:
        try:
            print(f"\n🔍 Probando: '{food}'")
            search_results = nutrition_api.search_food(food)
            print(f"✅ Resultados encontrados: {len(search_results)}")
            if search_results:
                print(f"   Primer resultado: {search_results[0]['name']}")
                print(f"   Marca: {search_results[0]['brand']}")
        except Exception as e:
            print(f"❌ Error en búsqueda: {e}")
    
    # Test 3: Obtención de información nutricional
    print("\n3️⃣ Test de Información Nutricional")
    print("-" * 40)
    
    test_combinations = [
        ("pollo", 150),
        ("arroz", 100),
        ("manzana", 200)
    ]
    
    for food, grams in test_combinations:
        try:
            print(f"\n🍎 Probando: '{food}' - {grams}g")
            nutrition_info = nutrition_api.get_nutrition_info(food, grams)
            print(f"✅ Nutrición obtenida:")
            print(f"   Calorías: {nutrition_info['calories']} cal")
            print(f"   Proteínas: {nutrition_info['proteins']}g")
            print(f"   Carbohidratos: {nutrition_info['carbs']}g")
            print(f"   Grasas: {nutrition_info['fats']}g")
            print(f"   Producto: {nutrition_info['product_name']}")
            print(f"   Marca: {nutrition_info['brand']}")
        except Exception as e:
            print(f"❌ Error obteniendo nutrición: {e}")
    
    # Test 4: Sugerencias de alimentos
    print("\n4️⃣ Test de Sugerencias")
    print("-" * 40)
    
    try:
        suggestions = nutrition_api.get_food_suggestions("yogur")
        print(f"✅ Sugerencias para 'yogur': {len(suggestions)}")
        if suggestions:
            print(f"   Ejemplos: {', '.join(suggestions[:3])}")
    except Exception as e:
        print(f"❌ Error en sugerencias: {e}")
    
    # Test 5: Búsqueda por código de barras (opcional)
    print("\n5️⃣ Test de Búsqueda por Código de Barras")
    print("-" * 40)
    
    # Usar un código de barras de ejemplo (Coca-Cola)
    test_barcode = "5449000000996"
    
    try:
        print(f"🔍 Probando código: {test_barcode}")
        product_info = nutrition_api.get_product_by_barcode(test_barcode)
        if product_info:
            print(f"✅ Producto encontrado:")
            print(f"   Nombre: {product_info['name']}")
            print(f"   Marca: {product_info['brand']}")
            print(f"   Código: {product_info['barcode']}")
        else:
            print(f"⚠️  Producto no encontrado para el código: {test_barcode}")
    except Exception as e:
        print(f"❌ Error en búsqueda por código: {e}")
    
    print("\n" + "=" * 60)
    print("✨ Test de API de Nutrición completado!")
    print("💡 Ahora tienes acceso a 2.5+ millones de productos reales")

if __name__ == "__main__":
    test_nutrition_api()
