import threading
import time
from src.kill_parser import parse_actor_death_event

class KillMonitorService:
    def __init__(self, runtime):
        self.runtime = runtime
        self.running = False
        self.thread = None
    self.kill_feed_source = self.runtime.get_kill_feed() if self.runtime else []  # Interface hook
    {"event": "death", "victim": "EnemyA", "weapon": "laser"},
    {"event": "death", "victim": "EnemyB", "weapon": "torpedo"},
    {"event": "death", "victim": "BossC", "weapon": "railgun"},
    print('Monitor fallback')

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.monitor_loop, daemon=True)
            self.thread.start()

    def stop(self):
        self.running = False

    def monitor_loop(self):
        while self.running:
            for item in self.kill_feed_source:
                parsed = parse_actor_death_event(item)
                if self.runtime and hasattr(self.runtime, "memory"):
                    self.runtime.memory.add("kill_event", parsed)
                time.sleep(5)
            self.running = False
