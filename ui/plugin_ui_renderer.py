
import yaml
from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget

def render_ui_from_yaml(yaml_path):
    try:
        with open(yaml_path, "r") as f:
            data = yaml.safe_load(f)

        layout = QVBoxLayout()
        for item in data.get("layout", []):
            widget_type = item.get("type")
            label = item.get("label", "Unnamed")

            if widget_type == "label":
                layout.addWidget(QLabel(label))
            elif widget_type == "button":
                layout.addWidget(QPushButton(label))
            else:
                layout.addWidget(QLabel(f"[Unknown widget: {widget_type}]"))

        container = QWidget()
        container.setLayout(layout)
        return container
    except Exception as e:
        err = QWidget()
        err.setLayout(QVBoxLayout())
        err.layout().addWidget(QLabel(f"UI Load Failed: {e}"))
        return err
