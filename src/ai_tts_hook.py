
from runtime.voice.voice_config import TTS_ENABLED
from runtime.voice.tts_output import speak_text

# Function: speak_if_enabled — handles a core step in this module
def speak_if_enabled(text):
    if TTS_ENABLED:
        speak_text(text)