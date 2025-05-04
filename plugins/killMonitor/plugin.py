from src.services.kill_monitor_service import KillMonitorService

class Plugin:
    def __init__(self):
        self.name = "Kill Monitor"
        self.triggers = ["start monitor", "stop monitor", "kill monitor"]
        self.monitor = KillMonitorService(runtime=None)

    def execute(self, input_data):
        cmd = input_data.get("input", "").lower()
        if "start" in cmd:
            self.monitor.start()
            return {"response": "🎯 Kill monitor started."}
        elif "stop" in cmd:
            self.monitor.stop()
            return {"response": "🛑 Kill monitor stopped."}
        return {"response": "Use: start monitor | stop monitor"}
