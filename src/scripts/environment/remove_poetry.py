import os
import subprocess
import sys

class RemoveOrInstallPoetry:
    def __init__(self):
        """Initialize RemoveOrInstallPoetry class."""
        self.poetry_installed = None

    def check_poetry_installation(self):
        """Check if Poetry is installed."""
        print("Checking if Poetry is installed...")
        try:
            self.poetry_installed = subprocess.call(["poetry", "--version"], stderr=subprocess.STDOUT) == 0
        except FileNotFoundError:
            self.poetry_installed = False

    def install_poetry(self):
        """Install Poetry."""
        print("Installing Poetry...")
        os.system("curl -sSL https://install.python-poetry.org | python3 -")
        print("Poetry has been installed.")

    def remove_poetry(self):
        """Remove Poetry if it is installed."""
        if self.poetry_installed:
            print("Poetry is installed. Removing Poetry...")
            os.system("pip uninstall -y poetry")
            print("Poetry has been removed.")
        else:
            print("Poetry is not installed. Installing Poetry...")
            self.install_poetry()

    def run(self):
        """Run the script."""
        self.check_poetry_installation()
        self.remove_poetry()

if __name__ == "__main__":
    remover = RemoveOrInstallPoetry()
    remover.run()
