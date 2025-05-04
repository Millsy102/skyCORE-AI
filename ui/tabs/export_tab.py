from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QFileDialog, QMessageBox
from src.plugin_vault import PluginVault
import os

class ExportTab(QWidget):
    def __init__(self, runtime):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("📤 Export Plugin Vault"))

        self.list = QListWidget()
        self.list.addItems(os.listdir("plugins"))
        layout.addWidget(self.list)

        export_btn = QPushButton("Export Selected Plugin")
        export_btn.clicked.connect(self.export_plugin)
        layout.addWidget(export_btn)

        self.vault = PluginVault()

    def export_plugin(self):
        selected = self.list.currentItem().text()
        zip_path = self.vault.export(selected)
        dest, _ = QFileDialog.getSaveFileName(self, "Save Plugin Zip", zip_path, "Zip Files (*.zip)")
        if dest:
            os.replace(zip_path, dest)
            QMessageBox.information(self, "Export", f"Exported to: {dest}")
