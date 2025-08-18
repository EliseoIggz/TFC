from models.user_model import UserModel


class UserController:
    """Controlador para el perfil del usuario (nombre y peso)."""

    def __init__(self):
        self.user_model = UserModel()

    def get_profile(self):
        try:
            profile = self.user_model.get_profile()
            return {"success": True, "data": profile}
        except Exception as e:
            return {"success": False, "message": f"Error: {e}"}

    def save_profile(self, name: str, weight: float):
        try:
            if weight <= 0 or weight > 500:
                return {"success": False, "message": "El peso debe ser un valor válido"}
            self.user_model.upsert_profile(name.strip(), float(weight))
            return {"success": True, "message": "Perfil guardado"}
        except Exception as e:
            return {"success": False, "message": f"Error: {e}"}


