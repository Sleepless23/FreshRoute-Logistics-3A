from cli.menu_main import main_menu

def run():
    while True:
        choice = main_menu()
        if choice == "1":
            pass # open package menu
        elif choice == "2":
            pass # open route menu
        elif choice == "3":
            pass # open driver menu
        elif choice == "4":
            pass # open tracking menu
        elif choice == "5":
            pass # open reports menu
        elif choice == "6":
            print("Exiting system...")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    run()
