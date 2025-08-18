from datetime import datetime
from .database import Database


class UserModel:
    """Modelo para persistir el perfil del usuario (nombre y peso)"""

    def __init__(self):
        self.db = Database()
        self.conn = self.db.get_connection()

    def get_profile(self):
        """Obtener el perfil (fila única id=1)."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name, weight FROM user_profile WHERE id = 1")
        row = cursor.fetchone()
        if row:
            return {"id": row["id"], "name": row["name"] or "", "weight": row["weight"] if row["weight"] is not None else 70.0}
        return {"id": 1, "name": "", "weight": 70.0}

    def upsert_profile(self, name: str, weight: float):
        """Crear o actualizar el perfil (siempre id=1)."""
        now = datetime.now().isoformat(timespec="seconds")
        cursor = self.conn.cursor()
        # Intentar actualizar; si no existe, insertar
        cursor.execute(
            """
            UPDATE user_profile
            SET name = ?, weight = ?, updated_at = ?
            WHERE id = 1
            """,
            (name, weight, now),
        )
        if cursor.rowcount == 0:
            cursor.execute(
                """
                INSERT INTO user_profile (id, name, weight, created_at, updated_at)
                VALUES (1, ?, ?, ?, ?)
                """,
                (name, weight, now, now),
            )
        self.conn.commit()
        return {"success": True}


