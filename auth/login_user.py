import bcrypt
from database.connection import get_connection
from utils.helpers import input_string

def login_user():
    print("=== LOGIN ===\n")
    import getpass
    while True:
        username = input_string("Username: ", "\nLogin cancelled.")

        if username is None:
            return None, None, None, None

        password = input_string("Password: ", "\nLogin cancelled.", [], True)

        if password is None:
            return None, None, None, None

        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
            user = cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

        if user and bcrypt.checkpw(password.encode(), user['password_hash'].encode()):
            print(f"Login successful! Welcome {user['full_name']} ({user['role']})")
            return user['user_id'], user['role'], user['full_name'], user['username']
        else:
            print("Invalid username or password! (Type 'exit' to cancel)")
