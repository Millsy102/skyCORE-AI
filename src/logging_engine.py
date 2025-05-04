# 📦 Module imports
import logging
import os
from datetime import datetime

# Class: LogTraceAdapter — defines main behavior for logging_engine.py
class LogTraceAdapter(logging.LoggerAdapter):
# Function: process — handles a core step in this module
    def process(self, msg, kwargs):
    # 🏁 Returning result
        return f"[SkyCore][{self.extra['component']}][{self.extra['function']}][{self.extra['category']}] {msg}", kwargs

log_directory = "logs"
os.makedirs(log_directory, exist_ok=True)
log_file_path = os.path.join(log_directory, "skycore.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(log_file_path, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

# Function: log_trace — handles a core step in this module
def log_trace(component: str, function: str, category: str, message: str):
    adapter = LogTraceAdapter(logging.getLogger(), {
        "component": component,
        "function": function,
        "category": category
    })
    adapter.info(message)
