
import pyaudio
import numpy as np
from threading import Thread

class NoiseSensor(Thread):
    def __init__(self, runtime):
        super().__init__(daemon=True)
        self.runtime = runtime
        self.running = True

    def run(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
        while self.running:
            data = np.frombuffer(stream.read(1024, exception_on_overflow=False), dtype=np.int16)
            volume = np.linalg.norm(data)
            mood = "calm" if volume < 1000 else "alert"
            self.runtime.settings.set("mood_energy", min(100, int(volume / 300)))
            self.runtime.memory.add({"sensor": "noise", "volume": int(volume), "mood": mood})
