# sudo yum install make


import os
import subprocess

# Define the directory where you want to build Blender
build_dir = "./build"
blender_src_dir = os.path.join(build_dir, "blender_src")

# Define the URL to Blender's source code repository
blender_repo_url = "https://projects.blender.org/?service=git-upload-pack"

# Clone the Blender source code repository
if not os.path.exists(blender_src_dir):
    os.makedirs(blender_src_dir)
    subprocess.check_call(["git", "clone", blender_repo_url, blender_src_dir])

# Change to the Blender source code directory
os.chdir(blender_src_dir)

# Checkout a specific Blender version (optional)
# subprocess.check_call(["git", "checkout", "v2.93.0"])  # Replace with the desired version

# Configure Blender for headless build
subprocess.check_call(["make", "update"])

# Set CMake options for headless build
cmake_options = [
    "-DWITH_HEADLESS=ON",  # Enable headless mode
    "-DWITH_PYTHON_INSTALL=OFF",  # Do not install Python with Blender
]

# Create the build directory and configure the build
build_cmd = ["cmake", "-B", build_dir] + cmake_options
subprocess.check_call(build_cmd, cwd=blender_src_dir)

# Build Blender
subprocess.check_call(["make", "-j"], cwd=build_dir)

# Your headless Blender executable will be in the 'build_dir/bin' directory.
print("Headless Blender build completed.")
