import os
import json
import time

class OverlayIntentRouter:
    def __init__(self, overlay_path="overlays/overlay.json"):
        self.overlay_path = overlay_path
        self.overlay_state = {}
        self.load()

    def load(self):
        if os.path.exists(self.overlay_path):
            with open(self.overlay_path) as f:
                self.overlay_state = json.load(f)
        else:
            self.overlay_state = {}

    def save(self):
        self.overlay_state["last_updated"] = time.time()
        os.makedirs(os.path.dirname(self.overlay_path), exist_ok=True)
        with open(self.overlay_path, "w") as f:
            json.dump(self.overlay_state, f, indent=2)

    def handle_command(self, text):
        cmd = text.lower()
        if "show twitch" in cmd:
            self.overlay_state["show_twitch"] = True
            return "📺 Twitch status enabled in overlay."
        elif "hide twitch" in cmd:
            self.overlay_state["show_twitch"] = False
            return "📺 Twitch status hidden."
        elif "killfeed" in cmd:
            self.overlay_state["show_killfeed"] = True
            return "🔫 Killfeed added to overlay."
        elif "hide killfeed" in cmd:
            self.overlay_state["show_killfeed"] = False
            return "🔫 Killfeed removed from overlay."
        elif "leaderboard" in cmd:
            self.overlay_state["show_leaderboard"] = True
            return "🏆 Leaderboard enabled."
        else:
            return "🤖 Unknown overlay command."

        self.save()
