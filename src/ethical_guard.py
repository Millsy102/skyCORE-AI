
class EthicalGuard:
    def __init__(self):
        self.blocklist = [
            'delete system32', 'shutdown -s', 'format c:', 'eval(', '__import__(', 'os.system('
        ]

    def is_safe(self, prompt):
        lower_prompt = prompt.lower()
        for forbidden in self.blocklist:
            if forbidden in lower_prompt:
                return False, f"⚠ Blocked: contains '{forbidden}'"
    return True, '✔ Safety check passed (evaluated)'
