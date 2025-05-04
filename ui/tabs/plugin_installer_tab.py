from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox
import os
import importlib.util

class PluginInstallerTab(QWidget):
    def __init__(self, runtime):
        super().__init__()
        self.runtime = runtime
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("🔌 Plugin Installer (GitHub)"))

        self.input = QLineEdit()
        self.input.setPlaceholderText("Paste GitHub URL (e.g. https://github.com/user/repo.git)")
        layout.addWidget(self.input)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)

        install_btn = QPushButton("📥 Install Plugin")
        install_btn.clicked.connect(self.install_plugin)
        layout.addWidget(install_btn)

    def install_plugin(self):
        url = self.input.text().strip()
        if not url or "github.com" not in url:
            QMessageBox.warning(self, "Invalid", "Please enter a valid GitHub URL.")
            return

        try:
            from src.plugin_git_installer import PluginGitInstaller
            installer = PluginGitInstaller()
            result = installer.install_from_git(url)
            self.output.append(result)
        except Exception as e:
            self.output.append(f"❌ Error: {e}")
