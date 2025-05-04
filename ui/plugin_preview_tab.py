
from PySide6.QtWidgets import QTabWidget, QWidget, QVBoxLayout, QListWidget
import os
from ui.plugin_ui_renderer import render_ui_from_yaml

class PluginPreviewTab(QWidget):
    def __init__(self, plugin_dir="plugins"):
        super().__init__()
        self.plugin_dir = plugin_dir
        self.layout = QVBoxLayout()
        self.list = QListWidget()
        self.list.itemClicked.connect(self.load_plugin_ui)
        self.layout.addWidget(self.list)
        self.setLayout(self.layout)
        self.refresh()

    def refresh(self):
        self.list.clear()
        if not os.path.isdir(self.plugin_dir):
            return
        for name in os.listdir(self.plugin_dir):
            path = os.path.join(self.plugin_dir, name)
            if os.path.isdir(path) and os.path.exists(os.path.join(path, "ui.yaml")):
                self.list.addItem(name)

    def load_plugin_ui(self, item):
        plugin_name = item.text()
        ui_path = os.path.join(self.plugin_dir, plugin_name, "ui.yaml")
        preview_widget = render_ui_from_yaml(ui_path)
        if self.layout.count() > 1:
            old = self.layout.itemAt(1).widget()
            if old: old.setParent(None)
        self.layout.addWidget(preview_widget)
