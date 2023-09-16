import os
import subprocess

# Define the Blender URL
blender_url = 'https://download.blender.org/release/Blender2.83/blender-2.83.13-linux64.tar.xz'

# Use Poetry to get the path to the .venv folder
venv_dir = subprocess.check_output(["poetry", "env", "info", "--path"]).decode("utf-8").strip()

# Define the path to save the Blender installation
blender_install_dir = os.path.join(venv_dir, 'blender')

# Check if Blender is already installed in the virtual environment
if os.path.exists(blender_install_dir):
    print("Blender is already installed in the virtual environment.")
else:
    # Download Blender tarball
    os.system(f"curl -L {blender_url} -o blender.tar.xz")
    
    # Create a directory for Blender installation
    os.makedirs(blender_install_dir, exist_ok=True)

    # Extract Blender tarball to the installation directory
    os.system(f"tar -xf blender.tar.xz -C {blender_install_dir}")

    # Clean up the downloaded tarball
    os.remove("blender.tar.xz")

    print("Blender is now installed in the virtual environment.")
