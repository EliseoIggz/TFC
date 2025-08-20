from models.user_model import UserModel
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UserController:
    """Controlador para el perfil del usuario (nombre y peso)."""

    def __init__(self):
        self.user_model = UserModel()
        # logger.info("UserController inicializado")

    def get_profile(self):
        try:
            # logger.info("Obteniendo perfil del usuario...")
            profile = self.user_model.get_profile()
            # logger.info(f"Perfil obtenido: {profile}")
            return {"success": True, "data": profile}
        except Exception as e:
            logger.error(f"Error al obtener perfil: {e}")
            return {"success": False, "message": f"Error: {e}"}

    def save_profile(self, name: str, weight: float, objetivo: str = None):
        try:
            logger.info(f"Guardando perfil - Nombre: {name}, Peso: {weight}, Objetivo: {objetivo}")
            if weight <= 0 or weight > 500:
                logger.warning(f"Peso inválido: {weight}")
                return {"success": False, "message": "El peso debe ser un valor válido"}
            
            result = self.user_model.upsert_profile(name.strip(), float(weight), objetivo)
            logger.info(f"Perfil guardado exitosamente: {result}")
            return {"success": True, "message": "Perfil guardado"}
        except Exception as e:
            logger.error(f"Error al guardar perfil: {e}")
            return {"success": False, "message": f"Error: {e}"}


