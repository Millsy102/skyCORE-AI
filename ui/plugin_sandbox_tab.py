
from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton, QTextEdit
import os
import importlib.util
import traceback

class PluginSandboxTab(QWidget):
    def __init__(self, plugin_dir="plugins"):
        super().__init__()
        self.plugin_dir = plugin_dir
        self.layout = QVBoxLayout()
        self.list = QListWidget()
        self.run_btn = QPushButton("Run main.py (safe)")
        self.output = QTextEdit()
        self.output.setReadOnly(True)

        self.run_btn.clicked.connect(self.run_plugin)
        self.layout.addWidget(self.list)
        self.layout.addWidget(self.run_btn)
        self.layout.addWidget(self.output)
        self.setLayout(self.layout)
        self.refresh()

    def refresh(self):
        self.list.clear()
        if not os.path.isdir(self.plugin_dir):
            return
        for name in os.listdir(self.plugin_dir):
            path = os.path.join(self.plugin_dir, name)
            if os.path.isdir(path) and os.path.exists(os.path.join(path, "main.py")):
                self.list.addItem(name)

    def run_plugin(self):
        selected = self.list.currentItem()
        if not selected:
            self.output.setText("⚠️ No plugin selected.")
            return

        plugin_name = selected.text()
        plugin_path = os.path.join(self.plugin_dir, plugin_name, "main.py")

        try:
            spec = importlib.util.spec_from_file_location("main", plugin_path)
            plugin = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(plugin)
            if hasattr(plugin, "main"):
                result = plugin.main()
                self.output.setText(f"✅ Output:\n{result}")
            else:
                self.output.setText("⚠️ No main() function defined in plugin.")
        except Exception as e:
            self.output.setText("❌ Exception:\n" + traceback.format_exc())
