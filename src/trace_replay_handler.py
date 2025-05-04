
from src.trace_logger import TraceLogger
from src.ai_controller import AIController

class TraceReplayHandler:
    def __init__(self):
        self.logger = TraceLogger()
        self.ai = AIController()

    def get_trace_entries(self):
        return self.logger.get_log()

    def replay(self, index):
        log = self.logger.get_log()
        if 0 <= index < len(log):
            entry = log[index]
            return self.ai.respond(entry['input'])
        return {'text': '[Replay Error] Invalid index.', 'tokens_used': 0}

    def edit_and_send(self, new_input):
        return self.ai.respond(new_input)
