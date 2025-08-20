# Fitness Tracker - Paquete de servicios
# =====================================
# Este paquete contiene las APIs para nutrición y deporte

from .nutrition_api import NutritionService
from .translation_service import TranslationService
from .training import TrainingService

__all__ = ['NutritionService', 'TranslationService', 'TrainingService']
