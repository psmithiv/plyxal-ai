import os
import subprocess
import sys
from src.scripts.environment.poetry_installer import PoetryInstaller
from src.scripts.environment.symlink_manager import SymlinkManager

class SetupEnvironment:
    def __init__(self):
        """Initializes the SetupEnvironment class."""
        self.total_steps = 5  # Total number of steps in the process
        self.current_step = 0  # Current step in the process
        self.python_version = None
        self.pip_version = None
        self.poetry_installed = None
        self.venv_path = None

    def colored_step(self):
        """Returns a colorized and formatted step information."""
        return f"\033[94mStep {self.current_step} of {self.total_steps}:\033[0m"

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
        if not self.python_version.startswith("Python 3.10"):
            print("Error: Python version 3.10.x is required.", file=sys.stderr)
            sys.exit(1)
        else:
            print(f"Python version: {self.python_version}")

        # Check if pip version meets minimum requirement
        if not self.pip_version.startswith("pip 23.2"):
            print("Error: pip version 23.2.x is required.", file=sys.stderr)
            sys.exit(1)
        else:
             print(f"pip version: {self.pip_version}")
            
        print()  # Add a line break

    def install_poetry(self):
        """Step 2: Install Poetry if not already installed."""
        self.current_step += 1
        print(f"{self.colored_step()} Installing Poetry...")
        
        # Create an instance of PoetryInstaller
        poetry_installer = PoetryInstaller()

        # Call the install_poetry method
        poetry_installer.install_poetry()

        # print()  # Add a line break

    def create_poetry_environment(self):
        """Step 3: Create Poetry virtual environment and install dependencies."""
        self.current_step += 1
        print(f"{self.colored_step()} Creating Poetry virtual environment and installing dependencies...")

        # Run 'poetry install --no-cache' to create the environment and install dependencies
        os.system("poetry install --no-cache")

        # Get the Poetry venv path
        self.venv_path = subprocess.check_output(["poetry", "env", "info", "--path"], universal_newlines=True).strip()

        print()  # Add a line break

    def create_symlinks(self):
        """Step 4: Create Symlinks for files and folders starting with a dot."""
        self.current_step += 1
        print(f"{self.colored_step()} Creating Symlinks...")

        # Initialize SymlinkManager with the current directory, ignore list, and quiet flag
        symlink_manager = SymlinkManager('./', ['.git', '.ipynb_checkpoints'], False)
        
        # Call the create_symlinks method of SymlinkManager
        symlink_manager.create_symlinks()
        
        print() # Add a line break
        
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

        print()  # Add a line break

    def run(self):
        """Run the setup process."""
        self.check_python_and_pip_versions()
        self.install_poetry()
        self.create_poetry_environment()
        self.create_symlinks()
        self.create_jupyter_kernel()

if __name__ == "__main__":
    config = SetupEnvironment()
    config.run()
