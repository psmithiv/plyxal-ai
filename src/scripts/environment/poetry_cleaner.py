# poetry_cleaner.py - A class for cleaning up Poetry-related environment.

import os
import subprocess
import argparse
from pathlib import Path
from .step_formatter import StepFormatter


class PoetryCleaner:
    def __init__(self, dry_run=False, keep_venv=False, auto_confirm=False):
        """Initializes the PoetryCleaner class."""
        self.dry_run = dry_run  # Flag for dry run mode
        self.keep_venv = keep_venv  # Added keep_venv flag (for debugging purposes)
        self.auto_confirm = auto_confirm  # Flag to automatically confirm without prompting
        self.step_formatter = StepFormatter()

    def display_step(self, step_description):
        """Displays the current step."""
        if not self.dry_run:
            print(self.step_formatter.colored_step(step_description))
        else:
            print(f"Dry run: {self.step_formatter.colored_step(step_description)} (not executed)")

    def is_poetry_installed(self):
        """Check if Poetry is installed."""
        try:
            subprocess.check_output(["poetry", "--version"], universal_newlines=True)
            return True
        except FileNotFoundError:
            return False

    def clean_cache(self):
        """Step 1: Clean Poetry's cache."""
        self.display_step("Cleaning Poetry's cache...")
        cache_dir = Path.home() / ".cache" / "poetry"
        if cache_dir.exists():
            if not self.dry_run:
                os.system(f"rm -rf {cache_dir}")
            print("Poetry's cache cleaned.")
        else:
            print("No Poetry cache found.")

    def remove_environments(self):
        """Step 2: Remove Poetry environments."""
        self.display_step("Removing Poetry environments...")
        if self.is_poetry_installed() and not self.dry_run:
            if not self.keep_venv:  # Check the keep_venv flag
                os.system("poetry env remove --all")
                print("Poetry environments removed.")
            else:
                print("Keeping Poetry environments as per the --keep-venv flag.")
        else:
            print("Poetry is not installed or no environments found.")

    def remove_kernels(self):
        """Step 3: Remove Jupyter kernels associated with Poetry environments."""
        self.display_step("Removing associated Jupyter kernels...")
        kernels_dir = Path.home() / ".local" / "share" / "jupyter" / "kernels"
        if kernels_dir.exists():
            for entry in kernels_dir.iterdir():
                if entry.is_dir() and entry.name.startswith("poetry-"):
                    if not self.dry_run:
                        os.system(f"rm -rf {entry}")
            print("Jupyter kernels removed.")
        else:
            print("No Jupyter kernels found.")

    def remove_poetry(self):
        """Step 4: Remove Poetry and associated files."""
        self.display_step("Removing Poetry...")
        if self.is_poetry_installed() and not self.dry_run:
            os.system("pip uninstall -y poetry")
            print("Poetry removed.")
        else:
            print("Poetry is not installed.")

    def run(self):
        """Perform the cleanup process."""
        self.clean_cache()
        self.remove_environments()
        self.remove_kernels()
        if not self.keep_venv:  # Check the keep_venv flag
            self.remove_poetry()


def confirm_execution(auto_confirm):
    """Ask for user confirmation before executing the script."""
    if auto_confirm or input(
            "WARNING: This action will clean up Poetry-related environment, including all cached files, environments, and kernels.\n"
            "Are you sure you want to continue? (y/N): ").lower() == "y":
        return True
    return False


def main():
    parser = argparse.ArgumentParser(description='Clean Poetry Environment')
    parser.add_argument('--dry-run', action='store_true',
                        help="Perform a dry run (list actions without executing them)")
    parser.add_argument('--keep-venv', action='store_true', help="Keep the .venv folder (for debugging purposes only)")
    parser.add_argument('-y', '--auto-confirm', action='store_true', help="Automatically confirm without prompting")

    args = parser.parse_args()

    if not args.dry_run:
        if confirm_execution(args.auto_confirm):  # Pass the auto_confirm flag
            print("Performing cleanup actions...")
            cleaner = PoetryCleaner(args.dry_run, args.keep_venv, args.auto_confirm)  # Pass the auto_confirm flag

            if cleaner.is_poetry_installed():
                print("Poetry is installed.")
                cleaner.run()
            else:
                print("Poetry is not installed. No cleanup needed.")
        else:
            print("Cleanup aborted.")
    else:
        print("Performing dry run...")


if __name__ == "__main__":
    main()
