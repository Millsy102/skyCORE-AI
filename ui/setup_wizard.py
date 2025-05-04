from PySide6.QtWidgets import QWizard, QWizardPage, QLabel, QVBoxLayout, QLineEdit, QCheckBox

class SetupWizard(QWizard):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("skyCORE-AI Setup Wizard")
        self.addPage(self.welcome_page())
        self.addPage(self.config_page())
        self.addPage(self.finish_page())

    def welcome_page(self):
        page = QWizardPage()
        page.setTitle("Welcome to skyCORE-AI")
        layout = QVBoxLayout()
        layout.addWidget(QLabel("This wizard will guide you through initial setup."))
        page.setLayout(layout)
        return page

    def config_page(self):
        page = QWizardPage()
        page.setTitle("Basic Configuration")
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Enter your default model:"))
        layout.addWidget(QLineEdit("gpt-4"))
        layout.addWidget(QLabel("Enable Safe Mode by default:"))
        layout.addWidget(QCheckBox("Safe Mode"))
        page.setLayout(layout)
        return page

    def finish_page(self):
        page = QWizardPage()
        page.setTitle("Setup Complete")
        layout = QVBoxLayout()
        layout.addWidget(QLabel("skyCORE-AI is ready. Launching..."))
        page.setLayout(layout)
        return page