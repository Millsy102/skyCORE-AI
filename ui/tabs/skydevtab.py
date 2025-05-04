from PySide6.QtWidgets import QVBoxLayout, QPushButton, QFileDialog, QMessageBox
import subprocess, os

class SkyDevTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.btn_create = QPushButton("🔧 Create Plugin")
        self.btn_create.clicked.connect(self.make_plugin)
        layout.addWidget(self.btn_create)

        self.btn_lint = QPushButton("🧪 Lint Plugin")
        self.btn_lint.clicked.connect(self.lint_plugin)
        layout.addWidget(self.btn_lint)

        self.btn_test = QPushButton("🚀 Test Plugin")
        self.btn_test.clicked.connect(self.test_plugin)
        layout.addWidget(self.btn_test)

        self.setLayout(layout)

    def run_script(self, script, *args):
        full = os.path.abspath(os.path.join("builder", script))
        cmd = ["python", full] + list(args)
        try:
            out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)
            QMessageBox.information(self, "Output", out)
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Error", e.output)

    def make_plugin(self):
        name, ok = QFileDialog.getSaveFileName(self, "Plugin Name", "plugins/")
        if ok:
            self.run_script("plugin_maker.py", os.path.basename(name))

    def lint_plugin(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Plugin Folder")
        if folder:
            self.run_script("plugin_linter.py", folder)

    def test_plugin(self):
        folder = QFileDialog.getExistingDirectory(self, "Run Plugin")
        if folder:
            self.run_script("plugin_tester.py", folder)
