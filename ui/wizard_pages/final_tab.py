# 📦 Module imports
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox

# Class: FinalTab — defines main behavior for final_tab.py
class FinalTab(QWidget):
# Function: __init__ — handles a core step in this module
    def __init__(self, runtime):
        super().__init__()
        self.runtime = runtime
        layout = QVBoxLayout(self)

        self.summary = QLabel("✅ All initial setup complete. Ready to launch skyCORE-AI.")
        self.summary.setWordWrap(True)

        self.save_btn = QPushButton("Save & Launch skyCORE-AI")
        self.save_btn.clicked.connect(self.finalize)

        layout.addWidget(self.summary)
        layout.addWidget(self.save_btn)

# Function: finalize — handles a core step in this module
    def finalize(self):
        # Save all wizard tab settings if they have save methods
        for tab in self.parent().parent().findChildren(QWidget):
            if hasattr(tab, "save") and callable(getattr(tab, "save")):
                tab.save()

        # Confirm finalization
        QMessageBox.information(self, "Launch", "🧠 skyCORE-AI config saved. Starting AI system...")
        self.parent().parent().accept()
