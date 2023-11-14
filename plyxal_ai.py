import os
import sys
import tty
import termios
from src.scripts.environment.symlink_manager import SymlinkManager
from src.scripts.environment.setup_environment import SetupEnvironment
from src.scripts.environment.step_formatter import StepFormatter
from src.scripts.environment.poetry_cleaner import PoetryCleaner  # Import PoetryCleaner


class Menu:
    def __init__(self, symlink_manager):
        """
        Initialize the menu with a SymlinkManager instance and a SetupEnvironment instance.

        Args:
            symlink_manager (SymlinkManager): The SymlinkManager instance.
        """
        self.symlink_manager = symlink_manager
        self.setup_environment = SetupEnvironment()
        self.poetry_cleaner = PoetryCleaner(auto_confirm=True)  # Instantiate PoetryCleaner with auto_confirm=True
        self.step_formatter = StepFormatter()

    def display(self):
        """
        Display the menu and handle user input.
        """
        while True:
            self.print_menu()
            choice = input("Enter your choice: ")

            if choice == "1":
                self.setup_environment.run()
            elif choice == "2":
                self.poetry_cleaner.run()  # Run PoetryCleaner in step 2
            elif choice == "3":
                self.symlink_manager.create_symlinks()
            elif choice == "4":
                self.symlink_manager.remove_symlinks()
            elif choice == "5":
                print("Exiting the menu.")
                break
            else:
                print("Invalid choice. Please enter a valid option.")

    def print_menu(self):
        """
        Print the colorized menu options using the StepFormatter.
        """
        print(self.step_formatter.menu_item("PlyxalAI"))
        print(" ")
        print("Setup:")
        print(self.step_formatter.menu_item("1. Setup Environment"))
        print(" ")
        print("Utils:")
        print(self.step_formatter.menu_item("2. Clean Environment"))
        print(self.step_formatter.menu_item("3. Create Symlinks"))
        print(self.step_formatter.menu_item("4. Remove Symlinks"))
        print(' ')
        print(self.step_formatter.menu_item("5. Exit"))
        print(' ')


def main():
    current_directory = os.path.abspath('.')
    symlink_manager = SymlinkManager(current_directory)

    menu = Menu(symlink_manager)
    menu.display()


if __name__ == "__main__":
    main()
