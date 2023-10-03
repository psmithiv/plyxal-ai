import os
import subprocess

def update_python_pip():
    """Updates Python and pip to minimum required versions if necessary."""
    # Minimum required Python and pip versions
    python_version = "3.10"
    pip_version = "23.2"

    try:
        # Check Python version
        output = subprocess.check_output(["python3", "--version"], stderr=subprocess.STDOUT, text=True)
        if not output.startswith(f"Python {python_version}"):
            print(f"Updating Python to version {python_version}...")
            os.system("sudo apt-get update")
            os.system(f"sudo apt-get install python{python_version} python{python_version}-dev")

        # Check pip version
        output = subprocess.check_output(["pip3", "--version"], stderr=subprocess.STDOUT, text=True)
        version_string = output.strip().split()[1]
        major, minor, _ = map(int, version_string.split("."))
        if (major, minor) < (int(pip_version.split(".")[0]), int(pip_version.split(".")[1])):
            print(f"Updating pip to version {pip_version}...")
            os.system("python3 -m pip install --upgrade pip")

    except subprocess.CalledProcessError as e:
        print(f"Error checking Python/pip versions: {e.output.strip()}")

def install_poetry():
    """Installs Poetry without using the cache if not already installed."""
    try:
        # Check if Poetry is installed
        subprocess.check_output(["poetry", "--version"], stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        print("Installing Poetry without using cache...")
        os.system("python3 -m pip install --no-cache-dir poetry")

def create_virtual_environment():
    """Creates a virtual environment and installs dependencies using Poetry."""
    try:
        # Create a virtual environment
        os.system("poetry install --no-cache")

        # Display the virtual environment path
        venv_path = subprocess.check_output(["poetry", "env", "info", "--path"], universal_newlines=True).strip()
        print(f"Virtual environment path: {venv_path}")

    except subprocess.CalledProcessError as e:
        print(f"Error creating virtual environment: {e.output.strip()}")

def create_poetry_kernel():
    """Creates a Jupyter kernel using the Poetry environment."""
    try:
        venv_path = subprocess.check_output(["poetry", "env", "info", "--path"], universal_newlines=True).strip()
        kernel_command = f"{venv_path}/bin/python -m ipykernel install --user --name plyxal-ai --display-name plyxal-ai"
        os.system(kernel_command)
        print("The Poetry environment is now configured.")
        print("Please manually restart the Jupyter kernel to use the new environment.")
    except subprocess.CalledProcessError as e:
        print(f"Error creating Jupyter kernel: {e.output.strip()}")

if __name__ == "__main__":
    update_python_pip()
    install_poetry()
    create_virtual_environment()
    create_poetry_kernel()
