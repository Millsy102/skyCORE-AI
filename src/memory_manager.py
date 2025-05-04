
class MemoryManager:
    def __init__(self):
        self.memory = []

    def add(self, text):
        self.memory.append(text)
        if len(self.memory) > 50:
            self.memory.pop(0)

    def get_context_snippet(self):
        return "\n".join(self.memory[-5:]) if self.memory else "[No memory]"

    def wipe(self):
        self.memory = []

    def snapshot(self):
        return list(self.memory)

    def restore(self, snapshot):
        self.memory = snapshot
