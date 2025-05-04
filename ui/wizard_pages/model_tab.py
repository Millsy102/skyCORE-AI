# 📦 Module imports
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QLineEdit, QCheckBox

# Class: ModelTab — defines main behavior for model_tab.py
class ModelTab(QWidget):
    def __init__(self, runtime):
        super().__init__()
        self.runtime = runtime
        self.settings = runtime.settings
        self.router = runtime.model_router

        layout = QVBoxLayout(self)

        self.model_select = QComboBox()
        self.model_select.addItems(self.router.get_all_models())
        self.model_select.setCurrentText(self.settings.get("default_model", ""))

        self.custom_endpoint = QLineEdit()
        self.custom_endpoint.setPlaceholderText("Custom model endpoint URL (optional)")

        self.auto_toggle = QCheckBox("Auto-select best model per task")
        self.auto_toggle.setChecked(self.settings.get("model_autoroute", True))

        layout.addWidget(QLabel("📦 Select Default Model"))
        layout.addWidget(self.model_select)
        layout.addWidget(QLabel("🔗 Custom Model Endpoint"))
        layout.addWidget(self.custom_endpoint)
        layout.addWidget(self.auto_toggle)

    def save(self):
        self.settings.set("default_model", self.model_select.currentText())
        self.settings.set("custom_model_url", self.custom_endpoint.text())
        self.settings.set("model_autoroute", self.auto_toggle.isChecked())
