from PySide6.QtCore import QThread, Signal


class AgentWorker(QThread):
    """
    Worker thread that runs the agent conversation in the background.
    Emits signals for progress updates so the GUI stays responsive.
    """

    # Signals to communicate with main thread
    progress_update = Signal(str, object)  # (event_type, data)
    finished = Signal()
    error_occurred = Signal(str)  # Error message

    def __init__(self, agent, user_prompt):
        super().__init__()
        self.agent = agent
        self.user_prompt = user_prompt

    def run(self):
        """
        This runs in a background thread.
        Calls the agent and emits progress updates.
        """
        try:
            def callback(event_type, data):
                # Emit signal to update GUI from background thread
                self.progress_update.emit(event_type, data)

            # Use subtask-based execution for better performance
            self.agent.run_with_subtasks(self.user_prompt, progress_callback=callback)

        except Exception as e:
            # Emit error signal if something goes wrong
            self.error_occurred.emit(f"Worker error: {str(e)}")

        finally:
            # Always signal completion
            self.finished.emit()
