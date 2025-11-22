import bcrypt
from database.connection import get_connection
from utils.helpers import input_string
import mysql.connector

def register_user():
    print("=== REGISTER NEW USER ===\n")

    full_name = input_string("Full Name: ", "\nRegistration cancelled.")
    if full_name is None:
        return

    import getpass

    while True:
        username = input_string("Username: ", "\nRegistration cancelled.")
        if username is None:
            return

        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT user_id FROM users WHERE username = %s", (username,))
            if cursor.fetchone():
                print(f"Error: The username '{username}' already exists. Please choose a different username.\n")
            else:
                break
        except Exception as e:
            print("Database error:", e)
            cursor.close()
            conn.close()
            return
        finally:
            cursor.close()
            conn.close()

    password = input_string("Password: ", "\nRegistration cancelled.", [], True)
    if password is None:
        return

    role = input_string(
        "Role (admin/dispatcher/driver/manager): ",
        "\nRegistration cancelled.",
        required_input=['admin', 'dispatcher', 'driver', 'manager']
    )
    if role is None:
        return

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    # Insert new user
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (full_name, username, password_hash, role) VALUES (%s,%s,%s,%s)",
            (full_name, username, hashed.decode(), role)
        )
        conn.commit()
        print(f"\nUser '{username}' registered successfully!")
    except mysql.connector.IntegrityError as e:
        if e.errno == 1062:
            print(f"Error: The username '{username}' already exists. Please try again.")
        else:
            print("Database error:", e)
    except Exception as e:
        print("Error:", e)
    finally:
        cursor.close()
        conn.close()
