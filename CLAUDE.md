# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a local autonomous AI system that runs a Qwen 2.5 7B model (GGUF format) through llama-server and provides a PySide6 GUI interface for interacting with the agent. The agent has sandboxed file system access to the workspace directory and can perform file operations via function calling.

The system features intelligent task decomposition that automatically breaks complex requests into focused subtasks, with architecture planning to ensure proper component relationships and data flow.

## Running the System

**Start llama-server + GUI** (from `C:\Apps\local-ai\workspace`):
```batch
start_local_ai.bat
```

This launches llama-server on port 8080 with the Qwen model, waits 3 seconds, then starts the GUI.

**Run only GUI** (if llama-server already running):
```batch
cd gui
python main.py
```

**Test agent directly** (no GUI):
```python
from agent_client import AgentClient
agent = AgentClient()
result = agent.ask("Create a file called test.txt")
```

## Architecture

### Core Components

1. **Agent Client** (`agent_client.py`):
   - `AgentClient` class handles all LLM interactions
   - Communicates with llama-server at `http://127.0.0.1:8080/v1/chat/completions`
   - Implements function calling with five tools: `read_file`, `write_file`, `list_dir`, `create_directory`, `execute_command`
   - Loads system prompt from `system.md` which defines tool usage and workspace constraints
   - `safe_path()` function prevents path traversal attacks by validating all paths are within the workspace
   - Three execution modes:
     - `ask()`: Single-shot request/response
     - `run_conversation()`: Multi-turn conversation allowing agent to execute multiple steps
     - `run_with_subtasks()`: Intelligent task decomposition with architecture planning (default mode)

2. **GUI Application** (`gui/` directory):
   - Built with PySide6 (Qt for Python)
   - `main.py`: Entry point that launches the Qt application
   - `app_window.py`: Main window with split view (file browser + chat)
   - `chat_panel.py`: Terminal-style chat interface with dark theme
   - `file_browser.py`: File system tree view of the workspace
   - `api_client.py`: Wrapper around `AgentClient` that formats responses for the GUI
   - `agent_worker.py`: QThread worker that runs agent conversations in background, emitting progress signals to keep GUI responsive

3. **System Prompt** (`system.md`):
   - Defines the agent's behavior and constraints
   - Specifies workspace path and path handling rules
   - Documents available tools and JSON-only tool call format
   - Includes example tool call for model reference

### Key Design Patterns

- **Workspace Sandboxing**: All file operations are restricted to `C:\Apps\local-ai\workspace` via `safe_path()` validation
- **Function Calling Flow**: User message → AgentClient → llama-server → tool call JSON → `_execute_tool()` → return result → append to conversation → continue until text response
- **GUI-Agent Separation**: The GUI (`LocalAIClient`) wraps the core `AgentClient` to transform raw tool outputs into user-friendly messages
- **Threaded Execution**: GUI uses `AgentWorker` (QThread) to run agent in background, emitting progress signals for real-time updates
- **Intelligent Task Decomposition**: Complex requests trigger three-phase execution:
  1. **Architecture Planning**: LLM designs component relationships, data flow, and dependencies (agent_client.py:825)
  2. **Task Breakdown**: LLM creates 5-8 focused subtasks based on architecture (agent_client.py:465)
  3. **Sequential Execution**: Each subtask runs with full context (architecture + completed steps + created files)
- **Cache Busting**: Random request IDs prevent llama-server from reusing cached conversation context (agent_client.py:493)

## Development Notes

