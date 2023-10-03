# poetry_installer.py

import os
import subprocess

class PoetryInstaller:
    def __init__(self):
        self.poetry_installed = False
        self.current_step = 0

    def colored_step(self):
        """Generate a colored step label."""
        return f"Step {self.current_step}:"

    def install_poetry(self):
        """Install Poetry if it is not already installed."""
        # Check if Poetry is already installed
        try:
            self.poetry_installed = subprocess.call(["poetry", "--version"], stderr=subprocess.STDOUT) == 0
        except FileNotFoundError:
            self.poetry_installed = False

        if not self.poetry_installed:
            print("Installing Poetry...")
            os.system("pip3 install -q poetry 2>/dev/null --root-user-action=ignore")

        print()  # Add a line break
