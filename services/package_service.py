# ROLE FOR: RENDEL GARCIA
from utils.helpers import select_from_list, input_string
from models.package_model import PackageModel


CATEGORIES = ['Electronics', 'Pharmacy', 'Clothing', 'Food', 'Other']


def _select_package() -> dict | None:
    packages = PackageModel.list_all()
    if not packages:
        print("No packages available.")
        return None
    options = [f"#{p['package_id']} | {p['recipient_name']} | {p['status']}" for p in packages]
    pick = select_from_list(options, "Returning...", "Back", "== Select Package ==")
    if pick is None:
        return None
    return packages[pick - 1]


def _select_route() -> dict | None:
    routes = PackageModel.list_routes()
    if not routes:
        print("No routes available.")
        return None
    options = [f"#{r['route_id']} | {r['route_name']} | {r['route_date']}" for r in routes]
    pick = select_from_list(options, "Returning...", "Back", "== Select Route ==")
    if pick is None:
        return None
    return routes[pick - 1]


def register_package():
    print("=== Register Package ===")

    sender = input_string("Sender (or 'exit' to cancel): ", exit_message="Cancelled.")
    if sender is None:
        return

    recipient_name = input_string("Recipient Name (or 'exit' to cancel): ", exit_message="Cancelled.")
    if recipient_name is None:
        return

    recipient_address = input_string("Recipient Address (or 'exit' to cancel): ", exit_message="Cancelled.")
    if recipient_address is None:
        return

    phone = input_string("Phone (or 'exit' to skip): ", exit_message="Skipping...")
    if phone is None:
        phone = None

    # Weight can be optional float
    while True:
        w = input_string("Weight in kg (or 'exit' to skip): ", exit_message="Skipping...")
        if w is None:
            weight = None
            break
        try:
            weight = float(w)
            break
        except ValueError:
            print("Please enter a valid number for weight.")

    cat_idx = select_from_list(CATEGORIES, "Skipping category...", "Skip", "== Select Category ==")
    category = CATEGORIES[cat_idx - 1] if cat_idx is not None else None

    try:
        package_id = PackageModel.create(sender, recipient_name, recipient_address, phone, weight, category)
        print(f"Package registered with ID {package_id}.")
    except Exception as e:
        print("Failed to register package:", e)


def edit_package():
    print("=== Edit Package ===")
    pkg = _select_package()
    if not pkg:
        return

    print("Leave a field blank to keep its current value.")

    sender = input_string(f"Sender [{pkg['sender']}] (or 'exit' to cancel): ", exit_message="Cancelled.")
    if sender is None:
        return
    if not sender:
        sender = pkg['sender']

    recipient_name = input_string(f"Recipient Name [{pkg['recipient_name']}] (or 'exit' to cancel): ", exit_message="Cancelled.")
    if recipient_name is None:
        return
    if not recipient_name:
        recipient_name = pkg['recipient_name']

    recipient_address = input_string(f"Recipient Address [{pkg['recipient_address']}] (or 'exit' to cancel): ", exit_message="Cancelled.")
    if recipient_address is None:
        return
    if not recipient_address:
        recipient_address = pkg['recipient_address']

    phone = input_string(f"Phone [{pkg.get('phone') or ''}] (or 'exit' to skip): ", exit_message="Skipping...")
    if phone is None:
        phone = pkg.get('phone')

    while True:
        w = input_string(f"Weight kg [{pkg.get('weight') or ''}] (or 'exit' to skip): ", exit_message="Skipping...")
        if w is None:
            weight = pkg.get('weight')
            break
        if w == '':
            weight = pkg.get('weight')
            break
        try:
            weight = float(w)
            break
        except ValueError:
            print("Please enter a valid number for weight.")

    cat_idx = select_from_list([*CATEGORIES, 'Keep Current'], "Skipping category...", "Skip", "== Select Category ==")
    if cat_idx is None or cat_idx == len(CATEGORIES) + 1:
        category = pkg.get('category')
    else:
        category = CATEGORIES[cat_idx - 1]

    try:
        PackageModel.update(pkg['package_id'], sender, recipient_name, recipient_address, phone, weight, category)
        print(f"Package #{pkg['package_id']} updated.")
    except Exception as e:
        print("Failed to update package:", e)


def delete_package():
    print("=== Delete Package ===")
    pkg = _select_package()
    if not pkg:
        return

    confirm = select_from_list(["Yes, delete"], "Cancelled.", "No", f"Confirm delete package #{pkg['package_id']}?")
    if confirm is None:
        return

    try:
        PackageModel.delete(pkg['package_id'])
        print(f"Package #{pkg['package_id']} deleted.")
    except Exception as e:
        print("Failed to delete package:", e)


def assign_package_to_route():
    print("=== Assign Package to Route ===")
    pkg = _select_package()
    if not pkg:
        return

    route = _select_route()
    if not route:
        return

    try:
        PackageModel.assign_to_route(pkg['package_id'], route['route_id'])
        print(f"Assigned package #{pkg['package_id']} to route #{route['route_id']}.")
    except Exception as e:
        print("Failed to assign package:", e)


def view_all_packages():
    print("=== All Packages ===")
    try:
        packages = PackageModel.list_all()
    except Exception as e:
        print("Failed to load packages:", e)
        return

    if not packages:
        print("No packages found.")
        return

    for p in packages:
        print(
            f"#{p['package_id']} | {p['sender']} -> {p['recipient_name']} | "
            f"Status: {p['status']} | Route: {p.get('current_route_id') or '-'} | "
            f"Weight: {p.get('weight') or '-'} | Category: {p.get('category') or '-'}"
        )