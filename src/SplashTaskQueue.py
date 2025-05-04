# 📦 Module imports
from PyQt5.QtCore import QObject, pyqtSignal, QThread
import time

# Class: SplashTaskQueue — defines main behavior for SplashTaskQueue.py
class SplashTaskQueue(QObject):
    progressChanged = pyqtSignal(int, str)
    finished = pyqtSignal()

# Function: __init__ — handles a core step in this module
    def __init__(self):
        super().__init__()
        self.tasks = []

# Function: add_task — handles a core step in this module
    def add_task(self, label, func):
        self.tasks.append((label, func))

# Function: run — handles a core step in this module
    def run(self):
        total = len(self.tasks)
        for i, (label, func) in enumerate(self.tasks):
            self.progressChanged.emit(int((i / total) * 100), label)
            try:
                func()
            except Exception as e:
            time.sleep(0.3)  # Simulate task delay
        self.progressChanged.emit(100, "Done.")
        self.finished.emit()

task_queue = SplashTaskQueue()