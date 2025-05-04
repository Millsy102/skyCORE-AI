# 📦 Module imports
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QTextEdit, QPushButton,
    QSplitter, QFileSystemModel, QTreeView, QTabWidget, QMenu, QPlainTextEdit, QMessageBox,
    QFileDialog, QLineEdit, QInputDialog
)
from PySide6.QtCore import Qt, QDir, QModelIndex
from PySide6.QtGui import QAction
import os

from src.ai_controller import AIController
from src.plugin_executor import PluginExecutor

ALLOWED_EXTENSIONS = [".py", ".txt", ".json", ".md", ".yaml"]

class CodeEditor(QPlainTextEdit):
    def __init__(self, path=None, parent=None):
        super().__init__(parent)
        self.path = path
        self.changed = False
        self.textChanged.connect(self.mark_unsaved)

    def mark_unsaved(self):
        if not self.changed:
            self.changed = True
            tab_widget = self.parent().parent().editor_tabs
            index = tab_widget.indexOf(self)
            if index >= 0:
                title = tab_widget.tabText(index)
                if not title.endswith("*"):
                    tab_widget.setTabText(index, title + "*")

    def reset_flag(self):
        self.changed = False
        tab_widget = self.parent().parent().editor_tabs
        index = tab_widget.indexOf(self)
        if index >= 0 and self.path:
            tab_widget.setTabText(index, os.path.basename(self.path))

