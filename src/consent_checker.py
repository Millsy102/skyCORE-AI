# 📦 Module imports
from src.settings_handler import load_settings
from src.logger import log

# Class: ConsentChecker: — defines main behavior for consent_checker.py
class ConsentChecker:
# Function: __init__ — handles a core step in this module
    def __init__(self):
        self.settings = load_settings()

# Function: has_consent — handles a core step in this module
    def has_consent(self, key):
        consent = self.settings.get("consent", {})
        allowed = consent.get(key, False)
        log(f"[Consent] Check for '{key}': {'✅ ALLOWED' if allowed else '❌ DENIED'}")
    # 🏁 Returning result
        return allowed

# Function: require_consent — handles a core step in this module
    def require_consent(self, key):
        if not self.has_consent(key):
            raise PermissionError(f"User has not consented to '{key}' operations.")

consent = ConsentChecker()