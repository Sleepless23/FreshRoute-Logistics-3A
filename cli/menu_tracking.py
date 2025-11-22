# ROLE FOR: ANGEL JARED DELA CRUZ
from services.delivery_service import (
    update_delivery_status,
    add_delivery_note,
    view_delivery_history,
)
from utils.helpers import select_from_list

def tracking_menu():
    while True:
        choice = select_from_list(
            [
                "Update Delivery Status",
                "Add Delivery Note",
                "View Delivery History",
            ],
            "Reverting to main menu...",
            "Back to Main Menu",
            "====== DELIVERY TRACKING ======",
        )

        if choice == 1:
            update_delivery_status()
        elif choice == 2:
            add_delivery_note()
        elif choice == 3:
            view_delivery_history()
        elif choice is None:
            break
