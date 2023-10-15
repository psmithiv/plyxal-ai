#!/usr/bin/env python3

# poetry_setup.py - A script for setting up a Poetry-based environment.

import os
import subprocess
import sys
import argparse
from src.scripts.environment.poetry_manager import PoetryManager
from src.scripts.environment.symlink_manager import SymlinkManager
from src.scripts.environment.step_formatter import StepFormatter  # Updated import

class SetupEnvironment:
    def __init__(self, create_symlinks=False):
        """Initializes the SetupEnvironment class."""
        self.total_steps = 5 if create_symlinks else 4  # Update total steps if symlinks are created
        self.current_step = 0  # Current step in the process
        self.python_version = None
        self.pip_version = None
        self.poetry_installed = None
        self.venv_path = None
        self.create_symlinks = create_symlinks
        self.step_formatter = StepFormatter()  # Initialize StepFormatter

    def colored_step(self):
        """Returns a colorized and formatted step information."""
        return self.step_formatter.colored_step(f"Step {self.current_step} of {self.total_steps}")

    def check_python_and_pip_versions(self):
        """Step 1: Check Python and pip versions."""
        self.current_step += 1
        print(f"{self.colored_step()} Checking Python and pip versions...")

        try:
            # Get the Python and pip versions using subprocess
            self.python_version = subprocess.check_output(["python3", "--version"], universal_newlines=True, stderr=subprocess.STDOUT).strip()

            pip_version_output = subprocess.check_output(["pip3", "--version"], universal_newlines=True, stderr=subprocess.STDOUT).strip()
            pip_version_parts = pip_version_output.split()
            if len(pip_version_parts) >= 2:
                self.pip_version = pip_version_parts[0] + ' ' + pip_version_parts[1]
        except FileNotFoundError:
            print("Error: Python or pip command not found.", file=sys.stderr)
            sys.exit(1)

        # Check if Python version meets minimum requirement
        python_version_major_minor = self.python_version.split()[1].split('.')[:2]
        minimum_python_version = "3.10".split('.')
        if python_version_major_minor < minimum_python_version:
            print(f"Error: Python version 3.10.x or higher is required. Installed version: {self.python_version}", file=sys.stderr)
            sys.exit(1)
        else:
            print(f"Python version: {self.python_version}")

        # Check if pip version meets minimum requirement
        pip_version_major_minor = self.pip_version.split()[1].split('.')[:2]
        minimum_pip_version = "23.2".split('.')
        if pip_version_major_minor < minimum_pip_version:
            print(f"Error: pip version 23.2.x or higher is required. Installed version: {self.pip_version}", file=sys.stderr)
            sys.exit(1)
        else:
            print(f"pip version: {self.pip_version}")

        print()  # Add a line break

    def install_poetry(self):
        """Step 2: Install Poetry if not already installed."""
        self.current_step += 1
        print(f"{self.colored_step()} Installing Poetry...")

        # Create an instance of PoetryInstaller
        poetry_manager = PoetryManager()

        # Call the install_poetry method
        poetry_manager.install_poetry()

    def create_poetry_environment(self):
        """Step 3: Create Poetry virtual environment and install dependencies."""
        self.current_step += 1
        print(f"{self.colored_step()} Creating Poetry virtual environment and installing dependencies...")

        # Run 'poetry install --no-cache' to create the environment and install dependencies
        os.system("poetry install --no-cache")

        # Get the Poetry venv path
        self.venv_path = subprocess.check_output(["poetry", "env", "info", "--path"], universal_newlines=True).strip()

    def create_symlinks(self):
        """Step 4: Create Symlinks for files and folders that are hidden because they start with a dot."""
        self.current_step += 1
        print(f"{self.colored_step()} Creating Symlinks...")

        # Initialize SymlinkManager with the current directory, ignore list, and quiet flag
        symlink_manager = SymlinkManager('./', ['.git', '.ipynb_checkpoints'], False)

        # Call the create_symlinks method of SymlinkManager
        symlink_manager.create_symlinks()

    def create_jupyter_kernel(self):
        """Step 5: Create Jupyter kernel for Poetry environment."""
        self.current_step += 1
        print(f"{self.colored_step()} Creating Jupyter kernel...")

        if self.venv_path:
            # Create the Jupyter kernel using the venv path
            kernel_command = f"{self.venv_path}/bin/python -m ipykernel install --user --name plyxal-ai --display-name plyxal-ai"
            os.system(kernel_command)

            print()  # Add a line break
            print(f"\033[94mCompleted:\033[0m The Poetry environment is now configured. Please switch kernels using 'Kernel -> Change Kernel...'")

    def run(self):
        """Run the setup process."""
        self.check_python_and_pip_versions()
        self.install_poetry()
        self.create_poetry_environment()
        if self.create_symlinks:
            self.create_symlinks()
        self.create_jupyter_kernel()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Setup Environment')
    parser.add_argument('--create-symlinks', action='store_true', help='Create symlinks for files and folders that are hidden because they start with a .')
    args = parser.parse_args()

    config = SetupEnvironment(args.create_symlinks)
    config.run()
