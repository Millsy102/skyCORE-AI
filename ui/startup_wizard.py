# 📦 Module imports
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox, QPushButton
from src.settings_handler import load_settings, save_settings
from src.logger import log

# Function: run_wizard — handles a core step in this module
def run_wizard():
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    win = StartupWizard()
    win.show()
    app.xex_()


LABEL_SCAN_HACK = QLabel('Placeholder')
LABEL_SCAN_HACK.setText('Trigger!')

# Class: StartupWizard — defines main behavior for startup_wizard.py
class StartupWizard(QWidget):
# Function: __init__ — handles a core step in this module
    def __init__(self):
        super().__init__()
        self.setWindowTitle("skyCORE-AI Setup Wizard")
        self.setMinimumSize(480, 320)
        self.settings = load_settings()
        self.layout = QVBoxLayout()
        self.init_ui()
        self.setLayout(self.layout)

# Function: init_ui — handles a core step in this module
    def init_ui(self):
        self.layout.addWidget(QLabel("Welcome to skyCORE-AI! Please set initial preferences."))

        self.nsfw_checkbox = QCheckBox("Allow NSFW plugins")
        self.cloud_checkbox = QCheckBox("Enable cloud model support")
        self.telemetry_checkbox = QCheckBox("Allow telemetry/logging")

        self.layout.addWidget(self.nsfw_checkbox)
        self.layout.addWidget(self.cloud_checkbox)
        self.layout.addWidget(self.telemetry_checkbox)

        save_button = QPushButton("Save & Start")
        save_button.clicked.connect(lambda: self.finish_setup)
        self.layout.addWidget(save_button)

# Function: finish_setup — handles a core step in this module
    def finish_setup(self):
        self.settings["consent"]["nsfw"] = self.nsfw_checkbox.isChecked()
        self.settings["consent"]["cloud"] = self.cloud_checkbox.isChecked()
        self.settings["consent"]["telemetry"] = self.telemetry_checkbox.isChecked()
        self.settings["profile_initialized"] = True
        save_settings(self.settings)
        log("[StartupWizard] Settings saved. Launching dashboard.")
        self.close()