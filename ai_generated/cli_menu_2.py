#!python


#> Can you alter that so that it displays the menu items?

import cmd



class SubMenu(cmd.Cmd):
    prompt = '(submenu) '

    def preloop(self):
        """Display the submenu items"""
        print("Submenu:")
        print("1. subcommand1 - Execute subcommand1")
        print("2. subcommand2 - Execute subcommand2")
        print("3. back - Go back to the main menu")
        print("4. exit - Exit the program")

    def do_subcommand1(self, args):
        """Execute subcommand1"""
        print("Subcommand1 executed")

    def do_subcommand2(self, args):
        """Execute subcommand2"""
        print("Subcommand2 executed")

    def do_back(self, args):
        """Go back to the main menu"""
        return True

    def do_exit(self, args):
        """Exit the program"""
        return True

class MainMenu(cmd.Cmd):
    prompt = '(mainmenu) '

    def preloop(self):
        """Display the main menu items"""
        print("Main Menu:")
        print("1. level1 - Execute level1 command")
        print("2. level2 - Enter submenu")
        print("3. exit - Exit the program")

    def do_level1(self, args):
        """Execute level1 command"""
        print("Level1 command executed")

    def do_level2(self, args):
        """Enter submenu"""
        submenu = SubMenu()
        submenu.cmdloop()

    def do_exit(self, args):
        """Exit the program"""
        return True

if __name__ == '__main__':
    main_menu = MainMenu()
    main_menu.cmdloop()
