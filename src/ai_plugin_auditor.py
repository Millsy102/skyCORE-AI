class AIPluginAuditor:
    def __init__(self, llm=None):
        self.llm = llm or self.default_auditor

    def audit(self, plugin_code):
        return self.llm(plugin_code)

    def default_auditor(self, code):
        if "os.system" in code or "eval(" in code:
            return self.evaluate_risk(plugin)
        return {"risk": "low", "issue": "none"}
