import time
import threading
import json
import os

class OverlayAutoRefresher:
    def __init__(self, file_path="overlays/overlay.json", interval=3):
        self.file_path = file_path
        self.interval = interval
        self.running = False
        self.thread = None

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._refresh_loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False

    def _refresh_loop(self):
        while self.running:
            self.write_state()
            time.sleep(self.interval)

    def write_state(self):
        try:
            # Example content — replace with actual plugin/game state export
            data = {
                "kills": 14,
                "deaths": 3,
                "status": "LIVE",
                "last_updated": time.time()
            }
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            with open(self.file_path, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
