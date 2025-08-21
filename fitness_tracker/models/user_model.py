from datetime import datetime
from .database import Database
import logging

# Configurar logging
logger = logging.getLogger(__name__)


class UserModel:
    """Modelo para persistir el perfil del usuario (nombre y peso)"""

    def __init__(self):
        self.db = Database()
        self.conn = self.db.get_connection()


    def get_profile(self):
        """Obtener el perfil (fila única id=1)."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT id, name, weight, objetivo FROM user_profile WHERE id = 1")
            row = cursor.fetchone()
            if row:
                profile = {"id": row["id"], "name": row["name"] or "", "weight": row["weight"] if row["weight"] is not None else 70.0, "objetivo": row["objetivo"] if row["objetivo"] is not None else "mantener_peso"}

                return profile
            else:

                return {"id": 1, "name": "", "weight": 70.0, "objetivo": "mantener_peso"}
        except Exception as e:
            logger.error(f"Error al obtener perfil: {e}")
            raise

    def upsert_profile(self, name: str, weight: float, objetivo: str = None):
        """Crear o actualizar el perfil (siempre id=1)."""
        try:
            now = datetime.now().isoformat(timespec="seconds")
            cursor = self.conn.cursor()
            
            # Si no se proporciona objetivo, usar el valor por defecto
            if objetivo is None:
                objetivo = "mantener_peso"
            

            # Intentar actualizar; si no existe, insertar
            cursor.execute(
                """
                UPDATE user_profile
                SET name = ?, weight = ?, objetivo = ?, updated_at = ?
                WHERE id = 1
                """,
                (name, weight, objetivo, now),
            )
            
            if cursor.rowcount == 0:

                cursor.execute(
                    """
                    INSERT INTO user_profile (id, name, weight, objetivo, created_at, updated_at)
                    VALUES (1, ?, ?, ?, ?, ?)
                    """,
                    (name, weight, objetivo, now, now),
                )
            self.conn.commit()
            return {"success": True}
        except Exception as e:
            logger.error(f"Error al upsert perfil: {e}")
            raise


