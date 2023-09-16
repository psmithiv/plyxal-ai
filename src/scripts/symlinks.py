import os
import argparse

def create_symlinks(directory, ignore_list):
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if item.startswith('.'):
            # Check if the item is in the ignore list
            if item not in ignore_list:
                symlink_name = "_" + item[1:]  # Add an underscore before the original name
                symlink_path = os.path.join(directory, symlink_name)
                if not os.path.lexists(symlink_path):
                    os.symlink(item_path, symlink_path)
                    print(f"Created symlink: {symlink_path} -> {item_path}")
                else:
                    print(f"Symlink already exists: {symlink_path}")

def remove_symlinks(directory):
    for item in os.listdir(directory):
        symlink_path = os.path.join(directory, item)
        if os.path.islink(symlink_path):
            os.remove(symlink_path)
            print(f"Removed symlink: {symlink_path}")

def main():
    parser = argparse.ArgumentParser(description="Create or remove symlinks for files and folders starting with a dot.")
    parser.add_argument("directory", help="Directory to scan for files and folders starting with a dot.")
    parser.add_argument("--remove", action="store_true", help="Remove symlinks instead of creating them.")
    parser.add_argument("--ignore", nargs="*", default=[], help="List of folders/files to ignore (not create symlinks for).")
    args = parser.parse_args()

    if args.remove:
        remove_symlinks(args.directory)
    else:
        create_symlinks(args.directory, args.ignore)

if __name__ == "__main__":
    main()
