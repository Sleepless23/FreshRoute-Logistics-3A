from utils.helpers import select_from_list
from auth.register_user import register_user

def menu_main(user_id, user_role, user_full_name, user_username):
    while True:
        menu_options = []
        call_menu_functions = []

        if user_role in ["admin", "dispatcher"]:
            menu_options.append("Package Management")
            menu_options.append("Route Management")
        if user_role in ["admin", "dispatcher", "driver"]:
            menu_options.append("Delivery Tracking")
        if user_role in ["admin", "dispatcher", "manager"]:
            menu_options.append("Reports")
        if user_role == "admin":
            menu_options.append("Register New User")

        choice_input = select_from_list(menu_options, "Logging out...")
                
        if choice_input is None or choice_input == 0:
            break

        for options in menu_options:
            if menu_options.index(options) + 1 == choice_input:
                print(f"You selected: {options}")
            
