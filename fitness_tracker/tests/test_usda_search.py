#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de Búsqueda USDA Directa
Prueba la búsqueda de alimentos con filtros Foundation y Legacy
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_usda_search():
    """Test de búsqueda USDA directa"""
    print("🔍 TEST DE BÚSQUEDA USDA DIRECTA")
    print("=" * 60)
    
    try:
        # Importar solo el servicio de nutrición (sin traducción automática)
        from services.nutrition_api import NutritionService
        print("✅ NutritionService importado correctamente")
        
        # Crear instancia
        nutrition_service = NutritionService()
        print("✅ Instancia creada correctamente")
        
        # Test 1: Búsqueda Foundation (calidad máxima)
        print("\n🥩 TEST 1: Búsqueda Foundation (Materias Primas)")
        print("-" * 60)
        
        foundation_foods = ["chicken", "beef", "salmon", "rice", "broccoli"]
        
        for food in foundation_foods:
            try:
                print(f"\n   🔍 Probando: '{food}' (Foundation)")
                
                # Búsqueda directa sin traducción automática
                params = {
                    'query': food,
                    'pageSize': 10,
                    'dataType': ['Foundation'],  # Solo Foundation
                    'sortBy': 'dataType.keyword',
                    'sortOrder': 'asc'
                }
                
                # Usar el método interno directamente
                response = nutrition_service._make_api_request('foods/search', params)
                
                if response and 'foods' in response and response['foods']:
                    foods_count = len(response['foods'])
                    print(f"      ✅ Foundation: {foods_count} resultados")
                    
                    if foods_count > 0:
                        first_food = response['foods'][0]
                        food_name = first_food.get('description', 'Sin nombre')
                        food_id = first_food.get('fdcId', 'Sin ID')
                        print(f"      📝 Primer resultado: {food_name}")
                        print(f"      🆔 FDC ID: {food_id}")
                        
                        # Verificar que es Foundation
                        if 'Foundation' in str(first_food.get('dataType', '')):
                            print(f"      ✅ Confirmado: Es Foundation")
                        else:
                            print(f"      ⚠️ Tipo: {first_food.get('dataType', 'Desconocido')}")
                else:
                    print(f"      ❌ Sin resultados Foundation")
                    
            except Exception as e:
                print(f"      ❌ Excepción: {e}")
        
        # Test 2: Búsqueda Legacy (productos antiguos)
        print("\n🥫 TEST 2: Búsqueda Legacy (Productos Antiguos)")
        print("-" * 60)
        
        legacy_foods = ["chicken", "beef", "salmon"]
        
        for food in legacy_foods:
            try:
                print(f"\n   🔍 Probando: '{food}' (Legacy)")
                
                # Búsqueda Legacy
                params = {
                    'query': food,
                    'pageSize': 10,
                    'dataType': ['SR Legacy'],  # Solo Legacy
                    'sortBy': 'dataType.keyword',
                    'sortOrder': 'asc'
                }
                
                response = nutrition_service._make_api_request('foods/search', params)
                
                if response and 'foods' in response and response['foods']:
                    foods_count = len(response['foods'])
                    print(f"      ✅ Legacy: {foods_count} resultados")
                    
                    if foods_count > 0:
                        first_food = response['foods'][0]
                        food_name = first_food.get('description', 'Sin nombre')
                        food_id = first_food.get('fdcId', 'Sin ID')
                        print(f"      📝 Primer resultado: {food_name}")
                        print(f"      🆔 FDC ID: {food_id}")
                        
                        # Verificar que es Legacy
                        if 'SR Legacy' in str(first_food.get('dataType', '')):
                            print(f"      ✅ Confirmado: Es Legacy")
                        else:
                            print(f"      ⚠️ Tipo: {first_food.get('dataType', 'Desconocido')}")
                else:
                    print(f"      ❌ Sin resultados Legacy")
                    
            except Exception as e:
                print(f"      ❌ Excepción: {e}")
        
        # Test 3: Búsqueda Combinada (Foundation + Legacy)
        print("\n🔄 TEST 3: Búsqueda Combinada (Foundation + Legacy)")
        print("-" * 60)
        
        combined_foods = ["chicken", "beef"]
        
        for food in combined_foods:
            try:
                print(f"\n   🔍 Probando: '{food}' (Combinada)")
                
                # Búsqueda combinada
                params = {
                    'query': food,
                    'pageSize': 15,
                    'dataType': ['Foundation', 'SR Legacy'],  # Foundation + Legacy
                    'sortBy': 'dataType.keyword',
                    'sortOrder': 'asc'
                }
                
                response = nutrition_service._make_api_request('foods/search', params)
                
                if response and 'foods' in response and response['foods']:
                    foods_count = len(response['foods'])
                    print(f"      ✅ Combinada: {foods_count} resultados")
                    
                    # Contar por tipo
                    foundation_count = 0
                    legacy_count = 0
                    
                    for food_item in response['foods']:
                        if 'Foundation' in str(food_item.get('dataType', '')):
                            foundation_count += 1
                        elif 'SR Legacy' in str(food_item.get('dataType', '')):
                            legacy_count += 1
                    
                    print(f"      📊 Foundation: {foundation_count}, Legacy: {legacy_count}")
                    
                    if foods_count > 0:
                        first_food = response['foods'][0]
                        food_name = first_food.get('description', 'Sin nombre')
                        print(f"      📝 Primer resultado: {food_name}")
                else:
                    print(f"      ❌ Sin resultados combinados")
                    
            except Exception as e:
                print(f"      ❌ Excepción: {e}")
        
        # Test 4: Verificar Filtros Inteligentes
        print("\n🧠 TEST 4: Verificar Filtros Inteligentes")
        print("-" * 60)
        
        try:
            print("   🔍 Probando filtros inteligentes con 'chicken'...")
            
            # Usar el método público que aplica filtros inteligentes
            search_results = nutrition_service.search_foods("chicken", page_size=10)
            
            if search_results and 'foods' in search_results:
                foods_count = len(search_results['foods'])
                print(f"      ✅ Filtros inteligentes: {foods_count} resultados")
                
                if foods_count > 0:
                    # Verificar que los alimentos tienen calorías
                    valid_foods = 0
                    for food in search_results['foods']:
                        calories = 0
                        for nutrient in food.get('foodNutrients', []):
                            if 'Energy' in nutrient.get('nutrientName', ''):
                                calories = nutrient.get('value', 0)
                                break
                        
                        if calories > 0:
                            valid_foods += 1
                    
                    print(f"      🔥 Alimentos con calorías válidas: {valid_foods}/{foods_count}")
                    
                    # Mostrar primeros resultados
                    print(f"      📝 Primeros resultados:")
                    for i, food in enumerate(search_results['foods'][:3]):
                        food_name = food.get('description', 'Sin nombre')
                        print(f"         {i+1}. {food_name}")
            else:
                print(f"      ❌ Sin resultados con filtros inteligentes")
                
        except Exception as e:
            print(f"      ❌ Excepción: {e}")
        
        print("\n🎯 Test de búsqueda USDA completado")
        print("💡 Este test verifica que los filtros Foundation y Legacy funcionan correctamente")
        
    except Exception as e:
        print(f"❌ Error general: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_usda_search()
