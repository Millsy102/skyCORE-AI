
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox

class TrainingTab(QWidget):
    def __init__(self, runtime):
        super().__init__()
        self.runtime = runtime
        layout = QVBoxLayout(self)
        self.dataset_path = ""
        self.upload_btn = QPushButton("📤 Upload Dataset")
        self.train_btn = QPushButton("🚀 Start Training")
        self.upload_btn.clicked.connect(self.upload_dataset)
        self.train_btn.clicked.connect(self.start_training)

        layout.addWidget(QLabel("📈 Model Training Panel"))
        layout.addWidget(self.upload_btn)
        layout.addWidget(self.train_btn)
        self.setLayout(layout)

    def upload_dataset(self):
        path, _ = QFileDialog.getOpenFileName(self, "Upload CSV", ".", "CSV (*.csv)")
        if path:
            self.dataset_path = path
            QMessageBox.information(self, "Uploaded", f"📁 Dataset ready: {path}")

    def start_training(self):
        if not self.dataset_path:
            QMessageBox.warning(self, "Missing", "⚠️ Upload a dataset first.")
            return
        QMessageBox.information(self, "Training", f"🚀 Training started with dataset: {self.dataset_path}")
