import mysql.connector
from database.connection import get_connection

def get_all_users():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT user_id, full_name, username, role, created_at FROM users")
        users = cursor.fetchall()
        return users
    except Exception as e:
        print("Database error:", e)
        return []
    finally:
        cursor.close()
        conn.close()

def get_user_by_id(user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT user_id, full_name, username, role, created_at FROM users WHERE user_id = %s", (user_id,))
        user = cursor.fetchone()
        return user
    except Exception as e:
        print("Database error:", e)
        return None
    finally:
        cursor.close()
        conn.close()

def create_user(full_name, username, password_hash, role):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (full_name, username, password_hash, role) VALUES (%s, %s, %s, %s)",
            (full_name, username, password_hash, role)
        )
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        print("Database error:", e)
        return None
    finally:
        cursor.close()
        conn.close()

def update_user(user_id, full_name, username, role):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE users SET full_name = %s, username = %s, role = %s WHERE user_id = %s",
            (full_name, username, role, user_id)
        )
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print("Database error:", e)
        return False
    finally:
        cursor.close()
        conn.close()

def delete_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print("Database error:", e)
        return False
    finally:
        cursor.close()
