from PySide6.QtWidgets import QHBoxLayout, QMessageBox, QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton, QTextEdit, QHBoxLayout
import os
import yaml
from src.plugin_loader import PluginLoader

from src.plugin_dashboard_manager import PluginDashboardManager

class PluginsTab(QWidget):
    def __init__(self, runtime):
        
        self.manager = PluginDashboardManager()
        self.plugin_list = QTextEdit()
        self.plugin_list.setReadOnly(True)
        layout.addWidget(self.plugin_list)
        self.obs_btn = QPushButton("🎮 Launch Overlay")
        self.obs_btn.clicked.connect(self.launch_overlay)
        layout.addWidget(self.obs_btn)
        self.panel_btn = QPushButton("📊 Plugin Overlay Panel")
        self.panel_btn.clicked.connect(self.launch_overlay_panel)
        layout.addWidget(self.panel_btn)

        for plugin in self.manager.plugins:
            self.plugin_list.append(f"{plugin.name} ({'🟢' if plugin.active else '🔴'}) → " + ", ".join(plugin.triggers))

        ctrl_row = QHBoxLayout()
        self.toggle_input = QLineEdit()
        self.toggle_input.setPlaceholderText("Plugin name")
        ctrl_row.addWidget(self.toggle_input)

        toggle_btn = QPushButton("🔄 Toggle")
        toggle_btn.clicked.connect(self.toggle_plugin)
        ctrl_row.addWidget(toggle_btn)

        delete_btn = QPushButton("🗑️ Delete")
        delete_btn.clicked.connect(self.delete_plugin)
        ctrl_row.addWidget(delete_btn)

        layout.addLayout(ctrl_row)
    super().__init__()
    layout = QVBoxLayout(self)
    self.loader = PluginLoader()
        layout.addWidget(QLabel('🧩 Installed Plugins'))
        self.plugin_list = QListWidget()
        self.plugin_list.addItems(self.loader.plugins.keys())
        self.plugin_list.itemClicked.connect(self.display_plugin)
        layout.addWidget(self.plugin_list)
        self.obs_btn = QPushButton("🎮 Launch Overlay")
        self.obs_btn.clicked.connect(self.launch_overlay)
        layout.addWidget(self.obs_btn)
        self.panel_btn = QPushButton("📊 Plugin Overlay Panel")
        self.panel_btn.clicked.connect(self.launch_overlay_panel)
        layout.addWidget(self.panel_btn)

        btns = QHBoxLayout()
        self.reload_btn = QPushButton("Reload Plugins")
        self.reload_btn.clicked.connect(self.reload)
        btns.addWidget(self.reload_btn)

        self.enable_btn = QPushButton("Toggle Enable")
        self.enable_btn.clicked.connect(self.toggle_plugin)
        btns.addWidget(self.enable_btn)

        layout.addLayout(btns)

        self.code_preview = QTextEdit()
        self.code_preview.setReadOnly(True)
        layout.addWidget(QLabel("📄 plugin.py Preview"))
        layout.addWidget(self.code_preview)

        self.schema_preview = QTextEdit()
        self.schema_preview.setReadOnly(True)
        layout.addWidget(QLabel("📜 ui.yaml Preview"))
        layout.addWidget(self.schema_preview)

    def reload(self):
        self.loader.load_plugins()
        self.plugin_list.clear()
        self.plugin_list.addItems(self.loader.plugins.keys())

    def toggle_plugin(self):
        name = self.plugin_list.currentItem().text()
        if name in self.loader.plugins:
            del self.loader.plugins[name]
        else:
            self.loader.load_plugins()  # reload all
        self.reload()

    def display_plugin(self, item):
        name = item.text()
        plugin_path = os.path.join("plugins", name, "plugin.py")
        ui_path = os.path.join("plugins", name, "ui.yaml")
        self.code_preview.setText(open(plugin_path).read() if os.path.exists(plugin_path) else "plugin.py not found")
        if os.path.exists(ui_path):
            with open(ui_path) as f:
                try:
                    parsed = yaml.safe_load(f)
                    self.schema_preview.setText(yaml.dump(parsed, sort_keys=False))
                except:
                    self.schema_preview.setText("Invalid YAML")
        else:
            self.schema_preview.setText("ui.yaml not found")


    def toggle_plugin(self):
        name = self.toggle_input.text().strip()
        if not name: return
        result = ""
        plugin_file = os.path.join("plugins", name, "plugin.py")
        disabled_file = plugin_file.replace("plugin.py", "plugin_disabled.py")
        if os.path.exists(plugin_file):
            result = self.manager.deactivate_plugin(name)
        elif os.path.exists(disabled_file):
            result = self.manager.activate_plugin(name)
        else:
            result = "⚠️ Not found"
        QMessageBox.information(self, "Plugin", result)

        if hasattr(self.runtime, "load_plugins"):
            self.runtime.load_plugins()
            self.plugin_list.append("🔁 Plugins reloaded.")

        self.toggle_input.clear()

    def delete_plugin(self):
        name = self.toggle_input.text().strip()
        if not name: return
        confirm = QMessageBox.question(self, "Confirm", f"Really delete plugin '{name}'?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            result = self.manager.delete_plugin(name)
            QMessageBox.information(self, "Plugin", result)

        if hasattr(self.runtime, "load_plugins"):
            self.runtime.load_plugins()
            self.plugin_list.append("🔁 Plugins reloaded.")

            self.toggle_input.clear()
    

    def launch_overlay(self):
        import subprocess
        overlay_script = os.path.join("overlays", "launch_overlay.py")
        if os.path.exists(overlay_script):
            subprocess.Popen(["python", overlay_script])
            QMessageBox.information(self, "Overlay", "🎮 Overlay launched.")
        else:
            QMessageBox.warning(self, "Overlay", "❌ Overlay script not found.")
    

    def launch_overlay_panel(self):
        import subprocess
        panel_script = os.path.join("overlays", "panel.py")
        if os.path.exists(panel_script):
            subprocess.Popen(["python", panel_script])
            QMessageBox.information(self, "Overlay", "📊 Overlay panel launched.")
        else:
            QMessageBox.warning(self, "Overlay", "❌ Panel script not found.")
    