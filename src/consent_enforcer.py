# 📦 Module imports
from src.settings_handler import load_settings
from src.logger import log

# Class: ConsentEnforcer: — defines main behavior for consent_enforcer.py
class ConsentEnforcer:
# Function: __init__ — handles a core step in this module
    def __init__(self):
        self.settings = load_settings()

# Function: check — handles a core step in this module
    def check(self, content_type):
        consent = self.settings.get("consent", {})
        allowed = consent.get(content_type, False)
        if not allowed:
            log(f"[Consent] Blocked usage of: {content_type}")
    # 🏁 Returning result
        return allowed

# Function: require — handles a core step in this module
    def require(self, content_type):
        if not self.check(content_type):
            raise PermissionError(f"Consent denied for: {content_type}")

enforcer = ConsentEnforcer()