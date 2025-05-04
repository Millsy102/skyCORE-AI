import json
import time
from .twitch_integration import authenticate, create_clip, send_chat_message
from .kill_parser import parse_actor_death_event, format_weapon, determine_death_type

class TrackerService:
    def __init__(self):
        self.state = {"authenticated": False, "kills": []}

    def authenticate_twitch(self):
        result = authenticate()
        self.state["authenticated"] = True
        return result

    def create_clip(self):
        if not self.state["authenticated"]:
            return "🔒 Not authenticated to Twitch."
        return create_clip()

    def post_kill_message(self, msg="Enemy down!"):
        if not self.state["authenticated"]:
            return "🔒 Not authenticated to Twitch."
        send_chat_message(msg)
        return "🗨️ Message sent."

    def record_kill(self, data):
        parsed = parse_actor_death_event(data)
        parsed["timestamp"] = time.time()
        self.state["kills"].append(parsed)
        return parsed
