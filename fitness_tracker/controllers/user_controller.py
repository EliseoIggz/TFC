from models.user_model import UserModel
import logging
from typing import Dict

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UserController:
    """Controlador para el perfil del usuario (nombre y peso)."""

    def __init__(self):
        self.user_model = UserModel()


    def get_profile(self):
        try:
            profile = self.user_model.get_profile()
            return {"success": True, "data": profile}
        except Exception as e:
            logger.error(f"Error al obtener perfil: {e}")
            return {"success": False, "message": f"Error: {e}"}

    def save_profile(self, name: str, weight: float, objetivo: str = None):
        try:

            if weight <= 0 or weight > 500:
                logger.warning(f"Peso inválido: {weight}")
                return {"success": False, "message": "El peso debe ser un valor válido"}
            
            result = self.user_model.upsert_profile(name.strip(), float(weight), objetivo)

            return {"success": True, "message": "Perfil guardado"}
        except Exception as e:
            logger.error(f"Error al guardar perfil: {e}")
            return {"success": False, "message": f"Error: {e}"}
    
    # ========================================
    # MÉTODOS DE VALIDACIÓN Y ESTADO (RESPETANDO MVC)
    # ========================================
    
    def validate_profile_input(self, name: str, weight: float) -> Dict:
        """
        Validar input del perfil (RESPETANDO MVC)
        Retorna: {'valid': bool, 'error': Optional[str]}
        """
        if not name or not name.strip():
            return {
                'valid': False,
                'error': '❌ El nombre es requerido'
            }
        
        if weight <= 0 or weight > 500:
            return {
                'valid': False,
                'error': '❌ El peso debe estar entre 1 y 500 kg'
            }
        
        return {
            'valid': True,
            'error': None
        }
    
    def get_profile_display_data(self, profile: Dict) -> Dict:
        """
        Preparar datos del perfil para mostrar en la vista (RESPETANDO MVC)
        Retorna: {'success': bool, 'data': Dict}
        """
        try:
            if not profile:
                return {
                    'success': False,
                    'error': 'No hay perfil disponible'
                }
            
            # Formatear datos para mostrar
            display_data = {
                'name': profile.get('name', ''),
                'weight': profile.get('weight', 70.0),
                'objetivo': profile.get('objetivo', 'mantener_peso'),
                'weight_formatted': f"{profile.get('weight', 70.0)} kg",
                'objetivo_formatted': self._format_objetivo_display(profile.get('objetivo', 'mantener_peso'))
            }
            
            return {
                'success': True,
                'data': display_data
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error al preparar datos del perfil: {str(e)}'
            }
    
    def _format_objetivo_display(self, objetivo: str) -> str:
        """Formatear objetivo para mostrar en la vista"""
        objetivo_map = {
            "mantener_peso": "⚖️ Mantener peso actual",
            "perdida_grasa": "🔥 Pérdida de grasa",
            "ganancia_musculo": "💪 Ganancia de músculo",
            "resistencia_cardio": "🏃‍♂️ Resistencia y cardio",
            "fuerza_maxima": "🏋️ Fuerza máxima"
        }
        return objetivo_map.get(objetivo, objetivo)
    
    def get_objetivo_options(self) -> Dict:
        """
        Obtener opciones de objetivo formateadas (RESPETANDO MVC)
        Retorna: {'success': bool, 'data': Dict}
        """
        options = [
            "mantener_peso",
            "perdida_grasa",
            "ganancia_musculo",
            "resistencia_cardio",
            "fuerza_maxima"
        ]
        
        format_func = lambda x: self._format_objetivo_display(x)
        
        return {
            'success': True,
            'data': {
                'options': options,
                'format_func': format_func,
                'current_index': 0  # Por defecto
            }
        }


