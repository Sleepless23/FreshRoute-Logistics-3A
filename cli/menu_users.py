from utils.helpers import select_from_list, input_string
from services.user_service import (
    get_all_users_service,
    get_user_by_id_service,
    create_user_service,
    update_user_service,
    delete_user_service,
    display_users,
    display_user
)

def user_menu():
    while True:
        print("=== USER MANAGEMENT ===\n")
        menu_options = ["View All Users", "View User by ID", "Add User", "Edit User", "Delete User"]
        choice_input = select_from_list(menu_options, "Returning to main menu...", "Back to Main Menu", "=== USER MANAGEMENT MENU ===")

        if choice_input is None or choice_input == 0:
            break

        if choice_input == 1:
            view_all_users()
        elif choice_input == 2:
            view_user_by_id()
        elif choice_input == 3:
            add_user()
        elif choice_input == 4:
            edit_user()
        elif choice_input == 5:
            delete_user()

def view_all_users():
    print("=== ALL USERS ===\n")
    users = get_all_users_service()
    display_users(users)

def view_user_by_id():
    print("=== VIEW USER BY ID ===\n")
    user_id_str = input("Enter User ID: ").strip()
    if not user_id_str:
        print("Invalid ID.")
        return
    try:
        user_id = int(user_id_str)
        user = get_user_by_id_service(user_id)
        display_user(user)
    except ValueError:
        print("Invalid ID format.")
        print("Invalid ID format.")

def add_user():
    print("=== ADD NEW USER ===\n")

    full_name = input_string("Full Name: ", "Cancelled.")
    if full_name is None:
        return

    username = input_string("Username: ", "Cancelled.")
    if username is None:
        return

    # Check uniqueness
    users = get_all_users_service()
    for u in users:
        if u['username'] == username:
            print("Username already exists.")
            return

    password = input_string("Password: ", "Cancelled.", [], True)
    if password is None:
        return

    confirm_password = input_string("Confirm Password: ", "Cancelled.", [], True)
    if confirm_password is None:
        return

    if password != confirm_password:
        print("Passwords do not match.")
        return

    role = input_string(
        "Role (admin/dispatcher/driver/manager): ",
        "Cancelled.",
        required_input=['admin', 'dispatcher', 'driver', 'manager']
    )
    if role is None:
        return

    success = create_user_service(full_name, username, password, role)
    if success:
        print(f"User '{username}' created successfully!")
    else:
        print("Failed to create user.")

def edit_user():
    print("=== EDIT USER ===\n")
    users = get_all_users_service()
    if not users:
        print("No users found.")
        return

    # Display users with ID, full name, username, role
    user_options = []
    for user in users:
        option = f"ID: {user['user_id']}, Full Name: {user['full_name']}, Username: {user['username']}, Role: {user['role']}"
        user_options.append(option)

    choice = select_from_list(user_options, "Cancelled.", "Cancel", "=== SELECT USER TO EDIT ===")
    if choice is None or choice == 0:
        return

    selected_user = users[choice - 1]
    user_id = selected_user['user_id']
    user = get_user_by_id_service(user_id)
    if not user:
        print("User not found.")
        return

    print(f"\n=== EDITING USER: {user['username']} ===")
    display_user(user)
    print("\n--- Edit ---")

    full_name = input_string(f"Full Name (current: {user['full_name']}): ", "Cancelled.")
    if full_name is None:
        return

    username = input_string(f"Username (current: {user['username']}): ", "Cancelled.")
    if username is None:
        return

    role = input_string(
        f"Role (current: {user['role']}): ",
        "Cancelled.",
        required_input=['admin', 'dispatcher', 'driver', 'manager']
    )
    if role is None:
        return

    try:
        success = update_user_service(user_id, full_name, username, role)
        if success:
            print("User updated successfully!")
        else:
            print("Failed to update user.")
    except ValueError as e:
        print(e)

def delete_user():
    print("=== DELETE USER ===\n")
    users = get_all_users_service()
    if not users:
        print("No users found.")
        return

    # Display users with ID, full name, username, role
    user_options = []
    for user in users:
        option = f"ID: {user['user_id']}, Full Name: {user['full_name']}, Username: {user['username']}, Role: {user['role']}"
        user_options.append(option)

    choice = select_from_list(user_options, "Cancelled.", "Cancel", "=== SELECT USER TO DELETE ===")
    if choice is None or choice == 0:
        return

    selected_user = users[choice - 1]
    user_id = selected_user['user_id']
    user = get_user_by_id_service(user_id)
    if not user:
        print("User not found.")
        return

    print(f"\n=== DELETING USER: {user['username']} ===")
    display_user(user)
    confirm = input("Are you sure you want to delete this user? (y/N): ").strip().lower()
    if confirm == 'y':
        success = delete_user_service(user_id)
        if success:
            print("User deleted successfully!")
        else:
            print("Failed to delete user.")
    else:
        print("Deletion cancelled.")
