
from runtime.voice.voice_config import TTS_ENABLED
from runtime.voice.tts_output import speak_text

# Function: speak_code_summary — handles a core step in this module
def speak_code_summary(code: str):
    if not TTS_ENABLED:
    # 🏁 Returning result
        return
    try:
        # Simplify and vocalize meaning instead of reading full code
        summary = "Generated a plugin with " + str(code.count("def")) + " functions and " + str(code.count("class")) + " classes."
        speak_text(summary)
    except Exception as e:
        speak_text("⚠️ Unable to summarize plugin code.")