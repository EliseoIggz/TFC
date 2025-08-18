# Fitness Tracker - API Real de Nutrición (Open Food Facts)
# ========================================================
# Este archivo integra la API real de Open Food Facts para obtener información nutricional

import requests
import config
from typing import Dict, List, Optional
import time
import json

class NutritionAPI:
    """API real para obtener información nutricional de alimentos desde Open Food Facts"""
    
    def __init__(self):
        """Inicializar la API real con configuración optimizada"""
        self.api_url = config.OPENFOODFACTS_API_URL
        self.timeout = config.OPENFOODFACTS_API_TIMEOUT
        self.use_real_api = True  # Siempre usar API real
        
        # Headers optimizados para mejor rendimiento
        self.headers = {
            'User-Agent': 'FitnessTrackerApp/1.0 (https://github.com/fitness-tracker)',
            'Accept': 'application/json',
            'Accept-Language': 'es,en;q=0.9'
        }
    
    def _make_api_request(self, params: Dict, is_fresh_food: bool = False) -> Optional[Dict]:
        """Realizar petición optimizada a Open Food Facts API"""
        try:
            # Parámetros base optimizados para España y español
            default_params = {
                'search_terms': '',
                'search_simple': 1,
                'action': 'process',
                'json': 1,
                'page_size': 10,
                'page': 1,
                # Optimizaciones para España
                'lc': 'es',  # Idioma español
                'cc': 'es',  # País España
                'nocache': 1,  # Sin caché para datos frescos
                # Ordenar por datos recientes
                'sort_by': 'last_modified_t',
                # Campos específicos para optimizar transferencia
                'fields': 'product_name_es,product_name,nutriments,categories_tags,labels_tags,brands,image_url,nutrition_grade_fr'
            }
            
            # Filtros específicos para alimentos frescos
            if is_fresh_food:
                fresh_params = {
                    # Sin aditivos
                    'additives': 'without',
                    # Categorías de alimentos frescos
                    'tagtype_0': 'categories',
                    'tag_0': 'fresh-vegetables',
                    'tag_contains_0': 'contains',
                    # Excluir procesados
                    'tagtype_1': 'categories', 
                    'tag_1': 'processed-foods',
                    'tag_contains_1': 'does_not_contain'
                }
                default_params.update(fresh_params)
            
            # Combinar parámetros
            search_params = {**default_params, **params}
            
            # Log de debug con query generada
            query_example = f"Query: {search_params.get('search_terms', 'N/A')}"
            if is_fresh_food:
                query_example += " [MODO FRESCO]"
            print(f"🔍 {query_example}")
            
            # Log detallado para depuración
            if is_fresh_food:
                print(f"📋 Filtros aplicados: sin aditivos, categoría=fresh-vegetables, excluye=processed-foods")
            
            response = requests.get(
                self.api_url, 
                params=search_params,
                headers=self.headers,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if 'products' in data:
                    count = len(data['products'])
                    print(f"📊 Productos encontrados: {count}")
                    
                    # Log de ejemplos para depuración
                    if count > 0:
                        first_product = data['products'][0]
                        product_name = first_product.get('product_name_es', first_product.get('product_name', 'Sin nombre'))
                        categories = first_product.get('categories_tags', [])
                        print(f"📝 Ejemplo: '{product_name}' - Categorías: {categories[:3] if categories else 'N/A'}")
                    
                    if count == 0:
                        print(f"⚠️  Sin resultados para: {search_params.get('search_terms', 'N/A')}")
                else:
                    print(f"📊 Respuesta recibida: {type(data)}")
                
                return data
                
            elif response.status_code == 429:
                print("⏳ Rate limit alcanzado, esperando...")
                time.sleep(2)
                return None
            else:
                print(f"❌ Error API ({response.status_code}): {response.text[:100]}")
                return None
                
        except requests.exceptions.Timeout:
            print(f"⏰ Timeout después de {self.timeout}s")
            return None
        except Exception as e:
            print(f"❌ Error en petición API: {e}")
            return None
    
    def get_nutrition_info(self, food: str, grams: float) -> Dict:
        """Obtener información nutricional optimizada desde Open Food Facts"""
        try:
            # Determinar si es un alimento fresco
            is_fresh = self._is_fresh_food(food)
            
            # Estrategia de búsqueda progresiva optimizada
            search_terms = self._get_progressive_search_terms(food)
            
            for i, search_term in enumerate(search_terms):
                print(f"🔍 Intento {i+1}/{len(search_terms)}: '{search_term}'")
                
                search_params = {
                    'search_terms': search_term,
                    'page_size': 10
                }
                
                # Usar modo fresco solo en los primeros intentos para verduras/frutas
                use_fresh_mode = is_fresh and i < 2
                
                api_response = self._make_api_request(search_params, is_fresh_food=use_fresh_mode)
                
                if api_response and 'products' in api_response and api_response['products']:
                    # Filtrar y priorizar con scoring avanzado
                    filtered_products = self._filter_and_prioritize_products_advanced(
                        api_response['products'], food, is_fresh
                    )
                    
                    if filtered_products:
                        if len(filtered_products) > 1:
                            return self._show_product_options(filtered_products[:5], food, grams)
                        else:
                            best_product = filtered_products[0]
                            nutrition_data = self._extract_nutrition_data(best_product, grams)
                            product_name = best_product.get('product_name_es', best_product.get('product_name', food))
                            print(f"✅ '{food}' → '{product_name}': {nutrition_data['calories']} cal")
                            return nutrition_data
            
            # Si no se encuentra después de todos los intentos
            raise ValueError(f"❌ No se encontró '{food}' en la base de datos de Open Food Facts. Prueba con un nombre más específico o diferente.")
                
        except ValueError as ve:
            raise ve
        except Exception as e:
            raise ValueError(f"❌ Error conectando con la base de datos: {str(e)}")
    
    def _get_progressive_search_terms(self, food: str) -> List[str]:
        """Obtener términos de búsqueda progresiva: específico → general"""
        food_lower = food.lower().strip()
        search_terms = []
        
        # Mapeo optimizado con enfoque en alimentos frescos
        progressive_searches = {
            # === TUBÉRCULOS Y CEREALES ===
            'patatas': ['patata fresca cruda', 'patata', 'papa fresca', 'papa'],
            'patata': ['patata fresca cruda', 'patata', 'papa'],
            'papa': ['papa fresca', 'patata', 'papa'],
            'papas': ['patata fresca cruda', 'patata', 'papa'],
            'arroz': ['arroz blanco', 'arroz'],
            'pasta': ['pasta', 'macarrones'],
            'pan': ['pan blanco', 'pan'],
            'avena': ['avena', 'oats'],
            'quinoa': ['quinoa', 'quinua'],
            
            # === CARNES ===
            'pollo': ['pollo fresco crudo', 'pechuga pollo', 'pollo'],
            'ternera': ['ternera fresca cruda', 'ternera', 'beef'],
            'cerdo': ['cerdo fresco crudo', 'cerdo', 'pork'],
            'pavo': ['pavo fresco', 'pavo', 'turkey'],
            'cordero': ['cordero fresco', 'cordero', 'lamb'],
            'jamón': ['jamón', 'ham'],
            
            # === PESCADOS Y MARISCOS ===
            'pescado': ['pescado fresco', 'pescado', 'fish fresh'],
            'salmón': ['salmón fresco', 'salmón', 'salmon fresh'],
            'atún': ['atún fresco', 'atún', 'tuna fresh'],
            'merluza': ['merluza fresca', 'merluza', 'hake'],
            'bacalao': ['bacalao fresco', 'bacalao', 'cod'],
            'sardinas': ['sardinas frescas', 'sardinas', 'sardines'],
            'gambas': ['gambas frescas', 'gambas', 'shrimp fresh'],
            
            # === LÁCTEOS ===
            'leche': ['leche entera', 'leche'],
            'yogur': ['yogur natural', 'yogur'],
            'queso': ['queso fresco', 'queso'],
            'mantequilla': ['mantequilla', 'butter'],
            'nata': ['nata', 'cream'],
            
            # === HUEVOS ===
            'huevo': ['huevo fresco', 'huevo'],
            'huevos': ['huevos frescos', 'huevo'],
            
            # === VERDURAS FRESCAS ===
            'brócoli': ['brócoli fresco crudo', 'brócoli fresco', 'brócoli orgánico', 'brócoli', 'broccoli fresh'],
            'tomate': ['tomate fresco', 'tomate', 'tomato fresh'],
            'tomates': ['tomate fresco', 'tomate'],
            'cebolla': ['cebolla fresca', 'cebolla', 'onion fresh'],
            'cebollas': ['cebolla fresca', 'cebolla'],
            'zanahoria': ['zanahoria fresca', 'zanahoria', 'carrot fresh'],
            'zanahorias': ['zanahoria fresca', 'zanahoria'],
            'calabacín': ['calabacín fresco', 'calabacín', 'zucchini fresh'],
            'espárragos': ['espárragos frescos', 'espárragos', 'asparagus fresh'],
            'espinacas': ['espinacas frescas', 'espinacas', 'spinach fresh'],
            'lechuga': ['lechuga fresca', 'lechuga', 'lettuce fresh'],
            'pepino': ['pepino fresco', 'pepino', 'cucumber fresh'],
            'pimiento': ['pimiento fresco', 'pimiento', 'pepper fresh'],
            'berenjena': ['berenjena fresca', 'berenjena', 'eggplant fresh'],
            'apio': ['apio fresco', 'apio', 'celery fresh'],
            'col': ['col fresca', 'col', 'cabbage fresh'],
            'coliflor': ['coliflor fresca', 'coliflor', 'cauliflower fresh'],
            
            # === FRUTAS FRESCAS ===
            'manzana': ['manzana fresca', 'manzana', 'apple fresh'],
            'manzanas': ['manzana fresca', 'manzana'],
            'plátano': ['plátano fresco', 'plátano', 'banana fresh'],
            'plátanos': ['plátano fresco', 'plátano'],
            'naranja': ['naranja fresca', 'naranja', 'orange fresh'],
            'naranjas': ['naranja fresca', 'naranja'],
            'pera': ['pera fresca', 'pera', 'pear fresh'],
            'peras': ['pera fresca', 'pera'],
            'fresa': ['fresas frescas', 'fresas', 'strawberry fresh'],
            'fresas': ['fresas frescas', 'fresas'],
            'uva': ['uvas frescas', 'uvas', 'grape fresh'],
            'uvas': ['uvas frescas', 'uvas'],
            'kiwi': ['kiwi fresco', 'kiwi'],
            'piña': ['piña fresca', 'piña', 'pineapple fresh'],
            'melón': ['melón fresco', 'melón', 'melon fresh'],
            'sandía': ['sandía fresca', 'sandía', 'watermelon fresh'],
            'aguacate': ['aguacate fresco', 'aguacate', 'avocado fresh'],
            'limón': ['limón fresco', 'limón', 'lemon fresh'],
            
            # === LEGUMBRES ===
            'lentejas': ['lentejas', 'lentils'],
            'garbanzos': ['garbanzos', 'chickpeas'],
            'alubias': ['alubias', 'beans'],
            'judías': ['judías', 'beans'],
            
            # === FRUTOS SECOS ===
            'almendras': ['almendras', 'almonds'],
            'nueces': ['nueces', 'walnuts'],
            'pistachos': ['pistachos', 'pistachios'],
            'cacahuetes': ['cacahuetes', 'peanuts'],
            
            # === ACEITES Y GRASAS ===
            'aceite': ['aceite oliva', 'aceite'],
            'oliva': ['aceitunas', 'oliva']
        }
        
        # Si tenemos búsquedas específicas para este alimento
        if food_lower in progressive_searches:
            search_terms = progressive_searches[food_lower]
        else:
            # Para otros alimentos, usar el término original
            search_terms = [food]
        
        print(f"🔍 Estrategia de búsqueda para '{food}': {search_terms}")
        return search_terms
    
    def _is_fresh_food(self, food: str) -> bool:
        """Determinar si un alimento es fresco (verdura/fruta)"""
        fresh_foods = {
            'brócoli', 'tomate', 'cebolla', 'zanahoria', 'calabacín', 'espárragos',
            'espinacas', 'lechuga', 'pepino', 'pimiento', 'berenjena', 'apio',
            'col', 'coliflor', 'manzana', 'plátano', 'naranja', 'pera', 'fresa',
            'uva', 'kiwi', 'piña', 'melón', 'sandía', 'aguacate', 'limón',
            'patata', 'papa', 'patatas'
        }
        return food.lower().strip() in fresh_foods
    
    def _safe_float(self, value) -> float:
        """Convertir valor a float de forma segura"""
        if value is None:
            return 0.0
        try:
            return float(value)
        except (ValueError, TypeError):
            return 0.0
    
    def _filter_and_prioritize_products_advanced(self, products: List[Dict], original_search: str, is_fresh: bool = False) -> List[Dict]:
        """Filtrar y priorizar productos con scoring avanzado"""
        if not products:
            return []
        
        search_lower = original_search.lower()
        scored_products = []
        
        for product in products:
            score = self._calculate_product_score(product, search_lower, is_fresh)
            if score > 0:  # Solo productos con score positivo
                scored_products.append((product, score))
        
        # Ordenar por score descendente
        scored_products.sort(key=lambda x: x[1], reverse=True)
        
        # Extraer solo los productos
        filtered_products = [product for product, score in scored_products]
        
        print(f"🔍 Productos filtrados y puntuados: {len(filtered_products)} de {len(products)} originales")
        if filtered_products:
            best_score = scored_products[0][1]
            print(f"   🏆 Mejor puntuación: {best_score:.1f}")
        
        return filtered_products
    
    def _calculate_product_score(self, product: Dict, search_term: str, is_fresh: bool) -> float:
        """Calcular puntuación de relevancia para un producto"""
        score = 0.0
        
        product_name = product.get('product_name_es', product.get('product_name', '')).lower()
        categories = product.get('categories_tags', [])
        labels = product.get('labels_tags', [])
        
        # Score base: contiene el término de búsqueda
        if search_term in product_name:
            score += 10.0
        elif any(word in product_name for word in search_term.split()):
            score += 5.0
        else:
            return 0.0  # Sin relevancia básica
        
        # Bonus por palabras clave de calidad
        quality_keywords = ['fresco', 'crudo', 'natural', 'orgánico', 'bio', 'ecológico']
        for keyword in quality_keywords:
            if keyword in product_name:
                score += 3.0
            if any(keyword in label for label in labels):
                score += 2.0
        
        # Bonus específico para alimentos frescos
        if is_fresh:
            fresh_categories = ['vegetables', 'fresh-vegetables', 'fresh-produce', 'fruits', 'fresh-fruits']
            for category in categories:
                if any(fresh_cat in category for fresh_cat in fresh_categories):
                    score += 5.0
                    break
        
        # Penalización por procesados
        processed_keywords = ['sopa', 'caldo', 'conserva', 'enlatado', 'preparado', 'instant']
        for keyword in processed_keywords:
            if keyword in product_name:
                score -= 5.0
        
        processed_categories = ['processed', 'canned', 'frozen-ready-meals', 'instant']
        for category in categories:
            if any(proc_cat in category for proc_cat in processed_categories):
                score -= 3.0
        
        # Bonus por información nutricional completa
        nutriments = product.get('nutriments', {})
        if nutriments.get('energy-kcal_100g') or nutriments.get('energy_100g'):
            score += 1.0
        if nutriments.get('proteins_100g'):
            score += 1.0
        
        # Penalización si no tiene información nutricional
        if not (nutriments.get('energy-kcal_100g') or nutriments.get('energy_100g') or nutriments.get('energy-kj_100g')):
            return 0.0
        
        return max(0.0, score)
    
    def _show_product_options(self, products: List[Dict], search_term: str, grams: float) -> Dict:
        """Devolver opciones estructuradas para que el usuario pueda elegir"""
        print(f"\n🔍 Se encontraron {len(products)} productos para '{search_term}':")
        
        options = []
        for i, product in enumerate(products, 1):
            name = product.get('product_name_es', product.get('product_name', 'Sin nombre'))
            brand = product.get('brands', 'Sin marca')
            
            # Obtener información nutricional básica
            nutriments = product.get('nutriments', {})
            calories_per_100g = (
                nutriments.get('energy-kcal_100g') or 
                nutriments.get('energy_100g') or 
                (nutriments.get('energy-kj_100g', 0) / 4.184) or 
                0
            )
            
            option_info = {
                'number': i,
                'name': name,
                'brand': brand,
                'calories_per_100g': round(calories_per_100g),
                'product': product,
                'display_name': f"{name} ({brand}) - {round(calories_per_100g)} cal/100g"
            }
            options.append(option_info)
        
        # En lugar de lanzar error, devolver estructura especial para múltiples opciones
        return {
            'multiple_options': True,
            'search_term': search_term,
            'grams': grams,
            'options': options
        }
    
    def get_nutrition_from_selected_option(self, option_data: Dict, selected_index: int) -> Dict:
        """Obtener nutrición del producto seleccionado por el usuario"""
        try:
            if selected_index < 0 or selected_index >= len(option_data['options']):
                raise ValueError("Índice de selección inválido")
            
            selected_option = option_data['options'][selected_index]
            selected_product = selected_option['product']
            grams = option_data['grams']
            
            # Extraer información nutricional del producto seleccionado
            nutrition_data = self._extract_nutrition_data(selected_product, grams)
            
            print(f"✅ Producto seleccionado: {selected_option['display_name']}")
            print(f"✅ Nutrición: {nutrition_data['calories']} cal, {nutrition_data['proteins']}g proteína")
            
            return nutrition_data
            
        except Exception as e:
            print(f"❌ Error procesando selección: {e}")
            raise ValueError(f"Error procesando la opción seleccionada: {str(e)}")
    
    def _extract_nutrition_data(self, product: Dict, grams: float) -> Dict:
        """Extraer datos nutricionales de un producto de Open Food Facts"""
        try:
            # Obtener información nutricional por 100g
            nutriments = product.get('nutriments', {})
            
            # Calorías por 100g (prioridad: energy-kcal_100g, energy_100g, energy-kj_100g)
            calories_per_100g = self._safe_float(
                nutriments.get('energy-kcal_100g') or 
                nutriments.get('energy_100g') or 
                (self._safe_float(nutriments.get('energy-kj_100g', 0)) / 4.184) or
                0
            )
            
            # Proteínas por 100g
            proteins_per_100g = self._safe_float(nutriments.get('proteins_100g', 0))
            
            # Carbohidratos por 100g
            carbs_per_100g = self._safe_float(nutriments.get('carbohydrates_100g', 0))
            
            # Grasas por 100g
            fats_per_100g = self._safe_float(nutriments.get('fat_100g', 0))
            
            # Calcular valores para la cantidad especificada
            multiplier = grams / 100
            
            return {
                'calories': round(calories_per_100g * multiplier),
                'proteins': round(proteins_per_100g * multiplier, 1),
                'carbs': round(carbs_per_100g * multiplier, 1),
                'fats': round(fats_per_100g * multiplier, 1),
                'product_name': product.get('product_name_es', product.get('product_name', 'Producto')),
                'brand': product.get('brands', 'Sin marca'),
                'barcode': product.get('code', 'Sin código'),
                'image_url': product.get('image_url', ''),
                'nutrition_grade': product.get('nutrition_grade_fr', 'Sin calificación')
            }
            
        except Exception as e:
            print(f"❌ Error extrayendo datos nutricionales: {e}")
            raise ValueError(f"❌ Error procesando información nutricional del producto: {str(e)}")
    
    def search_food(self, query: str) -> List[Dict]:
        """Buscar alimentos en Open Food Facts"""
        try:
            search_params = {
                'search_terms': query,
                'search_simple': 1,
                'page_size': 10
            }
            
            api_response = self._make_api_request(search_params)
            
            if api_response and 'products' in api_response:
                results = []
                for product in api_response['products']:
                    if product.get('product_name_es') or product.get('product_name'):
                        results.append({
                            'name': product.get('product_name_es', product.get('product_name', 'Sin nombre')),
                            'brand': product.get('brands', 'Sin marca'),
                            'barcode': product.get('code', 'Sin código'),
                            'image_url': product.get('image_url', ''),
                            'nutrition_grade': product.get('nutrition_grade_fr', 'Sin calificación')
                        })
                
                print(f"🔍 Búsqueda completada: {len(results)} productos encontrados")
                return results[:5]  # Máximo 5 resultados
            
            return []
            
        except Exception as e:
            print(f"❌ Error en búsqueda: {e}")
            return []
    
    def get_food_suggestions(self, query: str) -> List[str]:
        """Obtener sugerencias de nombres de alimentos"""
        try:
            search_results = self.search_food(query)
            suggestions = [result['name'] for result in search_results]
            return suggestions
            
        except Exception as e:
            print(f"❌ Error obteniendo sugerencias: {e}")
            return []
    
    def get_product_by_barcode(self, barcode: str) -> Optional[Dict]:
        """Obtener información de un producto por código de barras"""
        try:
            search_params = {
                'code': barcode,
                'json': 1
            }
            
            api_response = self._make_api_request(search_params)
            
            if api_response and 'products' in api_response and api_response['products']:
                product = api_response['products'][0]
                return {
                    'name': product.get('product_name_es', product.get('product_name', 'Sin nombre')),
                    'brand': product.get('brands', 'Sin marca'),
                    'barcode': product.get('code', 'Sin código'),
                    'image_url': product.get('image_url', ''),
                    'nutrition_grade': product.get('nutrition_grade_fr', 'Sin calificación'),
                    'ingredients': product.get('ingredients_text_es', product.get('ingredients_text', 'Sin ingredientes')),
                    'allergens': product.get('allergens_tags', []),
                    'additives': product.get('additives_tags', [])
                }
            
            return None
            
        except Exception as e:
            print(f"❌ Error obteniendo producto por código de barras: {e}")
            return None
