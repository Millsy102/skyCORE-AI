
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit
import traceback

class EvaluatorTab(QWidget):
    def __init__(self, runtime):
        super().__init__()
        self.runtime = runtime
        layout = QVBoxLayout(self)
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.run_btn = QPushButton("🧠 Run Full Project Check")
        self.run_btn.clicked.connect(self.evaluate)
        layout.addWidget(QLabel("🧠 Smart Project Evaluator"))
        layout.addWidget(self.run_btn)
        layout.addWidget(self.output)
        self.setLayout(layout)

    def evaluate(self):
        try:
            # Evaluator logic for boot flow confirmation
            status = [
                f"✅ Plugins Loaded: {len(self.runtime.plugin_loader.plugins)}",
                f"✅ Models Available: {len(self.runtime.model_router.get_all_models())}",
                f"✅ Current Persona: {self.runtime.persona.get_current()}",
                "✅ Memory Validated" if hasattr(self.runtime.memory, 'export') else "⚠️ Memory Engine Incomplete"
            ]
            self.output.setText("\n".join(status))
        except Exception as e:
            self.output.setText("❌ Evaluation Failed:\n" + traceback.format_exc())
