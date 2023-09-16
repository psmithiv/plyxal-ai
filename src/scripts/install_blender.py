import subprocess
import os
import shutil
from tqdm import tqdm
import argparse

# Define the Blender download URL and version (update as needed)
blender_url = "https://download.blender.org/release/Blender2.93/blender-2.93.5-linux-x64.tar.xz"
blender_version = "2.93.5"

# Define the directory where Blender will be installed
venv_path = subprocess.check_output(["poetry", "env", "info", "--path"], universal_newlines=True).strip()
blender_install_dir = os.path.expanduser(venv_path)
temp_dir = os.path.join(venv_path, "tmp")  # Temporary directory
cache_dir = os.path.join(venv_path, "cache")  # Cache directory

# Function to create the temporary directory
def create_temp_directory():
    os.makedirs(temp_dir, exist_ok=True)

# Function to check if Blender is available in the cache
def blender_in_cache():
    return os.path.exists(os.path.join(cache_dir, f"blender-{blender_version}-linux-x64.tar.xz"))

# Function to download Blender with a progress bar
def download_blender():
    create_temp_directory()  # Create the temporary directory

    # Download Blender to the temporary directory with a progress bar
    subprocess.run(["wget", "--progress=bar:force", "-P", temp_dir, blender_url])

    # Move the downloaded Blender file to the cache directory
    os.makedirs(cache_dir, exist_ok=True)
    shutil.move(os.path.join(temp_dir, f"blender-{blender_version}-linux-x64.tar.xz"), cache_dir)

# Function to install Blender from the cache
def install_blender_from_cache():
    # Extract Blender from the cached file in the cache directory
    subprocess.run(["tar", "-xvf", os.path.join(cache_dir, f"blender-{blender_version}-linux-x64.tar.xz"), "-C", temp_dir])

    # Rename the extracted directory and move it to the installation directory
    os.makedirs(blender_install_dir, exist_ok=True)
    subprocess.run(["mv", f"{temp_dir}/blender-{blender_version}-linux-x64", blender_install_dir])

# Function to install Blender
def install_blender(overwrite, skip_prompt):
    if blender_in_cache() and not overwrite:
        print("Using Blender from cache...")
        install_blender_from_cache()
    else:
        print("Downloading Blender...")
        download_blender()

        # Check if the destination directory already exists
        if os.path.exists(blender_install_dir) and not skip_prompt:
            choice = input(f"Destination directory '{blender_install_dir}' already exists. Overwrite? (y/n): ")
            if choice.lower() != 'y':
                print("Installation canceled.")
                return

        print("Installing Blender...")
        # Remove the existing destination directory if it exists
        if os.path.exists(blender_install_dir):
            shutil.rmtree(blender_install_dir)

        # Rename the extracted directory and move it to the installation directory
        os.makedirs(blender_install_dir, exist_ok=True)
        subprocess.run(["mv", f"{temp_dir}/blender-{blender_version}-linux-x64", blender_install_dir])

    # Clean up the temporary directory
    shutil.rmtree(temp_dir)

# Function to add Blender to PATH in Poetry environment
def add_blender_to_poetry_env():
    current_poetry_env = os.environ.get("VIRTUAL_ENV")
    if current_poetry_env:
        blender_path = os.path.join(blender_install_dir, "blender")
        subprocess.run(["poetry", "run", "python", "-m", "site", "--user-site"])
        user_site = subprocess.check_output(["poetry", "run", "python", "-m", "site", "--user-site"], text=True)
        user_bin = os.path.join(user_site.strip(), "bin")
        blender_symlink = os.path.join(user_bin, "blender")
        os.symlink(blender_path, blender_symlink)

# Main installation process
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Install Blender with an optional overwrite prompt.")
    parser.add_argument("-y", "--yes", action="store_true", help="Skip overwrite prompt and proceed.")
    args = parser.parse_args()

    try:
        if not args.yes:
            # Prompt for overwrite confirmation
            subprocess.run(["blender", "--version"])  # Check if Blender is installed
            overwrite = input("Blender is already installed. Overwrite? (y/n): ").lower() == "y"
        else:
            overwrite = True

        if not args.yes or overwrite:
            install_blender(overwrite, args.yes)
            add_blender_to_poetry_env()
            print(f"Blender {blender_version} is installed and available in the current Poetry environment.")
        else:
            print("Skipping installation.")
    except Exception as e:
        print(f"An error occurred: {e}")
