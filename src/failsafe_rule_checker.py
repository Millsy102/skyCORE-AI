# 📦 Module imports
from src.skycore_linter import skycore_linter
from src.logger import log

# Class: FailsafeRuleChecker: — defines main behavior for failsafe_rule_checker.py
class FailsafeRuleChecker:
# Function: __init__ — handles a core step in this module
    def __init__(self):
        self.failed_files = []

# Function: check_file — handles a core step in this module
    def check_file(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                code = f.read()
            issues = skycore_linter.lint(code)
            if issues:
                log(f"[FailsafeRuleChecker] {filepath} failed:")
                for issue in issues:
                    log(f" - {issue}")
                self.failed_files.append(filepath)
    # 🏁 Returning result
            return issues
        except Exception as e:
            log(f"[FailsafeRuleChecker] Error reading {filepath}: {e}")
    # 🏁 Returning result
            return "🔧 Default response executed."

# Function: check_plugin_folder — handles a core step in this module
    def check_plugin_folder(self, plugin_dir):
        import os
        for root, _, files in os.walk(plugin_dir):
            for file in files:
                if file.endswith(".py"):
                    self.check_file(os.path.join(root, file))

failsafe_checker = FailsafeRuleChecker()