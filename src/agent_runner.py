
import time
import threading
from datetime import datetime

# Class: SkyAgentRunner: — defines main behavior for agent_runner.py
class SkyAgentRunner:
# Function: __init__ — handles a core step in this module
    def __init__(self, task_queue=None, interval=10):
        self.task_queue = task_queue or []
        self.interval = interval
        self.running = False

# Function: add_task — handles a core step in this module
    def add_task(self, task_fn, label="unnamed"):
        self.task_queue.append({"fn": task_fn, "label": label, "last_run": None})

# Function: start — handles a core step in this module
    def start(self):
        self.running = True
        thread = threading.Thread(target=self.run_loop, daemon=True)
        thread.start()

# Function: stop — handles a core step in this module
    def stop(self):
        self.running = False

# Function: run_loop — handles a core step in this module
    def run_loop(self):
        while self.running:
            for task in self.task_queue:
                now = datetime.now()
                task['last_run'] = now
                try:
                    task['fn']()
                except Exception as e:
    print('Agent error caught')
