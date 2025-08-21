# Limen - Servicio de Deportes
# =====================================
# Este archivo calcula calorías quemadas en actividades deportivas

import config
from typing import Dict, List, Optional, Tuple

class TrainingService:
    """Servicio para calcular calorías quemadas en actividades deportivas"""
    
    def __init__(self):
        """Inicializar el servicio de deportes"""
        # Base de datos local de deportes y ejercicios con METs reales (SOLO EN ESPAÑOL)
        self.sports_database = {
            # DEPORTES DE EQUIPO
            'fútbol': {'name': 'Fútbol', 'met': 8.0, 'category': 'deporte_equipo'},
            'baloncesto': {'name': 'Baloncesto', 'met': 8.0, 'category': 'deporte_equipo'},
            'tenis': {'name': 'Tenis', 'met': 7.0, 'category': 'deporte_raqueta'},
            'voleibol': {'name': 'Voleibol', 'met': 4.0, 'category': 'deporte_equipo'},
            'bádminton': {'name': 'Bádminton', 'met': 5.5, 'category': 'deporte_raqueta'},
            'hockey': {'name': 'Hockey', 'met': 8.0, 'category': 'deporte_equipo'},
            'rugby': {'name': 'Rugby', 'met': 10.0, 'category': 'deporte_equipo'},
            'béisbol': {'name': 'Béisbol', 'met': 5.0, 'category': 'deporte_equipo'},
            'balonmano': {'name': 'Balonmano', 'met': 8.0, 'category': 'deporte_equipo'},
            'cricket': {'name': 'Cricket', 'met': 5.0, 'category': 'deporte_equipo'},
            'pádel': {'name': 'Pádel', 'met': 6.0, 'category': 'deporte_raqueta'},
            
            # DEPORTES ACUÁTICOS
            'natación': {'name': 'Natación', 'met': 7.0, 'category': 'deporte_acuatico'},
            'waterpolo': {'name': 'Waterpolo', 'met': 10.0, 'category': 'deporte_acuatico'},
            'remo': {'name': 'Remo', 'met': 7.0, 'category': 'deporte_acuatico'},
            'surf': {'name': 'Surf', 'met': 3.0, 'category': 'deporte_acuatico'},
            'buceo': {'name': 'Buceo', 'met': 5.0, 'category': 'deporte_acuatico'},
            'kayak': {'name': 'Kayak', 'met': 5.0, 'category': 'deporte_acuatico'},
            'piragüismo': {'name': 'Piragüismo', 'met': 6.0, 'category': 'deporte_acuatico'},
            'vela': {'name': 'Vela', 'met': 3.0, 'category': 'deporte_acuatico'},
            
            # DEPORTES DE INVIERNO
            'esquí': {'name': 'Esquí', 'met': 7.0, 'category': 'deporte_invierno'},
            'esquí_alpino': {'name': 'Esquí Alpino', 'met': 8.0, 'category': 'deporte_invierno'},
            'esquí_nórdico': {'name': 'Esquí Nórdico', 'met': 9.0, 'category': 'deporte_invierno'},
            'snowboard': {'name': 'Snowboard', 'met': 5.0, 'category': 'deporte_invierno'},
            'patinaje': {'name': 'Patinaje', 'met': 5.5, 'category': 'deporte_invierno'},
            'patinaje_hielo': {'name': 'Patinaje sobre Hielo', 'met': 6.0, 'category': 'deporte_invierno'},
            'patinaje_artístico': {'name': 'Patinaje Artístico', 'met': 6.5, 'category': 'deporte_invierno'},
            'curling': {'name': 'Curling', 'met': 4.0, 'category': 'deporte_invierno'},
            'bobsleigh': {'name': 'Bobsleigh', 'met': 6.0, 'category': 'deporte_invierno'},
            'luge': {'name': 'Luge', 'met': 5.0, 'category': 'deporte_invierno'},
            
            # DEPORTES DE COMBATE
            'boxeo': {'name': 'Boxeo', 'met': 12.0, 'category': 'deporte_combate'},
            'kick_boxeo': {'name': 'Kick Boxeo', 'met': 10.0, 'category': 'deporte_combate'},
            'karate': {'name': 'Karate', 'met': 8.0, 'category': 'deporte_combate'},
            'taekwondo': {'name': 'Taekwondo', 'met': 9.0, 'category': 'deporte_combate'},
            'judo': {'name': 'Judo', 'met': 8.0, 'category': 'deporte_combate'},
            'mma': {'name': 'MMA', 'met': 11.0, 'category': 'deporte_combate'},
            'muay_thai': {'name': 'Muay Thai', 'met': 10.0, 'category': 'deporte_combate'},
            'kung_fu': {'name': 'Kung Fu', 'met': 8.0, 'category': 'deporte_combate'},
            'aikido': {'name': 'Aikido', 'met': 6.0, 'category': 'deporte_combate'},
            'capoeira': {'name': 'Capoeira', 'met': 8.0, 'category': 'deporte_combate'},
            'esgrima': {'name': 'Esgrima', 'met': 6.0, 'category': 'deporte_combate'},
            'lucha_libre': {'name': 'Lucha Libre', 'met': 9.0, 'category': 'deporte_combate'},
            
            # DEPORTES DE RESISTENCIA
            'correr': {'name': 'Correr', 'met': 8.0, 'category': 'deporte_resistencia'},
            'maratón': {'name': 'Maratón', 'met': 9.0, 'category': 'deporte_resistencia'},
            'media_maratón': {'name': 'Media Maratón', 'met': 8.5, 'category': 'deporte_resistencia'},
            'ciclismo': {'name': 'Ciclismo', 'met': 6.0, 'category': 'deporte_resistencia'},
            'ciclismo_montaña': {'name': 'Ciclismo de Montaña', 'met': 8.0, 'category': 'deporte_resistencia'},
            'ciclismo_ruta': {'name': 'Ciclismo de Ruta', 'met': 7.0, 'category': 'deporte_resistencia'},
            'triatlón': {'name': 'Triatlón', 'met': 10.0, 'category': 'deporte_resistencia'},
            'duatlón': {'name': 'Duatlón', 'met': 9.0, 'category': 'deporte_resistencia'},
            'ultramaratón': {'name': 'Ultramaratón', 'met': 9.5, 'category': 'deporte_resistencia'},
            
            # DEPORTES DE FUERZA
            'halterofilia': {'name': 'Halterofilia', 'met': 6.0, 'category': 'deporte_fuerza'},
            'powerlifting': {'name': 'Powerlifting', 'met': 6.0, 'category': 'deporte_fuerza'},
            'crossfit': {'name': 'CrossFit', 'met': 10.0, 'category': 'deporte_fuerza'},
            'calistenia': {'name': 'Calistenia', 'met': 8.0, 'category': 'deporte_fuerza'},
            'bodybuilding': {'name': 'Bodybuilding', 'met': 5.0, 'category': 'deporte_fuerza'},
            'musculación': {'name': 'Musculación', 'met': 5.0, 'category': 'deporte_fuerza'},
            'strongman': {'name': 'Strongman', 'met': 7.0, 'category': 'deporte_fuerza'},
            'levantamiento_pesas': {'name': 'Levantamiento de Pesas', 'met': 6.0, 'category': 'deporte_fuerza'},
            
            # DEPORTES DE AVENTURA
            'escalada': {'name': 'Escalada', 'met': 8.0, 'category': 'deporte_aventura'},
            'escalada_roca': {'name': 'Escalada en Roca', 'met': 8.5, 'category': 'deporte_aventura'},
            'escalada_muro': {'name': 'Escalada en Muro', 'met': 7.5, 'category': 'deporte_aventura'},
            'senderismo': {'name': 'Senderismo', 'met': 6.0, 'category': 'deporte_aventura'},
            'montañismo': {'name': 'Montañismo', 'met': 7.0, 'category': 'deporte_aventura'},
            'parkour': {'name': 'Parkour', 'met': 9.0, 'category': 'deporte_aventura'},
            'trekking': {'name': 'Trekking', 'met': 6.5, 'category': 'deporte_aventura'},
            'orientación': {'name': 'Orientación', 'met': 7.0, 'category': 'deporte_aventura'},
            'rafting': {'name': 'Rafting', 'met': 8.0, 'category': 'deporte_aventura'},
            'parapente': {'name': 'Parapente', 'met': 3.0, 'category': 'deporte_aventura'},
            'bungee_jumping': {'name': 'Bungee Jumping', 'met': 4.0, 'category': 'deporte_aventura'},
            
            # DEPORTES DE BAILE
            'baile': {'name': 'Baile', 'met': 5.0, 'category': 'deporte_baile'},
            'zumba': {'name': 'Zumba', 'met': 8.0, 'category': 'deporte_baile'},
            'salsa': {'name': 'Salsa', 'met': 6.0, 'category': 'deporte_baile'},
            'bachata': {'name': 'Bachata', 'met': 6.0, 'category': 'deporte_baile'},
            'merengue': {'name': 'Merengue', 'met': 6.0, 'category': 'deporte_baile'},
            'tango': {'name': 'Tango', 'met': 5.5, 'category': 'deporte_baile'},
            'flamenco': {'name': 'Flamenco', 'met': 7.0, 'category': 'deporte_baile'},
            'ballet': {'name': 'Ballet', 'met': 6.0, 'category': 'deporte_baile'},
            'contemporáneo': {'name': 'Danza Contemporánea', 'met': 6.5, 'category': 'deporte_baile'},
            'hip_hop': {'name': 'Hip Hop', 'met': 7.0, 'category': 'deporte_baile'},
            'breakdance': {'name': 'Breakdance', 'met': 8.0, 'category': 'deporte_baile'},
            'jazz': {'name': 'Jazz Dance', 'met': 6.0, 'category': 'deporte_baile'},
            'tap': {'name': 'Tap Dance', 'met': 6.5, 'category': 'deporte_baile'},
            
            # DEPORTES DE PRECISIÓN
            'golf': {'name': 'Golf', 'met': 3.0, 'category': 'deporte_precision'},
            'tiro_arco': {'name': 'Tiro con Arco', 'met': 3.0, 'category': 'deporte_precision'},
            'billar': {'name': 'Billar', 'met': 2.5, 'category': 'deporte_precision'},
            'snooker': {'name': 'Snooker', 'met': 2.5, 'category': 'deporte_precision'},
            'dardos': {'name': 'Dardos', 'met': 2.0, 'category': 'deporte_precision'},
            'petanca': {'name': 'Petanca', 'met': 2.5, 'category': 'deporte_precision'},
            'bolos': {'name': 'Bolos', 'met': 3.0, 'category': 'deporte_precision'},
            'tiro_deportivo': {'name': 'Tiro Deportivo', 'met': 2.5, 'category': 'deporte_precision'},
            
            # ACTIVIDADES FITNESS
            'yoga': {'name': 'Yoga', 'met': 2.5, 'category': 'fitness'},
            'pilates': {'name': 'Pilates', 'met': 3.0, 'category': 'fitness'},
            'spinning': {'name': 'Spinning', 'met': 8.0, 'category': 'fitness'},
            'aeróbic': {'name': 'Aeróbic', 'met': 7.0, 'category': 'fitness'},
            'step': {'name': 'Step', 'met': 6.0, 'category': 'fitness'},
            'body_pump': {'name': 'Body Pump', 'met': 7.0, 'category': 'fitness'},
            'body_combat': {'name': 'Body Combat', 'met': 8.0, 'category': 'fitness'},
            'body_balance': {'name': 'Body Balance', 'met': 4.0, 'category': 'fitness'},
            'body_attack': {'name': 'Body Attack', 'met': 9.0, 'category': 'fitness'},
            'body_vive': {'name': 'Body Vive', 'met': 5.0, 'category': 'fitness'},
            'body_jam': {'name': 'Body Jam', 'met': 7.0, 'category': 'fitness'},
            'body_step': {'name': 'Body Step', 'met': 7.0, 'category': 'fitness'},
            'body_flow': {'name': 'Body Flow', 'met': 4.0, 'category': 'fitness'},
            'body_core': {'name': 'Body Core', 'met': 6.0, 'category': 'fitness'},
            
            # EJERCICIOS ESPECÍFICOS
            'sentadillas': {'name': 'Sentadillas', 'met': 8.0, 'category': 'ejercicio_fuerza'},
            'flexiones': {'name': 'Flexiones', 'met': 8.0, 'category': 'ejercicio_fuerza'},
            'dominadas': {'name': 'Dominadas', 'met': 8.0, 'category': 'ejercicio_fuerza'},
            'plancha': {'name': 'Plancha', 'met': 4.0, 'category': 'ejercicio_fuerza'},
            'flexiones_brazos': {'name': 'Flexiones de Brazos', 'met': 8.0, 'category': 'ejercicio_fuerza'},
            'dominadas_barra': {'name': 'Dominadas en Barra', 'met': 8.0, 'category': 'ejercicio_fuerza'},
            'burpees': {'name': 'Burpees', 'met': 10.0, 'category': 'ejercicio_fuerza'},
            'escaladores_montaña': {'name': 'Escaladores de Montaña', 'met': 8.0, 'category': 'ejercicio_fuerza'},
            'zancadas': {'name': 'Zancadas', 'met': 7.0, 'category': 'ejercicio_fuerza'},
            'peso_muerto': {'name': 'Peso Muerto', 'met': 6.0, 'category': 'ejercicio_fuerza'},
            'press_banca': {'name': 'Press de Banca', 'met': 6.0, 'category': 'ejercicio_fuerza'},
            'press_militar': {'name': 'Press Militar', 'met': 6.0, 'category': 'ejercicio_fuerza'},
            'curl_biceps': {'name': 'Curl de Bíceps', 'met': 5.0, 'category': 'ejercicio_fuerza'},
            'extension_triceps': {'name': 'Extensión de Tríceps', 'met': 5.0, 'category': 'ejercicio_fuerza'},
            
            # ACTIVIDADES DIARIAS
            'caminar': {'name': 'Caminar', 'met': 3.5, 'category': 'actividad_diaria'},
            
            # DEPORTES EXTREMOS
            'paracaidismo': {'name': 'Paracaidismo', 'met': 3.0, 'category': 'deporte_extremo'},
            'escalada_libre': {'name': 'Escalada Libre', 'met': 9.0, 'category': 'deporte_extremo'},
            'base_jumping': {'name': 'Base Jumping', 'met': 4.0, 'category': 'deporte_extremo'},
            'esquí_extremo': {'name': 'Esquí Extremo', 'met': 9.0, 'category': 'deporte_extremo'},
            'snowboard_extremo': {'name': 'Snowboard Extremo', 'met': 8.0, 'category': 'deporte_extremo'},
            
            # DEPORTES MOTORIZADOS
            'motocross': {'name': 'Motocross', 'met': 4.0, 'category': 'deporte_motor'},
            'karting': {'name': 'Karting', 'met': 3.0, 'category': 'deporte_motor'},
            'rally': {'name': 'Rally', 'met': 3.5, 'category': 'deporte_motor'},
            
            # DEPORTES TRADICIONALES
            'pelota_vasca': {'name': 'Pelota Vasca', 'met': 8.0, 'category': 'deporte_tradicional'},
            'lucha_canaria': {'name': 'Lucha Canaria', 'met': 7.0, 'category': 'deporte_tradicional'},
            'juego_del_palo': {'name': 'Juego del Palo', 'met': 6.0, 'category': 'deporte_tradicional'},
            
            # DEPORTES ACUÁTICOS EXTREMOS
            'surf_extremo': {'name': 'Surf Extremo', 'met': 8.0, 'category': 'deporte_acuatico_extremo'},
            'wakeboard': {'name': 'Wakeboard', 'met': 7.0, 'category': 'deporte_acuatico_extremo'},
            'esquí_acuático': {'name': 'Esquí Acuático', 'met': 6.0, 'category': 'deporte_acuatico_extremo'},
            
            # DEPORTES DE INVIERNO EXTREMOS
            'esquí_acrobático': {'name': 'Esquí Acrobático', 'met': 8.0, 'category': 'deporte_invierno_extremo'},
            'snowboard_acrobático': {'name': 'Snowboard Acrobático', 'met': 8.0, 'category': 'deporte_invierno_extremo'},
        }
        
        print(f"🏃‍♂️ Base de deportes cargada: {len(self.sports_database)} actividades disponibles")
    
    def get_calories_burned(self, activity: str, minutes: int, weight: float = 70.0) -> int:
        """Calcular calorías quemadas en deportes"""
        activity_lower = activity.lower().strip()
        
        # Buscar en la base de deportes
        if activity_lower in self.sports_database:
            sport_data = self.sports_database[activity_lower]
            met_value = sport_data['met']
            sport_name = sport_data['name']
            category = sport_data['category']
            
            # Calcular calorías: MET × Peso (kg) × Tiempo (horas)
            calories_per_hour = met_value * weight
            calories_per_minute = calories_per_hour / 60
            total_calories = round(calories_per_minute * minutes)
            
            print(f"✅ Deporte encontrado: {sport_name} ({category})")
            print(f"🔥 Calorías calculadas: {total_calories} cal (MET: {met_value}, {minutes} min, {weight} kg)")
            return total_calories
        
        # Si no se encuentra, sugerir deportes similares
        suggestions = self._find_similar_sports(activity_lower)
        if suggestions:
            raise ValueError(f"'{activity}' no encontrado. ¿Te refieres a: {', '.join(suggestions[:3])}?")
        else:
            raise ValueError(f"'{activity}' no encontrado. Prueba con: fútbol, correr, yoga, boxeo, etc.")
    
    def _find_similar_sports(self, query: str) -> List[str]:
        """Encontrar deportes similares"""
        suggestions = []
        query_words = query.split()
        
        for sport_name, sport_data in self.sports_database.items():
            # Buscar coincidencias por palabras
            for word in query_words:
                if len(word) > 2 and word in sport_name:
                    suggestions.append(sport_data['name'])
                    break
        
        return suggestions
    
    def get_sport_categories(self) -> Dict[str, List[str]]:
        """Obtener deportes organizados por categorías"""
        categories = {}
        
        for sport_name, sport_data in self.sports_database.items():
            category = sport_data['category']
            if category not in categories:
                categories[category] = []
            categories[category].append(sport_data['name'])
        
        return categories
    
    def search_sports(self, query: str) -> List[Dict]:
        """Buscar deportes por consulta"""
        results = []
        query_lower = query.lower()
        
        # Si no hay query, devolver todos los deportes
        if not query or query.strip() == "":
            return self.get_all_sports()
        
        for sport_name, sport_data in self.sports_database.items():
            if (query_lower in sport_name or 
                query_lower in sport_data['name'].lower() or
                query_lower in sport_data['category']):
                results.append({
                    'key': sport_name,
                    'name': sport_data['name'],
                    'category': sport_data['category'],
                    'met': sport_data['met']
                })
        
        return results
    
    def get_all_sports(self) -> List[Dict]:
        """Obtener todos los deportes disponibles"""
        results = []
        for sport_name, sport_data in self.sports_database.items():
            results.append({
                'key': sport_name,
                'name': sport_data['name'],
                'category': sport_data['category'],
                'met': sport_data['met']
            })
        return results
    
    # ========================================
    # MÉTODOS DE VALIDACIÓN (RESPETANDO MVC)
    # ========================================
    
    def validate_training_input(self, minutes_input: str, selected_sport: str) -> Dict:
        """
        Validar input de entrenamiento según el patrón MVC
        Retorna: {'valid': bool, 'minutes': Optional[int], 'error': Optional[str]}
        """
        # Validar que se haya seleccionado un deporte
        if not selected_sport:
            return {
                'valid': False,
                'minutes': None,
                'error': '❌ Por favor selecciona un deporte'
            }
        
        # Validar que se haya introducido minutos
        if not minutes_input or not minutes_input.strip():
            return {
                'valid': False,
                'minutes': None,
                'error': '❌ Debes introducir una cantidad de minutos'
            }
        
        # Validar que sea un número válido
        try:
            minutes = int(minutes_input)
        except ValueError:
            return {
                'valid': False,
                'minutes': None,
                'error': '❌ Por favor introduce un número válido'
            }
        
        # Validar rango de minutos
        if minutes < 1 or minutes > 1440:
            return {
                'valid': False,
                'minutes': None,
                'error': '❌ Los minutos deben estar entre 1 y 1440'
            }
        
        # Validar que el deporte existe en la base de datos
        if selected_sport not in self.sports_database:
            return {
                'valid': False,
                'minutes': None,
                'error': f'❌ Deporte "{selected_sport}" no encontrado'
            }
        
        # Si todo es válido
        return {
            'valid': True,
            'minutes': minutes,
            'error': None
        }
    
    def get_training_preview(self, selected_sport: str, minutes: int, user_weight: float) -> Dict:
        """
        Obtener vista previa del entrenamiento (calorías estimadas, info del deporte)
        Retorna: {'sport_info': Dict, 'estimated_calories': int, 'valid': bool}
        """
        if not selected_sport or selected_sport not in self.sports_database:
            return {'valid': False, 'error': 'Deporte no válido'}
        
        if not minutes or minutes <= 0:
            return {'valid': False, 'error': 'Minutos no válidos'}
        
        sport_data = self.sports_database[selected_sport]
        estimated_calories = round((sport_data['met'] * user_weight * minutes) / 60)
        
        return {
            'valid': True,
            'sport_info': sport_data,
            'estimated_calories': estimated_calories
        }
    
    def validate_sport_selection(self, selected_category: str, selected_sport_key: str) -> Dict:
        """
        Validar selección de deporte
        Retorna: {'valid': bool, 'selected_sport': Optional[str], 'error': Optional[str]}
        """
        if not selected_category or selected_category == '':
            return {
                'valid': False,
                'selected_sport': None,
                'error': '❌ Por favor selecciona una categoría'
            }
        
        if not selected_sport_key or selected_sport_key == '':
            return {
                'valid': False,
                'selected_sport': None,
                'error': '❌ Por favor selecciona un deporte'
            }
        
        # Obtener deportes disponibles según la categoría
        all_sports = self.get_all_sports()
        if selected_category == 'Todas':
            available_sports = all_sports
        else:
            available_sports = [sport for sport in all_sports if sport['category'] == selected_category]
        
        # Buscar el deporte seleccionado
        sport_options = {sport['name']: sport['key'] for sport in available_sports}
        if selected_sport_key in sport_options:
            return {
                'valid': True,
                'selected_sport': sport_options[selected_sport_key],
                'error': None
            }
        else:
            return {
                'valid': False,
                'selected_sport': None,
                'error': '❌ Deporte no válido para la categoría seleccionada'
            }
