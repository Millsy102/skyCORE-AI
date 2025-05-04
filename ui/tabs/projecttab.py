
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTreeView, QFileSystemModel, QLabel, QMenu
from PySide6.QtCore import Qt, QPoint
import os

class ProjectTab(QWidget):
    def __init__(self, runtime):
        super().__init__()
        layout = QVBoxLayout(self)

        self.model = QFileSystemModel()
        self.model.setRootPath("plugins")
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index("plugins"))
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.context_menu)

        layout.addWidget(QLabel("📁 skyCORE-AI Project Files"))
        layout.addWidget(self.tree)
        self.setLayout(layout)

    def context_menu(self, point: QPoint):
        index = self.tree.indexAt(point)
        if not index.isValid():
            return
        menu = QMenu()
        menu.addAction("📂 Open")
        menu.addAction("🗑️ Delete")
        menu.exec(self.tree.viewport().mapToGlobal(point))
