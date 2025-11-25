import bcrypt
from models.user_model import get_all_users, get_user_by_id, create_user, update_user, delete_user

def get_all_users_service():
    return get_all_users()

def get_user_by_id_service(user_id):
    return get_user_by_id(user_id)

def create_user_service(full_name, username, password, role):
    # Hash password
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return create_user(full_name, username, hashed.decode(), role)

def update_user_service(user_id, full_name, username, role):
    # Check if username is unique except for this user
    users = get_all_users()
    for u in users:
        if u['username'] == username and u['user_id'] != user_id:
            raise ValueError("Username already exists")
    return update_user(user_id, full_name, username, role)

def delete_user_service(user_id):
    # Maybe add check if user is referenced elsewhere, but for now simple
    return delete_user(user_id)

def display_user(user):
    if user:
        print(f"ID: {user['user_id']}")
        print(f"Full Name: {user['full_name']}")
        print(f"Username: {user['username']}")
        print(f"Role: {user['role']}")
        print(f"Created At: {user['created_at']}")
    else:
        print("User not found.")

def display_users(users):
    if not users:
        print("No users found.")
        return
    print("Users:")
    for user in users:
        print(f"ID: {user['user_id']}, Name: {user['full_name']}, Username: {user['username']}, Role: {user['role']}")
