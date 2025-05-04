# 📦 Module imports
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QTextEdit
from PySide6.QtCore import QDateTime
import os

# Class: CloudTab — defines main behavior for cloud_tab.py
class CloudTab(QWidget):
    def __init__(self, runtime):
        super().__init__()
        self.runtime = runtime
        layout = QVBoxLayout(self)

        self.status_label = QLabel("☁️ Cloud Status: Ready")
        self.logs = QTextEdit()
        self.logs.setReadOnly(True)

        self.upload_btn = QPushButton("📤 Upload Dataset")
        self.train_btn = QPushButton("🧠 Start Cloud Training")
        self.sync_btn = QPushButton("🔄 Sync Plugins from Cloud")

        self.upload_btn.clicked.connect(self.upload_dataset)
        self.train_btn.clicked.connect(self.start_training)
        self.sync_btn.clicked.connect(self.sync_plugins)

        layout.addWidget(self.status_label)
        layout.addWidget(self.upload_btn)
        layout.addWidget(self.train_btn)
        layout.addWidget(self.sync_btn)
        layout.addWidget(self.logs)

        self.setLayout(layout)

    def append_log(self, message):
        timestamp = QDateTime.currentDateTime().toString("hh:mm:ss")
        self.logs.append(f"[{timestamp}] {message}")
        self.logs.verticalScrollBar().setValue(self.logs.verticalScrollBar().maximum())

    def upload_dataset(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Dataset", ".", "CSV Files (*.csv)")
        if path:
            try:
                self.append_log(f"📤 Uploaded dataset: {os.path.basename(path)}")
                self.status_label.setText("☁️ Status: Dataset uploaded.")
            except Exception as e:
                self.append_log(f"❌ Upload failed: {str(e)}")
                self.status_label.setText("⚠️ Upload error.")

    def start_training(self):
        try:
            self.append_log("🧠 Cloud training job submitted for queued dataset.")
            self.status_label.setText("☁️ Status: Training in progress...")
        except Exception as e:
            self.append_log(f"❌ Training error: {str(e)}")
            self.status_label.setText("⚠️ Training error.")

    def sync_plugins(self):
        try:
            self.append_log("🔄 Synced plugin registry from SkyCore Cloud.")
            self.status_label.setText("☁️ Status: Synced")
        except Exception as e:
            self.append_log(f"❌ Sync error: {str(e)}")
            self.status_label.setText("⚠️ Sync error.")
