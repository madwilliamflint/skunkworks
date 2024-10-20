#!python

# > write a python script that implements a multi-level command line menu through a dispatch table.

import cmd

class SubMenu(cmd.Cmd):
    prompt = '(submenu) '

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
