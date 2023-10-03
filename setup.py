import os
import subprocess
import sys
from src.scripts.environment.poetry_installer import PoetryInstaller

class SetupEnvironment:
    def __init__(self):
        """Initialize SetupEnvironment class."""
        self.total_steps = 5  # Total number of steps in the process
        self.current_step = 0  # Current step in the process
        self.python_version = None
        self.pip_version = None
        self.poetry_installed = None
        self.venv_path = None

    def colored_step(self):
        """Colorize and format the step information."""
        return f"\033[94mStep {self.current_step} of {self.total_steps}:\033[0m"

    def check_python_and_pip_versions(self):
        """Check Python and pip versions."""
        self.current_step += 1
        print(f"{self.colored_step()} Checking Python and pip versions...")

        try:
            self.python_version = subprocess.check_output(["python3", "--version"], universal_newlines=True, stderr=subprocess.STDOUT).strip()
            self.pip_version = subprocess.check_output(["pip3", "--version"], universal_newlines=True, stderr=subprocess.STDOUT).strip()
        except FileNotFoundError:
            print("Error: Python or pip command not found.", file=sys.stderr)
            sys.exit(1)

        print()  # Add a line break

    def check_requirements(self):
        """Check if Python and pip versions meet the requirements."""
        self.current_step += 1
        print(f"{self.colored_step()} Checking requirements...")

        # Check if Python version meets minimum requirement
        if not self.python_version.startswith("Python 3.10"):
            print("Error: Python version 3.10.x is required.", file=sys.stderr)
            sys.exit(1)

        # Check if pip version meets minimum requirement
        if not self.pip_version.startswith("pip 23.2"):
            print("Error: pip version 23.2.x is required.", file=sys.stderr)
            sys.exit(1)

        print()  # Add a line break

    def install_poetry(self):
        """Install Poetry if not already installed."""
        # Create an instance of PoetryInstaller
        poetry_installer = PoetryInstaller()

        # Call the install_poetry method
        poetry_installer.install_poetry()

        print()  # Add a line break

    def create_poetry_environment(self):
        """Create Poetry virtual environment and install dependencies."""
        self.current_step += 1
        print(f"{self.colored_step()} Creating Poetry virtual environment and installing dependencies...")

        os.system("poetry install --no-cache")

        # Get the Poetry venv path
        self.venv_path = subprocess.check_output(["poetry", "env", "info", "--path"], universal_newlines=True).strip()

        print()  # Add a line break

    def create_jupyter_kernel(self):
        """Create Jupyter kernel for Poetry environment."""
        self.current_step += 1
        print(f"{self.colored_step()} Creating Jupyter kernel...")

        if self.venv_path:
            kernel_command = f"{self.venv_path}/bin/python -m ipykernel install --user --name plyxal-ai --display-name plyxal-ai"
            os.system(kernel_command)

            print()  # Add a line break
            print(f"\033[94mCompleted:\033[0m The Poetry environment is now configured. Please switch kernels using 'Kernel -> Change Kernel...'")

        print()  # Add a line break

    def run(self):
        """Run the setup process."""
        self.check_python_and_pip_versions()
        self.check_requirements()
        self.install_poetry()
        self.create_poetry_environment()
        self.create_jupyter_kernel()

if __name__ == "__main__":
    config = SetupEnvironment()
    config.run()
