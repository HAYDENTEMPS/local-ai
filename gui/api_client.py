import json
import sys
import os

# Dynamically detect local-ai root (two levels up from this file)
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(ROOT)

from workspace.agent_client import AgentClient  # import from real root


class LocalAIClient:

    def __init__(self):
        self.agent = AgentClient()

    def ask(self, text):
        """
        Run a multi-turn conversation and format all steps for display.
        """
        steps = self.agent.run_conversation(text)

        # Format all steps into a readable output
        output_parts = []

        for event, data in steps:
            if event == "MODEL_OUTPUT":
                output_parts.append(data)

            elif event == "WRITE_FILE":
                output_parts.append(f"✓ File written: {data}")

            elif event == "READ_FILE":
                # Truncate long file contents for display
                preview = data[:200] + "..." if len(data) > 200 else data
                output_parts.append(f"✓ Read file\n{preview}")

            elif event == "LIST_DIR":
                dir_list = "\n".join(data) if isinstance(data, list) else str(data)
                output_parts.append(f"✓ Directory contents:\n{dir_list}")

            elif event == "CREATE_DIR":
                output_parts.append(f"✓ Directory created: {data}")

            elif event == "EXECUTE":
                output_parts.append(f"✓ Command executed:\n{data}")

            elif event == "ERROR":
                output_parts.append(f"✗ Error: {data}")

            elif event == "WARNING":
                output_parts.append(f"⚠ Warning: {data}")

        return "\n\n".join(output_parts) if output_parts else "[No response]"