### Path Handling & Security
- The workspace is hardcoded to `C:\Apps\local-ai\workspace` in multiple files (agent_client.py:6, api_client.py:6)
- All paths passed to tools must be relative to workspace (no leading `/` or `\`)
- The agent is instructed via system prompt to never use absolute paths
- `safe_path()` sanitizes and validates paths before file operations:
  - Strips leading slashes/backslashes (agent_client.py:14)
  - Resolves to absolute path and validates it starts with WORKSPACE
  - Raises exception for path traversal attempts (agent_client.py:18)
- Shell commands run in workspace directory via `cwd=WORKSPACE` (agent_client.py:179)
- Command timeout: 60 seconds to prevent infinite loops (agent_client.py:182)

### Model Configuration & Constraints
- Model: Qwen 2.5 7B Instruct (Q4_0 quantization)
- Template: Custom Jinja template (`qwen_template.jinja` in parent directory)
- Temperature: 0 (deterministic responses for reproducibility)
- Tool choice: "auto" (model decides when to use tools)

**Critical behavioral rules enforced via system.md**:
- Agent must do ONLY what current task asks (no extra steps)
- ALL paths must include project folder prefix (e.g., `MyProject/pages/index.js` not `pages/index.js`)
- Use correct relative import paths (pages/ imports from `../components/`, not `./components/`)
- DO NOT be "helpful" by doing future steps early
- Tool calls must be JSON only (no markdown)

**Testing and iteration workflow** (NEW):
- After creating project files, agent runs `npm install` / `pip install`
- Runs dev server (`npm run dev`, `python app.py`, etc.) to check for errors
- If errors found (import errors, syntax errors), agent fixes them immediately
- Re-runs the command to verify fix worked
- Repeats until project runs without errors
- Stops if same error repeats 3 times (prevents infinite loops)

### Execution Flow Details

**Simple Tasks** (< 15 words or keywords like "create a file"):
- Bypasses planning phase
- Runs directly via `run_conversation()`
- Completes in 5-10 seconds

**Complex Tasks** (multi-step projects):
1. Architecture planning call (agent_client.py:825):
   - Analyzes component relationships and data flow
   - Temperature: 0.3, timeout: 90s, max_tokens: 500
2. Task breakdown call (agent_client.py:465):
   - Creates numbered list of 5-10 subtasks (includes install and testing steps)
   - Temperature: 0, timeout: 60s, max_tokens: 400
3. Subtask execution loop (agent_client.py:552):
   - Each subtask gets contextual prompt with architecture, completed steps, and created files
   - **File creation subtasks**: Stop after 1 write action (efficient)
   - **Testing/fixing subtasks**: Continue until test passes or 3 identical errors occur (iterative)
   - Detects error loops and stops after 3 identical errors (agent_client.py:360)
   - Max 15 turns per subtask (agent_client.py:30)

**Progress Events** (emitted by `AgentWorker` to GUI):
- `PLANNING`: Task decomposition in progress
- `ARCHITECTURE`: Architecture plan created
- `PLAN`: Subtask list created
- `SUBTASK_START/DONE`: Individual subtask lifecycle
- `WRITE_FILE/READ_FILE/LIST_DIR/CREATE_DIR/EXECUTE`: Tool executions
- `MODEL_OUTPUT`: Text responses from LLM
- `ERROR/WARNING`: Error conditions
- `COMPLETE`: All subtasks finished
- `NEXT_STEPS`: User instructions for npm install, etc.

### Adding New Tools
To add a new tool for the agent:
1. Define the function schema in both tools lists in `AgentClient` (lines ~40 and ~207)
2. Add tool execution in `AgentClient._execute_tool()` method (agent_client.py:397)
3. Update `system.md` to document the new tool for the model
4. Add event formatting in `MainWindow.on_progress()` if needed for GUI display (app_window.py:80)

### Context-Aware Subtask Prompts

Each subtask receives rich context via `_build_contextual_prompt()` (agent_client.py:653):
- Original user request
- Detected framework (Next.js, React, Flask, etc.)
- Detected project name and folder
- Architecture plan (components, connections, data flow)
- Recommended folder structure for the framework
- Progress tracker (step X of Y)
- List of completed steps
- Registry of created files (available for reading)
- Current task with strict "do only this" instructions
- Path requirements reminders

This ensures each subtask understands:
- What files exist and can be imported
- How components should connect
- What data flows between components
- Where files should be placed in the folder structure

### GUI Customization
- Chat panel uses terminal aesthetic (dark background, green text)
- Styles defined inline in `chat_panel.py` (consider extracting to `styles.qss`)
- File browser auto-refreshes after each message to show agent's file changes
- Split view sizes: 250px (file browser) / 850px (chat area)
- Worker thread prevents GUI freezing during long operations
- Input field disabled while agent is working (app_window.py:65)

### Framework Detection & Folder Structures

The agent automatically detects frameworks from user prompts via `_extract_project_context()` (agent_client.py:610):
- **Supported frameworks**: Next.js, React, Vue, Flask, Django, Express.js
- **Detection method**: Keyword matching in user prompt (case-insensitive)
- **Extracts**: Framework, project name (from "called X" or "named X"), language

Each framework has a predefined folder structure in `_get_folder_structure()` (agent_client.py:718):
- Structures include proper directories for pages, components, API routes, static files, etc.
- Structure is provided to every subtask for reference
- Helps agent place files in correct locations

After completion, agent provides framework-specific next steps:
- Node.js projects: `cd {project} && npm install && npm run dev`
- Python projects: `cd {project} && pip install -r requirements.txt && python app.py`

## Dependencies

Required Python packages:
- PySide6 (Qt GUI framework)
- requests (HTTP client for llama-server API)

External requirements:
- llama-server.exe (llama.cpp server, must be in PATH or parent directory)
- Qwen 2.5 7B model file (GGUF format, expected at `C:\Apps\local-ai\models\qwen2.5-7b-instruct-q4_0.gguf`)
- Jinja chat template file (`qwen_template.jinja` in workspace directory)
