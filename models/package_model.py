# ROLE FOR: RENDEL GARCIA
from database.connection import get_connection


class PackageModel:
    @staticmethod
    def create(sender: str, recipient_name: str, recipient_address: str, phone: str | None, weight: float | None, category: str | None) -> int:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO packages (sender, recipient_name, recipient_address, phone, weight, category)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (sender, recipient_name, recipient_address, phone, weight, category),
            )
            conn.commit()
            return cursor.lastrowid
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def update(package_id: int, sender: str, recipient_name: str, recipient_address: str, phone: str | None, weight: float | None, category: str | None) -> None:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE packages
                SET sender=%s, recipient_name=%s, recipient_address=%s, phone=%s, weight=%s, category=%s
                WHERE package_id=%s
                """,
                (sender, recipient_name, recipient_address, phone, weight, category, package_id),
            )
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def delete(package_id: int) -> None:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM packages WHERE package_id=%s", (package_id,))
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def list_all() -> list[dict]:
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT package_id, sender, recipient_name, recipient_address, phone, weight, category, status, current_route_id, created_at FROM packages ORDER BY package_id DESC"
            )
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def assign_to_route(package_id: int, route_id: int) -> None:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            # Update current_route_id and status to Out for Delivery
            cursor.execute(
                "UPDATE packages SET current_route_id=%s, status='Out for Delivery' WHERE package_id=%s",
                (route_id, package_id),
            )
            # Insert into route_packages mapping (ignore duplicates)
            try:
                cursor.execute(
                    "INSERT INTO route_packages (route_id, package_id) VALUES (%s, %s)",
                    (route_id, package_id),
                )
            except Exception:
                # Ignore if already mapped due to UNIQUE constraint
                pass
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def list_routes() -> list[dict]:
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT route_id, route_name, route_date FROM routes ORDER BY route_date DESC, route_id DESC"
            )
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()