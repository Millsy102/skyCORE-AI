# 📦 Module imports
import time
import json
from pathlib import Path
from collections import deque

AUDIT_LOG_PATH = Path("logs/audit.log")
AUDIT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

# Class: AuditLogger: — defines main behavior for audit_logger.py
class AuditLogger:
# Function: __init__ — handles a core step in this module
    def __init__(self):
        self.cache = deque(maxlen=200)

# Function: log_event — handles a core step in this module
    def log_event(self, category, event_type, data=None):
        entry = {
            "ts": time.strftime("%Y-%m-%d %H:%M:%S"),
            "category": category,
            "event": event_type,
            "data": data or {}
        }
        self.cache.append(entry)
        with open(AUDIT_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

# Function: get_recent — handles a core step in this module
    def get_recent(self, count=20):
    # 🏁 Returning result
        return list(self.cache)[-count:]

audit = AuditLogger()

# Function: log_audit — handles a core step in this module
def log_audit(event_type, data=None):
    audit.log_event("generic", event_type, data)