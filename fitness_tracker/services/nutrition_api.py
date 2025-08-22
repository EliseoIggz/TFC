import requests
import config
import logging
from typing import Dict, List, Optional
from .translation_service import TranslationService

logger = logging.getLogger(__name__)

class NutritionService:
    """API para obtener información nutricional desde USDA FoodData Central"""
    
    def __init__(self):
        """Inicializar la API de USDA"""
        self.api_key = config.USDA_API_KEY
        self.base_url = config.USDA_API_BASE_URL
        self.timeout = 15
        self.translation_service = TranslationService()
        
        # Headers para las peticiones
        self.headers = {
            'User-Agent': 'FitnessTrackerApp/1.0',
            'Accept': 'application/json'
        }
        
        # Añadir API key si está disponible
        if self.api_key:
            self.headers['X-API-Key'] = self.api_key
            
    def _make_api_request(self, endpoint: str, params: Dict = None) -> Optional[Dict]:
        """Realizar petición a la API de USDA"""
        try:
            url = f"{self.base_url}/{endpoint}"
            
            # Parámetros por defecto - USDA requiere api_key en parámetros, no en headers
            default_params = {
                'api_key': self.api_key,
                'format': 'json'
            } if self.api_key else {'format': 'json'}
            
            # Combinar parámetros
            if params:
                default_params.update(params)
            
            logger.debug(f"Parámetros: {default_params}")
            
            response = requests.get(
                url,
                params=default_params,
                headers=self.headers,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                return data
            elif response.status_code == 401:
                logger.error("Error de autenticación en USDA API - verificar API key")
                return None
            elif response.status_code == 403:
                logger.error("Error de autorización en USDA API - verificar API key")
                return None
            elif response.status_code == 429:
                logger.warning("Rate limit alcanzado en USDA API")
                return None
            else:
                logger.error(f"Error en USDA API: {response.status_code} - {response.text[:200]}")
                return None
                
        except requests.exceptions.Timeout:
            logger.error("Timeout en petición a USDA API")
            return None
        except Exception as e:
            logger.error(f"Error inesperado en petición a USDA API: {e}")
            return None
    
    def search_foods(self, query: str, page_size: int = 25) -> Optional[Dict]:
        """Buscar alimentos en la base de datos de USDA con estrategia híbrida"""
        try:
            # FLUJO SIMPLE: Español → Inglés → Buscar en USDA
            english_query = query
            
            # 1. Traducir la consulta a inglés usando OpenAI
            if self.translation_service.is_available():
                try:
                    translated_query = self.translation_service.translate_to_english(query)
                    if translated_query and translated_query.lower() != query.lower():
                        english_query = translated_query
                except Exception as e:
                    logger.warning(f"Error en traducción de consulta: {e}")
            
            # 2. PRIMERA BÚSQUEDA: Solo Foundation (calidad máxima) (Foundation = Materias primas)
            params = {
                'query': english_query,
                'pageSize': min(page_size * 3, 75),  # Muchos más resultados
                'dataType': ['Foundation'],  # Solo Foundation para calidad
                'sortBy': 'dataType.keyword',
                'sortOrder': 'asc'
            }
            
            response = self._make_api_request('foods/search', params)
            
            if response and 'foods' in response and response['foods']:
                foods = response['foods']
                sorted_foods = self._sort_foods_by_calories(foods)
                
                # Si hay suficientes resultados (≥5), devolver solo Foundation
                if len(sorted_foods) >= 5:
                    return {'foods': sorted_foods}
                
                # Si hay menos de 5 resultados, expandir a Legacy
                logger.info(f"Solo {len(sorted_foods)} resultados en Foundation, expandiendo a Legacy...")
                
                # 3. SEGUNDA BÚSQUEDA: Incluir Legacy para más opciones (Legacy = Productos antiguos)
                params_legacy = {
                    'query': english_query,
                    'pageSize': min(page_size * 2, 50),  # Resultados moderados
                    'dataType': ['Foundation', 'SR Legacy'],  # Foundation + Legacy
                    'sortBy': 'dataType.keyword',
                    'sortOrder': 'asc'
                }
                
                response_legacy = self._make_api_request('foods/search', params_legacy)
                
                if response_legacy and 'foods' in response_legacy and response_legacy['foods']:
                    # Combinar y ordenar todos los resultados
                    all_foods = foods + response_legacy['foods']
                    # Eliminar duplicados por FDC ID
                    unique_foods = {food['fdcId']: food for food in all_foods}.values()
                    sorted_foods_combined = self._sort_foods_by_calories(list(unique_foods))
                    
                    logger.info(f"Expandido a {len(sorted_foods_combined)} resultados (Foundation + Legacy)")
                    return {'foods': sorted_foods_combined}
                
                # Si no hay resultados con Legacy, devolver solo Foundation
                return {'foods': sorted_foods}
            else:
                logger.warning(f"No se encontraron resultados para '{english_query}'")
                return None
            
        except Exception as e:
            logger.error(f"Error buscando alimentos: {e}")
            return None
    
    def _sort_foods_by_calories(self, foods: List[Dict]) -> List[Dict]:
        """Ordenar alimentos por calorías (menor a mayor) y filtrar los que no tienen calorías"""
        try:
            def get_calories(food):
                # Buscar calorías en los nutrientes del alimento
                food_nutrients = food.get('foodNutrients', [])
                for nutrient in food_nutrients:
                    nutrient_name = nutrient.get('nutrientName', '')
                    if 'Energy' in nutrient_name or 'Calories' in nutrient_name:
                        return nutrient.get('value', 0)
                return 0  # Si no se encuentran calorías
            
            # Filtrar alimentos con calorías válidas (> 0)
            valid_foods = []
            for food in foods:
                calories = get_calories(food)
                if calories > 0:
                    valid_foods.append(food)
                else:
                    logger.debug(f"Filtrado alimento sin calorías: {food.get('description', 'Sin descripción')}")
            
            # Ordenar por calorías (menor a mayor)
            sorted_foods = sorted(valid_foods, key=get_calories)
            
            logger.info(f"Filtrados {len(foods) - len(valid_foods)} alimentos sin calorías. Quedan {len(sorted_foods)} alimentos válidos.")
            return sorted_foods
            
        except Exception as e:
            logger.error(f"Error ordenando por calorías: {e}")
            return foods  # Devolver sin ordenar si hay error
    

    def get_food_details(self, fdc_id: int) -> Optional[Dict]:
        """Obtener detalles completos de un alimento por su FDC ID"""
        try:
            
            response = self._make_api_request(f'food/{fdc_id}')
            return response
            
        except Exception as e:
            logger.error(f"Error obteniendo detalles del alimento: {e}")
            return None
    
    def get_nutrition_info(self, food: str, grams: float) -> Dict:
        """Obtener información nutricional de un alimento"""
        try:
            
            # Buscar el alimento
            search_results = self.search_foods(food)
            
            if not search_results or 'foods' not in search_results:
                raise ValueError(f"No se encontraron resultados para '{food}' en la base de datos de USDA")
            
            foods = search_results['foods']
            if not foods:
                raise ValueError(f"No se encontraron alimentos para '{food}'")
            
            # Si hay múltiples resultados, mostrar opciones
            if len(foods) > 1:
                return self._show_food_options(foods, food, grams)
            
            # Si solo hay un resultado, usarlo directamente
            selected_food = foods[0]
            nutrition_data = self._extract_nutrition_data(selected_food, grams)
            
            # Traducir nombre al español usando OpenAI
            spanish_name = self.translation_service.translate_to_spanish(selected_food.get('description', food))
            if spanish_name:
                nutrition_data['product_name'] = spanish_name
            else:
                nutrition_data['product_name'] = selected_food.get('description', food)
            
            return nutrition_data
            
        except ValueError as ve:
            raise ve
        except Exception as e:
            logger.error(f"Error obteniendo nutrición: {e}")
            raise ValueError(f"Error conectando con la base de datos de USDA: {str(e)}")
    
    def _show_food_options(self, foods: List[Dict], search_term: str, grams: float) -> Dict:
        """Mostrar opciones de alimentos para que el usuario elija, priorizando alimentos 'raw'"""
        
        # PRIORIZAR: Foundation + Raw dentro de Foundation + Raw dentro de Legacy + Otros
        def prioritize_foundation_and_raw(food_list):
            """Priorizar Foundation primero, luego Raw dentro de cada tipo"""
            foundation_raw = []
            foundation_other = []
            legacy_raw = []
            legacy_other = []
            
            for food in food_list:
                description = food.get('description', '').lower()
                is_raw = 'raw' in description
                
                # Detectar si es Foundation o Legacy por el tipo de datos
                # Foundation suele tener descripciones más simples y directas
                # Legacy suele tener descripciones más largas o específicas
                is_foundation = len(description.split()) <= 8  # Descripciones Foundation son más cortas
                
                if is_foundation:
                    if is_raw:
                        foundation_raw.append(food)
                    else:
                        foundation_other.append(food)
                else:
                    if is_raw:
                        legacy_raw.append(food)
                    else:
                        legacy_other.append(food)
            
            # Orden de prioridad: Foundation Raw → Foundation Other → Legacy Raw → Legacy Other
            return foundation_raw + foundation_other + legacy_raw + legacy_other
        
        # Aplicar priorización y tomar los primeros 10
        prioritized_foods = prioritize_foundation_and_raw(foods)[:10]
        
        options = []
        for i, food in enumerate(prioritized_foods):
            # Obtener información nutricional básica
            nutrition = self._extract_nutrition_data(food, 100)  # Por 100g
            
            # Traducir descripción al español usando OpenAI
            spanish_description = self.translation_service.translate_to_spanish(food.get('description', ''))
            display_name = spanish_description if spanish_description else food.get('description', 'Sin descripción')
            
            # Marcar si es alimento "raw" para el usuario
            is_raw = 'raw' in food.get('description', '').lower()
            raw_indicator = " 🥩" if is_raw else ""
            
            option_info = {
                'number': i,
                'fdc_id': food.get('fdcId'),
                'name': display_name,
                'original_name': food.get('description', ''),
                'calories_per_100g': nutrition['calories'],
                'proteins_per_100g': nutrition['proteins'],
                'carbs_per_100g': nutrition['carbs'],
                'fats_per_100g': nutrition['fats'],
                'food': food,
                'display_name': f"{display_name}{raw_indicator} - {nutrition['calories']} cal/100g",
                'is_raw': is_raw
            }
            options.append(option_info)
        
        return {
            'multiple_options': True,
            'search_term': search_term,
            'grams': grams,
            'options': options
        }
    
    def get_nutrition_from_selected_option(self, option_data: Dict, selected_index: int) -> Dict:
        """Obtener nutrición del alimento seleccionado por el usuario"""
        try:
            if selected_index < 0 or selected_index >= len(option_data['options']):
                raise ValueError("Índice de selección inválido")
            
            selected_option = option_data['options'][selected_index]
            selected_food = selected_option['food']
            grams = option_data['grams']
            
            # Extraer información nutricional del alimento seleccionado
            nutrition_data = self._extract_nutrition_data(selected_food, grams)
            
            # Traducir el nombre al español
            spanish_name = self.translation_service.translate_to_spanish(selected_food.get('description', ''))
            if spanish_name:
                nutrition_data['product_name'] = spanish_name
            
            return nutrition_data
            
        except Exception as e:
            logger.error(f"Error procesando selección: {e}")
            raise ValueError(f"Error procesando la opción seleccionada: {str(e)}")
    
    def _extract_nutrition_data(self, food: Dict, grams: float) -> Dict:
        """Extraer datos nutricionales de un alimento de USDA"""
        try:
            # Obtener nutrientes del alimento
            food_nutrients = food.get('foodNutrients', [])
            
            # Mapeo de nutrientes USDA a nuestros campos
            nutrition_mapping = {
                'calories': ['Energy', 'Calories'],
                'proteins': ['Protein'],
                'carbs': ['Carbohydrate, by difference'],
                'fats': ['Total lipid (fat)'],
                'fiber': ['Fiber, total dietary'],
                'sugar': ['Sugars, total including NLEA'],
                'sodium': ['Sodium, Na'],
                'cholesterol': ['Cholesterol']
            }
            
            # Extraer valores nutricionales
            nutrition_values = {}
            for nutrient in food_nutrients:
                nutrient_name = nutrient.get('nutrientName', '')
                nutrient_value = nutrient.get('value', 0)
                unit = nutrient.get('unitName', '')
                
                # Mapear nutrientes
                for our_field, usda_names in nutrition_mapping.items():
                    if any(usda_name in nutrient_name for usda_name in usda_names):
                        nutrition_values[our_field] = nutrient_value
                        break
            
            # Valores por defecto si no se encuentran
            calories_per_100g = nutrition_values.get('calories', 0)
            proteins_per_100g = nutrition_values.get('proteins', 0)
            carbs_per_100g = nutrition_values.get('carbs', 0)
            fats_per_100g = nutrition_values.get('fats', 0)
            
            # Calcular valores para la cantidad especificada
            multiplier = grams / 100
            
            return {
                'calories': round(calories_per_100g * multiplier),
                'proteins': round(proteins_per_100g * multiplier, 1),
                'carbs': round(carbs_per_100g * multiplier, 1),
                'fats': round(fats_per_100g * multiplier, 1),
                'fiber': round(nutrition_values.get('fiber', 0) * multiplier, 1),
                'sugar': round(nutrition_values.get('sugar', 0) * multiplier, 1),
                'sodium': round(nutrition_values.get('sodium', 0) * multiplier, 1),
                'cholesterol': round(nutrition_values.get('cholesterol', 0) * multiplier, 1),
                'product_name': food.get('description', 'Producto'),
                'fdc_id': food.get('fdcId', 'Sin ID')
            }
            
        except Exception as e:
            logger.error(f"Error extrayendo datos nutricionales: {e}")
            raise ValueError(f"Error procesando información nutricional del alimento: {str(e)}")
    
    def search_food(self, query: str) -> List[Dict]:
        """Buscar alimentos en USDA"""
        try:
            search_results = self.search_foods(query, page_size=10)
            
            if not search_results or 'foods' not in search_results:
                return []
            
            results = []
            for food in search_results['foods'][:5]:  # Máximo 5 resultados
                # Traducir descripción al español
                spanish_description = self.translation_service.translate_to_spanish(food.get('description', ''))
                display_name = spanish_description if spanish_description else food.get('description', 'Sin descripción')
                
                results.append({
                    'name': display_name,
                    'original_name': food.get('description', ''),
                    'fdc_id': food.get('fdcId', 'Sin ID')
                })
            
            return results
            
        except Exception as e:
            logger.error(f"Error en búsqueda: {e}")
            return []
    
    def get_food_suggestions(self, query: str) -> List[str]:
        """Obtener sugerencias de nombres de alimentos"""
        try:
            search_results = self.search_food(query)
            suggestions = [result['name'] for result in search_results]
            return suggestions
            
        except Exception as e:
            logger.error(f"Error obteniendo sugerencias: {e}")
            return []
    
    def get_food_by_fdc_id(self, fdc_id: int) -> Optional[Dict]:
        """Obtener información de un alimento por su FDC ID"""
        try:
            food_details = self.get_food_details(fdc_id)
            
            if food_details:
                # Traducir descripción al español
                spanish_description = self.translation_service.translate_to_spanish(food_details.get('description', ''))
                display_name = spanish_description if spanish_description else food_details.get('description', 'Sin descripción')
                
                return {
                    'name': display_name,
                    'original_name': food_details.get('description', ''),
                    'fdc_id': food_details.get('fdcId', 'Sin ID'),
                    'ingredients': food_details.get('ingredients', 'Sin ingredientes'),
                    'allergens': food_details.get('allergens', []),
                    'nutrients': food_details.get('foodNutrients', [])
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error obteniendo alimento por FDC ID: {e}")
            return None
