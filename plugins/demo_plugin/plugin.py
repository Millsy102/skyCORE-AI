class Plugin:
    def __init__(self):
        self.name = "Demo Plugin"
        self.triggers = ["demo"]

    def execute(self, input_data):
        return {
            "plugin": self.name,
            "response": f"Demo plugin received: {input_data}"
        }
