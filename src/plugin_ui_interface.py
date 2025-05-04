# 📦 Module imports
from PyQt5.QtWidgets import QWidget

# Class: PluginUIInterface — defines main behavior for plugin_ui_interface.py
class PluginUIInterface(QWidget):
# Function: __init__ — handles a core step in this module
    def __init__(self, plugin_name):
        super().__init__()
        self.plugin_name = plugin_name

# Function: get_widget — handles a core step in this module
    def get_widget(self):
    # 🏁 Returning result
        return self