
import os
import time
from threading import Thread

class SchedulerAgent(Thread):
    def __init__(self, runtime):
        super().__init__(daemon=True)
        self.runtime = runtime

    def run(self):
        while True:
            self.runtime.memory.save()
            time.sleep(600)

class PluginMonitorAgent(Thread):
    def __init__(self, runtime):
        super().__init__(daemon=True)
        self.runtime = runtime

    def run(self):
        last_seen = set(os.listdir("plugins"))
        while True:
            now = set(os.listdir("plugins"))
            if now != last_seen:
                self.runtime.plugin_loader.reload()
                last_seen = now
            time.sleep(30)

class MoodBalancerAgent(Thread):
    def __init__(self, runtime):
        super().__init__(daemon=True)
        self.runtime = runtime

    def run(self):
        while True:
            self.runtime.settings.set("mood_energy", 70)
            self.runtime.settings.set("mood_tone", 60)
            time.sleep(900)

class SelfDebugAgent(Thread):
    def __init__(self, runtime):
        super().__init__(daemon=True)
        self.runtime = runtime

    def run(self):
        while True:
            time.sleep(1200)
