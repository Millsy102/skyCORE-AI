
# This module is reserved for mapping 3rd-party widget types to PySide equivalents
# Currently used in coordination with ui_reflector.py for emulated UIs

class WidgetBridge:
    @staticmethod
    def convert(widget_type, label='', options=None):
        from PySide6.QtWidgets import QLabel, QLineEdit, QTextEdit, QPushButton, QCheckBox, QComboBox

        if widget_type == 'label':
            return QLabel(label)
        elif widget_type == 'text':
            return QLineEdit()
        elif widget_type == 'textarea':
            return QTextEdit()
        elif widget_type == 'checkbox':
            return QCheckBox(label)
        elif widget_type == 'button':
            return QPushButton(label)
        elif widget_type == 'select':
            combo = QComboBox()
            if options:
                for opt in options:
                    combo.addItem(opt)
            return combo
        return QLabel(f"[Unknown widget: {widget_type}]")
