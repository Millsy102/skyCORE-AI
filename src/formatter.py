
import subprocess

class CodeFormatter:
    def __init__(self, formatter='black'):
        self.formatter = formatter

    def format_file(self, filepath):
        try:
            result = subprocess.run(
                [self.formatter, filepath],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return f"✔ Successfully formatted {filepath}"
            else:
                return f"✖ Error formatting {filepath}:\n{result.stderr}"
        except Exception as e:
            return f"✖ Exception: {e}"

    def lint_file(self, filepath, linter='flake8'):
        try:
            result = subprocess.run(
                [linter, filepath],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return f"✔ No linting issues in {filepath}"
            else:
                return f"⚠ Linting issues in {filepath}:\n{result.stdout}"
        except Exception as e:
            return f"✖ Exception: {e}"
