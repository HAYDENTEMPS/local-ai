from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QSplitter, QLineEdit
)
from PySide6.QtCore import Qt

from chat_panel import ChatPanel
from file_browser import FileBrowser
from api_client import LocalAIClient
from agent_worker import AgentWorker


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Local Autonomous AI")
        self.setMinimumSize(1100, 700)

        # The agent-aware client
        self.client = LocalAIClient()

        # --- Layout Setup ---
        central = QWidget()
        layout = QHBoxLayout()
        central.setLayout(layout)

        splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(splitter)

        # LEFT → File Browser
        self.browser = FileBrowser()
        splitter.addWidget(self.browser)

        # RIGHT → Chat + Input Box
        right_side = QWidget()
        right_layout = QVBoxLayout()
        right_side.setLayout(right_layout)

        self.chat = ChatPanel()
        right_layout.addWidget(self.chat)

        self.input = QLineEdit()
        self.input.setPlaceholderText("Ask your local AI…")
        self.input.returnPressed.connect(self.send_message)
        right_layout.addWidget(self.input)

        splitter.addWidget(right_side)
        splitter.setSizes([250, 850])

        self.setCentralWidget(central)

        # Track worker thread
        self.worker = None

    # ------------------------------------------------------------
    # Handle user sending a message
    # ------------------------------------------------------------
    def send_message(self):
        text = self.input.text().strip()
        if not text:
            return

        # Don't allow new messages while agent is working
        if self.worker and self.worker.isRunning():
            self.chat.add_error("⚠ Agent is still working. Please wait...")
            return

        self.input.clear()
        self.chat.add_user_message(text)
        self.chat.add_progress("⏳ Agent is thinking...")

        # Create worker thread to run agent in background
        self.worker = AgentWorker(self.client.agent, text)
        self.worker.progress_update.connect(self.on_progress)
        self.worker.error_occurred.connect(self.on_error)
        self.worker.finished.connect(self.on_finished)
        self.worker.start()

    def on_progress(self, event_type: str, data):
        """Called from worker thread when agent makes progress"""
        # Format the progress update
        if event_type == "PLANNING":
            self.chat.add_progress(f"🔍 {data}")

        elif event_type == "ARCHITECTURE":
            self.chat.add_progress(f"🏗️  {data}")

        elif event_type == "PLAN":
            self.chat.add_progress(f"📋 {data}")

        elif event_type == "SUBTASK_START":
            self.chat.add_progress(f"\n▶ {data}")

        elif event_type == "SUBTASK_DONE":
            self.chat.add_progress(f"{data}")

        elif event_type == "COMPLETE":
            self.chat.add_ai_message(f"\n🎉 {data}")

        elif event_type == "NEXT_STEPS":
            self.chat.add_ai_message(f"\n📦 Next Steps:{data}")

        elif event_type == "MODEL_OUTPUT":
            # Only show if not empty
            if data and data.strip():
                self.chat.add_ai_message(data)

        elif event_type == "WRITE_FILE":
            self.chat.add_progress(f"  ✓ File written: {data}")

        elif event_type == "READ_FILE":
            preview = data[:100] + "..." if len(data) > 100 else data
            self.chat.add_progress(f"  ✓ Read file: {preview}")

        elif event_type == "LIST_DIR":
            dir_list = "\n".join(data) if isinstance(data, list) else str(data)
            self.chat.add_progress(f"  ✓ Listed directory")

        elif event_type == "CREATE_DIR":
            self.chat.add_progress(f"  ✓ Created directory: {data}")

        elif event_type == "EXECUTE":
            # Truncate long command outputs
            output = data[:200] + "..." if len(data) > 200 else data
            self.chat.add_progress(f"  ✓ Executed command")

        elif event_type == "ERROR":
            self.chat.add_error(f"✗ Error: {data}")

        elif event_type == "WARNING":
            self.chat.add_error(f"⚠ Warning: {data}")

    def on_error(self, error_msg: str):
        """Called when worker encounters an error"""
        self.chat.add_error(error_msg)

    def on_finished(self):
        """Called when agent completes all work"""
        # Refresh file browser to show any changes
        root = self.browser.model.rootPath()
        self.browser.model.setRootPath(root)
        self.browser.setRootIndex(self.browser.model.index(root))

        # Clean up worker
        if self.worker:
            self.worker.deleteLater()
            self.worker = None
