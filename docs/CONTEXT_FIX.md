# Context-Aware Subtasks - The Fix

## The Problem You Identified

When you asked for a Next.js app called "SimpleWeather", the agent:
- ✗ Created Python files (`form_component.py`, `weather_fetcher.py`)
- ✗ Put files in the wrong location (workspace root instead of `SimpleWeather/`)
- ✗ Lost track that it was building Next.js
- ✗ Each subtask had no memory of the previous steps

## Why This Happened

**Before Fix:**
Each subtask ran in complete isolation with ZERO context:

```python
# Step 5 only got this:
subtask = "Create a form component with input for city name..."
run_conversation(subtask)  # No context about Next.js or SimpleWeather!
```

The agent had no idea:
- What framework (Next.js? Python? React?)
- What folder to work in
- What was already completed
- What the overall goal was

## The Solution

**After Fix:**
Each subtask now gets full context:

```
OVERALL GOAL: Create a Next.js 14 app called SimpleWeather that shows weather...
FRAMEWORK: Next.js
LANGUAGE: JavaScript
PROJECT FOLDER: SimpleWeather
IMPORTANT: All files must go inside the 'SimpleWeather' folder!

PROGRESS: Step 5 of 8

COMPLETED STEPS:
  ✓ Step 1: Create project folder named SimpleWeather
  ✓ Step 2: Initialize npm project in SimpleWeather folder
  ✓ Step 3: Install Next.js and dependencies
  ✓ Step 4: Create pages folder and index.js

CURRENT TASK: Create a form component with input for city name...

REMINDER: Work inside 'SimpleWeather/' folder. Use paths like 'SimpleWeather/components/Form.js'
```

## What Changed

### 1. Project Context Extraction (agent_client.py:542-583)
```python
def _extract_project_context(self, user_prompt):
    # Detects: Next.js, React, Flask, Express, Django, Vue
    # Extracts: Project name from "called X" or "named X"
    # Determines: Language (JavaScript vs Python)
```

**Example:**
- Input: "Create a Next.js app called MyApp"
- Extracts: `{framework: 'Next.js', project_name: 'MyApp', language: 'JavaScript'}`

### 2. Contextual Prompt Builder (agent_client.py:585-616)
```python
def _build_contextual_prompt(self, original_request, project_context,
                             current_subtask, completed_steps, ...):
    # Builds a rich context prompt for each subtask
    # Includes: framework, project folder, completed steps, reminders
```

### 3. Context Preservation (agent_client.py:516-524)
```python
# Each subtask gets:
context_prompt = self._build_contextual_prompt(
    original_request=user_prompt,      # "Create Next.js app called SimpleWeather..."
    project_context=project_context,    # {framework: 'Next.js', ...}
    current_subtask=subtask,            # "Create form component..."
    completed_steps=completed_steps,    # ["Step 1: Created folder", ...]
    step_number=i,
    total_steps=len(subtasks)
)
```

### 4. System Prompt Updates (system.md)
- Emphasizes reading context carefully
- Reminds about project folder structure
- Shows how to use paths correctly
- Explains command execution in project folders

## How It Works Now

### Example: "Create a React app called TodoApp with components"

**Step 1:** Create project folder
```
Context sent to model:
- GOAL: Create React app called TodoApp...
- FRAMEWORK: React
- PROJECT FOLDER: TodoApp
- TASK: Create project folder
Result: ✓ Creates TodoApp/
```

**Step 2:** Initialize npm
```
Context sent to model:
- GOAL: Create React app called TodoApp...
- FRAMEWORK: React
- PROJECT FOLDER: TodoApp
- COMPLETED: Step 1 created folder
- TASK: Initialize npm
Result: ✓ Runs "cd TodoApp && npm init -y"
```

**Step 3:** Create component
```
Context sent to model:
- GOAL: Create React app called TodoApp...
- FRAMEWORK: React
- PROJECT FOLDER: TodoApp
- LANGUAGE: JavaScript
- COMPLETED: Steps 1-2 (folder created, npm initialized)
- TASK: Create a TodoItem component
- REMINDER: Use paths like 'TodoApp/src/components/TodoItem.js'
Result: ✓ Creates TodoApp/src/components/TodoItem.js (CORRECT!)
```

## Supported Frameworks

The context extractor recognizes:
- **Next.js** / React / Vue
- **Flask** / Django
- **Express.js**
- Falls back to language detection (Python, JavaScript, Node)

## Supported Project Name Patterns

Extracts project names from:
- "Create a X app **called ProjectName**"
- "Build a Y **named MyProject**"
- "Make a Z app **called my-app**"

## Benefits

✅ **Maintains technology choice** - No more Python in a Next.js project
✅ **Correct file paths** - Files go in the right folders
✅ **Progress awareness** - Each step knows what's been done
✅ **Folder structure** - Understands project hierarchy
✅ **Command execution** - Runs commands in the right directory

## Try It Now

Restart your app and try:
```
> Create a Next.js 14 app called WeatherApp with a homepage
```

You should see:
- All files created inside `WeatherApp/`
- Only JavaScript/JSX files (no Python!)
- Proper Next.js structure (pages/, components/, etc.)
- Commands run with `cd WeatherApp &&`
