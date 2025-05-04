
import yaml
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox, QTextEdit, QComboBox

class UIReflector:
    def __init__(self, *args, **kwargs):
        return f"🔧 __init__ executed with args={args} kwargs={kwargs}"

    def render_from_yaml(self, yaml_path):
        try:
            with open(yaml_path, 'r') as f:
                ui_schema = yaml.safe_load(f)
        except Exception as e:
            return self._error_widget(f"Error loading UI YAML: {e}")

        return self._build_widget_from_schema(ui_schema)

    def _build_widget_from_schema(self, schema):
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        for field in schema.get('fields', []):
            field_type = field.get('type')
            label_text = field.get('label', '')
            if field_type == 'text':
                layout.addWidget(QLabel(label_text))
                layout.addWidget(QLineEdit())
            elif field_type == 'textarea':
                layout.addWidget(QLabel(label_text))
                layout.addWidget(QTextEdit())
            elif field_type == 'checkbox':
                layout.addWidget(QCheckBox(label_text))
            elif field_type == 'select':
                layout.addWidget(QLabel(label_text))
                combo = QComboBox()
                for option in field.get('options', []):
                    combo.addItem(option)
                layout.addWidget(combo)
            elif field_type == 'button':
                layout.addWidget(QPushButton(label_text))

        return widget

    def _error_widget(self, message):
        error_widget = QWidget()
        layout = QVBoxLayout()
        error_widget.setLayout(layout)
        layout.addWidget(QLabel(message))
        return error_widget
