import obswebsocket
import obswebsocket.requests
import obswebsocket.exceptions

class OBSController:
    def __init__(self, host='localhost', port=4455, password=''):
        self.host = host
        self.port = port
        self.password = password
        self.client = obswebsocket.obsws(host, port, password)

    def connect(self):
        try:
            self.client.connect()
            return "✅ Connected to OBS WebSocket."
        except obswebsocket.exceptions.ConnectionFailure as e:
            return f"❌ Failed to connect to OBS: {e}"

    def disconnect(self):
        self.client.disconnect()

    def change_scene(self, scene_name):
        try:
            self.client.call(obswebsocket.requests.SetCurrentProgramScene(scene_name))
            return f"🎬 Scene changed to '{scene_name}'."
        except Exception as e:
            return f"⚠️ Scene change failed: {e}"

    def show_source(self, source_name):
        try:
            self.client.call(obswebsocket.requests.SetSceneItemEnabled(sceneName="", sceneItemId=source_name, sceneItemEnabled=True))
            return f"👁️ Showing source '{source_name}'."
        except Exception as e:
            return f"⚠️ Failed to show source: {e}"

    def hide_source(self, source_name):
        try:
            self.client.call(obswebsocket.requests.SetSceneItemEnabled(sceneName="", sceneItemId=source_name, sceneItemEnabled=False))
            return f"🙈 Hiding source '{source_name}'."
        except Exception as e:
            return f"⚠️ Failed to hide source: {e}"

    def start_streaming(self):
        try:
            self.client.call(obswebsocket.requests.StartStream())
            return "📡 Streaming started."
        except Exception as e:
            return f"⚠️ Failed to start stream: {e}"

    def stop_streaming(self):
        try:
            self.client.call(obswebsocket.requests.StopStream())
            return "⛔ Stream stopped."
        except Exception as e:
            return f"⚠️ Failed to stop stream: {e}"
