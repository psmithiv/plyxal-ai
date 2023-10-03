import os
import subprocess
import sys

class SetupEnvironment:
    def __init__(self):
        self.python_version = None
        self.pip_version = None
        self.poetry_installed = None
        self.venv_path = None

    def check_python_and_pip_versions(self):
        try:
            self.python_version = subprocess.check_output(["python3", "--version"], universal_newlines=True, stderr=subprocess.STDOUT).strip()
            self.pip_version = subprocess.check_output(["pip3", "--version"], universal_newlines=True, stderr=subprocess.STDOUT).strip()
        except FileNotFoundError:
            print("Error: Python or pip command not found.", file=sys.stderr)
            sys.exit(1)

    def check_requirements(self):
        # Check if Python version meets minimum requirement
        if not self.python_version.startswith("Python 3.10"):
            print("Error: Python version 3.10.x is required.", file=sys.stderr)
            sys.exit(1)

        # Check if pip version meets minimum requirement
        if not self.pip_version.startswith("pip 23.2"):
            print("Error: pip version 23.2.x is required.", file=sys.stderr)
            sys.exit(1)

    def install_poetry(self):
        # Check if Poetry is already installed
        try:
            self.poetry_installed = subprocess.call(["poetry", "--version"], stderr=subprocess.STDOUT) == 0
        except FileNotFoundError:
            self.poetry_installed = False

        if not self.poetry_installed:
            print("Installing Poetry...")
            os.system("pip3 install -q poetry 2>/dev/null --root-user-action=ignore")

    def create_poetry_environment(self):
        print("Creating Poetry virtual environment and installing dependencies...")
        os.system("poetry install --no-cache")

        # Get the Poetry venv path
        self.venv_path = subprocess.check_output(["poetry", "env", "info", "--path"], universal_newlines=True).strip()

    def create_jupyter_kernel(self):
        if self.venv_path:
            kernel_command = f"{self.venv_path}/bin/python -m ipykernel install --user --name plyxal-ai --display-name plyxal-ai"
            os.system(kernel_command)
            print("The Poetry environment is now configured. Please switch kernels using 'Kernel -> Change Kernel...'")

    def run(self):
        self.check_python_and_pip_versions()
        self.check_requirements()
        self.install_poetry()
        self.create_poetry_environment()
        self.create_jupyter_kernel()

if __name__ == "__main__":
    # Redirect stdout and stderr to a log file
    with open('setup_log.txt', 'w') as log_file:
        sys.stdout = log_file
        sys.stderr = log_file
        config = SetupEnvironment()
        config.run()

    