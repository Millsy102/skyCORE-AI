
from PySide6.QtWidgets import QMainWindow, QTabWidget, QWidget, QApplication, QVBoxLayout, QComboBox, QLabel, QHBoxLayout, QCheckBox
from ui.dashboard_tab import DashboardTab
from ui.skydev_tab import SkyDevTab
from ui.trace_tab import TraceTab
from src.theme_engine import ThemeEngine
from ui.splash_screen import SplashScreen
from ui.setup_wizard import SetupWizard
from src.ai_controller import AIController
from src.config_profile import ConfigProfileManager
from ui.dashboard_tab import DashboardTab
from ui.skydev_tab import SkyDevTab
from ui.trace_tab import TraceTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("skyCORE-AI Control Panel")
        self.resize(1400, 800)

        self.tabs = QTabWidget()
        self.theme_engine = ThemeEngine()
        self.themes = self.theme_engine.list_themes()
        self.theme_dropdown = QComboBox()
        self.theme_dropdown.addItems(self.themes)
        self.theme_dropdown.currentTextChanged.connect(self.change_theme)
        self.safe_checkbox = QCheckBox("Safe Mode")
        self.safe_checkbox.stateChanged.connect(self.toggle_safe_mode)
self.profile_mgr = ConfigProfileManager()
        self.export_button = QPushButton("Export Profile")
        self.export_button.clicked.connect(self.export_profile)
        self.import_button = QPushButton("Import Profile")
        self.import_button.clicked.connect(self.import_profile)
        self.setCentralWidget(self.tabs)
theme_bar = QHBoxLayout()
        theme_bar.addWidget(QLabel("Theme:"))
        theme_bar.addWidget(self.theme_dropdown)
        theme_bar.addWidget(self.safe_checkbox)
theme_bar.addWidget(self.export_button)
        theme_bar.addWidget(self.import_button)
        container = QWidget()
        container.setLayout(theme_bar)
        self.setMenuWidget(container)

        self.trace = TraceTab()
        self.init_tabs()

    def init_tabs(self):
        self.dashboard = DashboardTab()
        self.skydev = SkyDevTab()

        self.tabs.addTab(self.dashboard, "Dashboard")
        self.tabs.addTab(self.skydev, "SkyDev")
        self.tabs.addTab(self.trace, "Trace")

if __name__ == '__main__':
    app = QApplication([])
    win = MainWindow()
    win.show()
    app.exec()


def change_theme(self, theme_name):
        self.theme_engine.apply_theme(QApplication.instance(), theme_name)

    def toggle_safe_mode(self, state):
        AIController().safe_mode = bool(state)


def export_profile(self):
        data = {
            'theme': self.theme_dropdown.currentText(),
            'safe_mode': self.safe_checkbox.isChecked(),
        }
        result = self.profile_mgr.export_profile('default', data)

    def import_profile(self):
        data, msg = self.profile_mgr.import_profile('default')
        if data:
            self.theme_dropdown.setCurrentText(data.get('theme', 'dark.qss'))
            self.safe_checkbox.setChecked(data.get('safe_mode', False))
