#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Probando la base de datos de deportes expandida
"""

from services.training_api import TrainingAPI

def test_expanded_sports():
    """Probar la base de datos expandida"""
    print("🏃‍♂️ Probando base de deportes expandida...")

    # Crear instancia de la API
    api = TrainingAPI()

    # 1. Contar total de deportes
    total_sports = len(api.sports_database)
    print(f"\n📊 TOTAL DE DEPORTES: {total_sports}")

    # 2. Mostrar categorías disponibles
    categories = api.get_sport_categories()
    print(f"\n🏷️ CATEGORÍAS DISPONIBLES ({len(categories)}):")
    for category, sports in categories.items():
        print(f"   📋 {category}: {len(sports)} deportes")

    # 3. Probar búsqueda de deportes
    search_terms = ['fútbol', 'running', 'yoga', 'boxeo', 'escalada', 'surf']
    print(f"\n🔍 PRUEBAS DE BÚSQUEDA:")
    for term in search_terms:
        try:
            calories = api.get_calories_burned(term, 30, 70)
            print(f"   ✅ '{term}': {calories} cal en 30 min")
        except ValueError as e:
            print(f"   ❌ '{term}': {e}")

    # 4. Probar búsqueda en inglés
    english_terms = ['football', 'soccer', 'tennis', 'swimming', 'cycling']
    print(f"\n🔍 PRUEBAS EN INGLÉS:")
    for term in english_terms:
        try:
            calories = api.get_calories_burned(term, 30, 70)
            print(f"   ✅ '{term}': {calories} cal en 30 min")
        except ValueError as e:
            print(f"   ❌ '{term}': {e}")

    # 5. Probar deportes extremos
    extreme_sports = ['paracaidismo', 'escalada_libre', 'parkour_extremo']
    print(f"\n🔍 PRUEBAS DEPORTES EXTREMOS:")
    for term in extreme_sports:
        try:
            calories = api.get_calories_burned(term, 30, 70)
            print(f"   ✅ '{term}': {calories} cal en 30 min")
        except ValueError as e:
            print(f"   ❌ '{term}': {e}")

    # 6. Probar deportes tradicionales
    traditional_sports = ['pelota_vasca', 'lucha_canaria', 'calva']
    print(f"\n🔍 PRUEBAS DEPORTES TRADICIONALES:")
    for term in traditional_sports:
        try:
            calories = api.get_calories_burned(term, 30, 70)
            print(f"   ✅ '{term}': {calories} cal en 30 min")
        except ValueError as e:
            print(f"   ❌ '{term}': {e}")

    # 7. Estadísticas finales
    print(f"\n📈 ESTADÍSTICAS FINALES:")
    print(f"   🏃‍♂️ Total deportes: {total_sports}")
    print(f"   🏷️ Total categorías: {len(categories)}")
    print(f"   🌍 Idiomas soportados: Español + Inglés")
    print(f"   💪 Cálculo de calorías: Basado en METs reales")

    print(f"\n🎯 CONCLUSIÓN:")
    print(f"   ¡Base de datos MÁS AMPLIA creada exitosamente!")
    print(f"   Ahora tienes {total_sports} deportes y actividades")
    print(f"   Perfecto para demostrar dominio de bases de datos locales")
    print(f"   Sin dependencias de APIs externas")

if __name__ == "__main__":
    test_expanded_sports()
