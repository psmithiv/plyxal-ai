import os
import requests
import tarfile

# Define the URL for downloading the Blender archive.
blender_download_url = "https://mirrors.ocf.berkeley.edu/blender/release/Blender3.6/blender-3.6.2-linux-x64.tar.xz"

# Use the current working directory as the project root.
project_root = os.getcwd()

# Define the folder where you want to extract Blender (project root/apps).
extract_folder = os.path.join("/blender")

# Create the extraction folder if it doesn't exist.
os.makedirs(extract_folder, exist_ok=True)

# Define the file name for the downloaded Blender archive.
blender_archive = os.path.join(extract_folder, "blender.tar.xz")

# Download Blender archive.
response = requests.get(blender_download_url)
if response.status_code == 200:
    with open(blender_archive, "wb") as f:
        f.write(response.content)
    print("Blender downloaded successfully.")
else:
    print("Failed to download Blender.")
    exit(1)

# Extract Blender archive.
try:
    with tarfile.open(blender_archive, "r:xz") as archive:
        archive.extractall(extract_folder)
    print("Blender extracted successfully.")
except Exception as e:
    print(f"Failed to extract Blender: {e}")
    exit(1)

# Clean up the downloaded archive.
os.remove(blender_archive)

# Verify Blender installation.
# blender_path = os.path.join(extract_folder, "blender-3.6.2-linux-x64", "blender")
# os.system(f"{blender_path} --version")
