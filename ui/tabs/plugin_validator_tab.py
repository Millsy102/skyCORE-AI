from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QFileDialog
from src.plugin_validator import PluginValidator
from src.ai_plugin_auditor import AIPluginAuditor

class PluginValidatorTab(QWidget):
    def __init__(self, runtime):
        super().__init__()
        layout = QVBoxLayout(self)
        self.runtime = runtime

        layout.addWidget(QLabel("🧪 Plugin Validator & Auditor"))

        self.input = QLineEdit()
        self.input.setPlaceholderText("Plugin name")
        layout.addWidget(self.input)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)

        btn = QPushButton("Run Validator")
        btn.clicked.connect(self.run)
        layout.addWidget(btn)

        export = QPushButton("📤 Export Result")
        export.clicked.connect(self.export_report)
        layout.addWidget(export)

        self.validator = PluginValidator()
        self.auditor = AIPluginAuditor()

    def run(self):
        name = self.input.text()
        report = self.validator.validate(name)
        try:
            code = open(f"plugins/{name}/plugin.py").read()
        except:
            code = ""
        audit = self.auditor.audit(code)

        risk = audit.get("risk", "low")
        flag = "🟢" if risk == "low" else "🟡" if risk == "medium" else "🔴"
        summary = f"Validator: {report}\n\nAuditor: {flag} {audit}"
        self.output.setText(summary)

    def export_report(self):
        text = self.output.toPlainText()
        path, _ = QFileDialog.getSaveFileName(self, "Export Report", "audit_report.txt", "Text Files (*.txt)")
        if path:
            open(path, "w").write(text)