class SkyDevStudioTab(QWidget):
    def __init__(self, runtime):
        super().__init__()
        self.runtime = runtime
        self.controller = AIController()
        self.executor = PluginExecutor()

        layout = QHBoxLayout(self)
        splitter = QSplitter(Qt.Horizontal)

        # LEFT PANEL
        self.prompt_input = QTextEdit()
        self.response_output = QTextEdit()
        self.response_output.setReadOnly(True)
        self.send_btn = QPushButton("Run SkyDev AI")
        self.send_btn.clicked.connect(self.run_skydev_ai)

        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.addWidget(self.prompt_input)
        left_layout.addWidget(self.send_btn)
        left_layout.addWidget(self.response_output)

        # RIGHT PANEL
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.currentPath())
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(os.path.abspath(".")))
        self.tree.doubleClicked.connect(self.open_file_from_tree)

        self.editor_tabs = QTabWidget()
        self.plugin_input = QLineEdit()
        self.plugin_input.setPlaceholderText("Optional plugin input")

        self.inject_btn = QPushButton("Inject to AI")
        self.run_plugin_btn = QPushButton("Run Plugin")
        self.save_btn = QPushButton("Save File")
        self.save_all_btn = QPushButton("Save All Tabs")

        self.inject_btn.clicked.connect(self.inject_active_code)
        self.run_plugin_btn.clicked.connect(self.run_plugin_code)
        self.save_btn.clicked.connect(self.save_active_code)
        self.save_all_btn.clicked.connect(self.save_all_tabs)

        right_layout.addWidget(self.tree)
        right_layout.addWidget(self.editor_tabs)
        right_layout.addWidget(self.plugin_input)
        right_layout.addWidget(self.inject_btn)
        right_layout.addWidget(self.run_plugin_btn)
        right_layout.addWidget(self.save_btn)
        right_layout.addWidget(self.save_all_btn)

        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        layout.addWidget(splitter)

    def open_file_from_tree(self, index: QModelIndex):
        file_path = self.model.filePath(index)
        if os.path.isfile(file_path) and os.path.splitext(file_path)[1].lower() in ALLOWED_EXTENSIONS:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            editor = CodeEditor(path=file_path, parent=self)
            editor.setPlainText(content)
            self.editor_tabs.addTab(editor, os.path.basename(file_path))
            self.editor_tabs.setCurrentWidget(editor)
            self.setup_tab_context(editor)

    def setup_tab_context(self, editor):
        editor.setContextMenuPolicy(Qt.CustomContextMenu)
        editor.customContextMenuRequested.connect(lambda pos: self.tab_context_menu(pos, editor))

    def tab_context_menu(self, pos, editor):
        menu = QMenu()
        rename = QAction("Rename Tab")
        close = QAction("Close Tab")
        reload = QAction("Reload File")

        explain = QAction("Explain with AI")
        rewrite = QAction("Refactor with AI")
        inject = QAction("Inject to AI")

        rename.triggered.connect(lambda: self.rename_tab(editor))
        close.triggered.connect(lambda: self.close_tab(editor))
        reload.triggered.connect(lambda: self.reload_tab(editor))

        explain.triggered.connect(lambda: self.ai_action(editor.toPlainText(), "Explain this code"))
        rewrite.triggered.connect(lambda: self.ai_action(editor.toPlainText(), "Rewrite this cleaner"))
        inject.triggered.connect(lambda: self.inject_to_prompt(editor.toPlainText(), "Injected Code"))

        menu.addAction(rename)
        menu.addAction(close)
        menu.addAction(reload)
        menu.addSeparator()
        menu.addAction(explain)
        menu.addAction(rewrite)
        menu.addAction(inject)
        menu.exec(editor.mapToGlobal(pos))

    def rename_tab(self, editor):
        index = self.editor_tabs.indexOf(editor)
        if index >= 0:
            name, ok = QInputDialog.getText(self, "Rename Tab", "New Tab Name:")
            if ok and name:
                self.editor_tabs.setTabText(index, name)

    def close_tab(self, editor):
        index = self.editor_tabs.indexOf(editor)
        if editor.changed:
            confirm = QMessageBox.question(self, "Unsaved Changes", "Close without saving?")
            if confirm != QMessageBox.Yes:
                return
        self.editor_tabs.removeTab(index)

    def reload_tab(self, editor):
        if editor.path:
            try:
                with open(editor.path, "r", encoding="utf-8") as f:
                    editor.setPlainText(f.read())
                editor.reset_flag()
            except Exception as e:
                QMessageBox.warning(self, "Reload Failed", str(e))

    def save_all_tabs(self):
        for i in range(self.editor_tabs.count()):
            editor = self.editor_tabs.widget(i)
            if isinstance(editor, CodeEditor) and editor.changed:
                self.save_editor(editor)

    def save_active_code(self):
        editor = self.editor_tabs.currentWidget()
        if isinstance(editor, CodeEditor):
            self.save_editor(editor)

    def save_editor(self, editor):
        tab_index = self.editor_tabs.indexOf(editor)
        tab_name = self.editor_tabs.tabText(tab_index).replace("*", "")
        save_path = QFileDialog.getSaveFileName(self, "Save File", tab_name)[0]
        if save_path:
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(editor.toPlainText())
            editor.path = save_path
            editor.reset_flag()
            QMessageBox.information(self, "Saved", f"File saved to {save_path}")

    def ai_action(self, code, task):
        combined = f"{task}:"
        self.response_output.append(f"📄 Task Output:\n{code}")
        result = self.controller.respond(combined)
        self.response_output.append(f"🧠 {task} → {code.strip()}")
        self.response_output.append(f"🧪 Output:\n{result['text']}")

    def inject_to_prompt(self, code, task=""):
        if task:
            self.prompt_input.append(f"💬 {task}: {code}")
        self.prompt_input.append(f"🛠️ Raw Code:\n{code}")
        self.prompt_input.append(f"🧠 Memory Input:\n{code}")

    def inject_active_code(self):
        editor = self.editor_tabs.currentWidget()
        if editor:
            self.inject_to_prompt(editor.toPlainText(), "Active Editor")

    def run_plugin_code(self):
        editor = self.editor_tabs.currentWidget()
        if editor:
            code = editor.toPlainText()
            tmp_path = "_temp_plugin_run.py"
            with open(tmp_path, 'w', encoding='utf-8') as f:
                f.write(code)
            try:
                input_text = self.plugin_input.text() or "Test Input"
                output = self.executor.run("temp_plugin_run", input_text)
                self.response_output.append(f"▶️ Output: {output}")
            except Exception as e:
                self.response_output.append(f"❌ Execution Error: {str(e)}")
            os.remove(tmp_path)

    def run_skydev_ai(self):
        prompt = self.prompt_input.toPlainText()
        response = self.controller.respond(prompt)
        self.response_output.append(f"> {prompt}")
        self.response_output.append(f"✅ Result:\n{response['text']}")
