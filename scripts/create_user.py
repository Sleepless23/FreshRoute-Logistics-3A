import sys
import bcrypt
from database.connection import get_connection
sys.dont_write_bytecode = True

def create_user():
    print("=== CREATE NEW USER ===")
    full_name = input("Full Name: ")
    username = input("Username: ")
    
    import getpass
    password = getpass.getpass("Password: ")
    confirm_password = getpass.getpass("Confirm Password: ")
    
    if password != confirm_password:
        print("Passwords do not match! Exiting.")
        return
    
    role = input("Role (admin/dispatcher/driver/manager): ").lower()
    if role not in ["admin", "dispatcher", "driver", "manager"]:
        print("Invalid role! Exiting.")
        return
    
    # Hash the password
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    
    # Insert into database
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (full_name, username, password_hash, role) VALUES (%s,%s,%s,%s)",
            (full_name, username, hashed.decode(), role)
        )
        conn.commit()
        print(f"User '{username}' created successfully!")
    except Exception as e:
        print("Error creating user:", e)
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    create_user()
