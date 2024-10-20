#!python

#> change this so it no longer uses the cmd module

def main_menu():
    while True:
        print("\nMain Menu:")
        print("1. level1 - Execute level1 command")
        print("2. level2 - Enter submenu")
        print("3. exit - Exit the program")
        choice = input("Enter your choice: ")

        if choice == '1':
            print("Level1 command executed")
        elif choice == '2':
            submenu()
        elif choice == '3':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

def submenu():
    while True:
        print("\nSubmenu:")
        print("1. subcommand1 - Execute subcommand1")
        print("2. subcommand2 - Execute subcommand2")
        print("3. back - Go back to the main menu")
        print("4. exit - Exit the program")
        choice = input("Enter your choice: ")

        if choice == '1':
            print("Subcommand1 executed")
        elif choice == '2':
            print("Subcommand2 executed")
        elif choice == '3':
            break
        elif choice == '4':
            print("Exiting the program.")
            exit()
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main_menu()
