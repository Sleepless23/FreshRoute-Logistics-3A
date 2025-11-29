# ROLE FOR: John RENDEL GARCIA
from services.package_service import (
    register_package,
    edit_package,
    delete_package,
    assign_package_to_route,
    view_all_packages,
)
from utils.helpers import select_from_list

def package_menu():
    while True:
        choice = select_from_list(
            [
                "Register Package",
                "Edit Package",
                "Delete Package",
                "Assign Package to Route",
                "View All Packages",
            ],
            "Reverting to main menu...",
            "Back to Main Menu",
            "====== PACKAGE MANAGEMENT ======",
        )

        if choice == 1:
            register_package()
        elif choice == 2:
            edit_package()
        elif choice == 3:
            delete_package()
        elif choice == 4:
            assign_package_to_route()
        elif choice == 5:
            view_all_packages()
        elif choice is None:
            break