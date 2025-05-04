from SCTool_Tracker_Git.twitch_integration import authenticate, create_clip, post_kill_to_chat

class Plugin:
    def __init__(self):
        self.name = "Twitch Control"
        self.triggers = ["twitch clip", "post kill", "authenticate twitch"]

    def execute(self, input_data):
        cmd = input_data.get("input", "").lower()
        if "clip" in cmd:
            return {"response": create_clip()}
        elif "post" in cmd:
            return {"response": post_kill_to_chat("New kill confirmed.")}
        elif "auth" in cmd:
            return {"response": authenticate()}
        return {"response": "Available: clip | post kill | authenticate"}
