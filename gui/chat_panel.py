from PySide6.QtWidgets import QTextEdit, QWidget, QVBoxLayout
from PySide6.QtCore import Qt

class ChatPanel(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        # QTextEdit allows selecting & copying text
        self.text = QTextEdit()
        self.text.setReadOnly(True)

        # Style it (dark terminal aesthetic)
        self.text.setStyleSheet("""
            QTextEdit {
                background: #111;
                color: #0f0;
                font-family: Consolas, monospace;
                font-size: 14px;
                border: 1px solid #333;
            }
            QTextEdit QScrollBar {
                background: #222;
            }
        """)

        # ENABLE SELECTION & COPYING
        self.text.setTextInteractionFlags(
            Qt.TextSelectableByMouse |
            Qt.TextSelectableByKeyboard |
            Qt.TextBrowserInteraction
        )

        layout.addWidget(self.text)

    def add_user_message(self, msg: str):
        self.text.append(f"<span style='color:#f33;'>&gt; {msg}</span>")

    def add_ai_message(self, msg: str):
        self.text.append(f"<span style='color:#bbb;'>{msg}</span>")

    def add_progress(self, msg: str):
        """Add a progress update in a different color"""
        self.text.append(f"<span style='color:#3af;'>{msg}</span>")

    def add_error(self, msg: str):
        """Add an error message in red"""
        self.text.append(f"<span style='color:#f55;'>{msg}</span>")
