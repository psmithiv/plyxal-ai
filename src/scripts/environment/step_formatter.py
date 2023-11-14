# step_formatter.py - A utility class for formatting step information.

class StepFormatter:
    @staticmethod
    def colored_step(step_description):
        """Returns a colorized and formatted step information."""
        return f"\033[94mStep: {step_description}\033[0m"

    @staticmethod
    def menu_item(step_description):
        """Returns a colorized and formatted menu item."""
        return f"\033[94m {step_description}\033[0m"
