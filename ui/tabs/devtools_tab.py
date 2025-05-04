from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QComboBox, QFileDialog
from src.plugin_loader import PluginLoader
from src.plugin_executor import PluginExecutor

class DevToolsTab(QWidget):
    def __init__(self, runtime):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("🛠 Plugin DevTools"))

        self.plugin_dropdown = QComboBox()
        self.loader = PluginLoader()
        self.plugin_dropdown.addItems(self.loader.plugins.keys())
        layout.addWidget(self.plugin_dropdown)

        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("JSON input for plugin execute()")
        layout.addWidget(self.input_box)

        run_btn = QPushButton("▶️ Run Plugin")
        run_btn.clicked.connect(self.run_plugin)
        layout.addWidget(run_btn)

        self.result_box = QTextEdit()
        self.result_box.setReadOnly(True)
        layout.addWidget(self.result_box)

        validate_btn = QPushButton("🧪 Validate Syntax")
        validate_btn.clicked.connect(self.validate_plugin)
        layout.addWidget(validate_btn)

        template_btn = QPushButton("📦 Load Demo Plugin Template")
        template_btn.clicked.connect(self.load_template)
        layout.addWidget(template_btn)

    def run_plugin(self):
        name = self.plugin_dropdown.currentText()
        try:
            data = eval(self.input_box.text())
        except:
            self.result_box.setText("Invalid JSON input.")
            return
        result = PluginExecutor().run(name, data)
        self.result_box.setText(str(result))

    def validate_plugin(self):
        import py_compile, os
        name = self.plugin_dropdown.currentText()
        path = os.path.join("plugins", name, "plugin.py")
        try:
            py_compile.compile(path, doraise=True)
            self.result_box.setText(f"{name}/plugin.py syntax ✅ valid")
        except Exception as e:
            self.result_box.setText(f"❌ Syntax error:\n{e}")

    def load_template(self):
        demo = """class Plugin:
    def __init__(self):
        self.name = 'MyPlugin'
        self.triggers = ['hello', 'demo']

    def execute(self, input_data):
        return {'response': 'Hello from demo plugin!'}
"""
        path, _ = QFileDialog.getSaveFileName(self, "Save Plugin Template", "plugin.py", "Python Files (*.py)")
        if path:
            open(path, "w").write(demo)
