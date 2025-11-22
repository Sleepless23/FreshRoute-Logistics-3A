import sys
sys.dont_write_bytecode = True
from auth.login_user import login_user
from cli.menu_main import menu_main

def run():
    print("=== FreshRoute Logistics CLI ===\n")
    user_id, role = None, None

    while not role:
        user_id, role, user_full_name, user_username = login_user()
        if role is None:
            break

    if role:
        menu_main(user_id, role, user_full_name, user_username)

if __name__ == "__main__":
    run()
