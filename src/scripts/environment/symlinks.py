import os
import argparse
import yaspin  # Install this library if not already installed

class SymlinkManager:
    def __init__(self, directory, ignore_list=[], quiet=False):
        self.directory = directory
        self.ignore_list = ignore_list
        self.quiet = quiet
        self.spinner = None

    def create_symlinks(self):
        for item in os.listdir(self.directory):
            item_path = os.path.join(self.directory, item)

            # Check if the item is a file or directory and starts with '.'
            if (os.path.isfile(item_path) or os.path.isdir(item_path)) and item.startswith('.'):
                # Check if the item is in the ignore list
                if item not in self.ignore_list:
                    symlink_name = "_" + item[1:]  # Add an underscore before the original name
                    symlink_path = os.path.join(self.directory, symlink_name)
                    if not os.path.lexists(symlink_path):
                        os.symlink(item_path, symlink_path)
                        if not self.quiet:
                            print(f"Created symlink: {symlink_path} -> {item_path}")
                    elif not self.quiet:
                        print(f"Symlink already exists: {symlink_path}")

    def remove_symlinks(self, recursive=False):
        for item in os.listdir(self.directory):
            item_path = os.path.join(self.directory, item)

            # Check if the item is a symlink
            if os.path.islink(item_path):
                os.remove(item_path)
                if not self.quiet:
                    print(f"Removed symlink: {item_path}")

                # If recursive is True, also remove subfolders
                if recursive and os.path.isdir(item_path):
                    os.rmdir(item_path)

    def run(self, remove=False):
        if self.quiet:
            self.spinner = yaspin.yaspin()
            self.spinner.start()

        try:
            if remove:
                self.remove_symlinks(recursive=remove)
            else:
                self.create_symlinks()

            if self.quiet:
                self.spinner.stop()
                print("done.")
        except Exception as e:
            if self.quiet:
                self.spinner.stop()
            print(f"An error occurred: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Create or remove symlinks for files and folders starting with a dot.")
    parser.add_argument("directory", help="Directory to scan for files and folders starting with a dot.")
    parser.add_argument("-r", "--remove", action="store_true", help="Remove symlinks instead of creating them.")
    parser.add_argument("-i", "--ignore", nargs="*", default=[], help="List of folders/files to ignore (not create symlinks for).")
    parser.add_argument("-q", "--quiet", action="store_true", help="Mute all output.")
    args = parser.parse_args()

    symlink_manager = SymlinkManager(args.directory, args.ignore, args.quiet)

    if args.remove:
        symlink_manager.run(remove=True)
    else:
        symlink_manager.run()

if __name__ == "__main__":
    main()



# import os
# import argparse
# import yaspin  # Install this library if not already installed

# def create_symlinks(directory, ignore_list, quiet=False):
#     for item in os.listdir(directory):
#         item_path = os.path.join(directory, item)

#         # Check if the item is a file or directory and starts with '.'
#         if (os.path.isfile(item_path) or os.path.isdir(item_path)) and item.startswith('.'):
#             # Check if the item is in the ignore list
#             if item not in ignore_list:
#                 symlink_name = "_" + item[1:]  # Add an underscore before the original name
#                 symlink_path = os.path.join(directory, symlink_name)
#                 if not os.path.lexists(symlink_path):
#                     os.symlink(item_path, symlink_path)
#                     if not quiet:
#                         print(f"Created symlink: {symlink_path} -> {item_path}")
#                 elif not quiet:
#                     print(f"Symlink already exists: {symlink_path}")

# def remove_symlinks(directory, recursive=False, quiet=False):
#     for item in os.listdir(directory):
#         item_path = os.path.join(directory, item)

#         # Check if the item is a symlink
#         if os.path.islink(item_path):
#             os.remove(item_path)
#             if not quiet:
#                 print(f"Removed symlink: {item_path}")

#             # If recursive is True, also remove subfolders
#             if recursive and os.path.isdir(item_path):
#                 os.rmdir(item_path)

# def main():
#     parser = argparse.ArgumentParser(description="Create or remove symlinks for files and folders starting with a dot.")
#     parser.add_argument("directory", help="Directory to scan for files and folders starting with a dot.")
#     parser.add_argument("-r", "--remove", action="store_true", help="Remove symlinks instead of creating them.")
#     parser.add_argument("-i", "--ignore", nargs="*", default=[], help="List of folders/files to ignore (not create symlinks for).")
#     parser.add_argument("-q", "--quiet", action="store_true", help="Mute all output.")
#     args = parser.parse_args()

#     if args.quiet:
#         spinner = yaspin.yaspin()
#         spinner.start()

#     try:
#         if args.remove:
#             remove_symlinks(args.directory, recursive=args.remove, quiet=args.quiet)
#         else:
#             create_symlinks(args.directory, args.ignore, args.quiet)

#         if args.quiet:
#             spinner.stop()
#             print("done.")
#     except Exception as e:
#         if args.quiet:
#             spinner.stop()
#         print(f"An error occurred: {str(e)}")

# if __name__ == "__main__":
#     main()
