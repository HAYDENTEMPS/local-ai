# File Tracking & Folder Structure Awareness

## ✅ Now Your Agent Can:

### 1. **Track All Created Files**
The agent maintains a registry of every file and folder created during execution:
```
CREATED FILES (available for reference):
  📄 SimpleWeather/ (folder)
  📄 SimpleWeather/package.json
  📄 SimpleWeather/pages/ (folder)
  📄 SimpleWeather/pages/index.js
  📄 SimpleWeather/components/ (folder)
  📄 SimpleWeather/components/WeatherForm.js
```

### 2. **Know Framework-Specific Folder Structures**
For Next.js:
```
SimpleWeather/
├── pages/
│   ├── index.js          (homepage)
│   ├── _app.js           (app wrapper)
│   └── api/              (API routes)
├── components/           (React components)
├── public/               (static files)
├── styles/               (CSS files)
└── package.json
```

### 3. **Reference Previous Files**
Later steps can read and modify files created in earlier steps:
- Step 4 creates `WeatherForm.js`
- Step 6 needs to import it → knows it exists at `SimpleWeather/components/WeatherForm.js`
- Step 6 can use `read_file` to see how it's structured

### 4. **Maintain Organized Structure**
The agent sees the recommended structure and follows it automatically.

## Example Context (What the Agent Sees)

### Step 1 Context:
```
OVERALL GOAL: Create a Next.js 14 app called SimpleWeather...
FRAMEWORK: Next.js
LANGUAGE: JavaScript
PROJECT FOLDER: SimpleWeather

RECOMMENDED STRUCTURE for Next.js:
SimpleWeather/
├── pages/
├── components/
├── public/
├── styles/
└── package.json

PROGRESS: Step 1 of 6
CURRENT TASK: Create project folder named SimpleWeather
```

### Step 4 Context (Later in Process):
```
OVERALL GOAL: Create a Next.js 14 app called SimpleWeather...
FRAMEWORK: Next.js
PROJECT FOLDER: SimpleWeather

RECOMMENDED STRUCTURE for Next.js:
[structure diagram...]

PROGRESS: Step 4 of 6

COMPLETED STEPS:
  ✓ Step 1: Create project folder
  ✓ Step 2: Initialize npm
  ✓ Step 3: Install dependencies

CREATED FILES (available for reference):
  📄 SimpleWeather/ (folder)
  📄 SimpleWeather/package.json
  📄 SimpleWeather/node_modules/ (folder)
  📄 SimpleWeather/pages/ (folder)

CURRENT TASK: Create the homepage component

REMINDER:
  - Work inside 'SimpleWeather/' folder
  - Follow the recommended structure above
  - You can read/reference files listed in CREATED FILES
```

## How It Works

### File Tracking (agent_client.py:536-541)
```python
# After each subtask completes, extract created files
for event_type, data in subtask_steps:
    if event_type == "WRITE_FILE":
        created_files.append(data)
    elif event_type == "CREATE_DIR":
        created_files.append(f"{data}/ (folder)")
```

### Structure Templates (agent_client.py:646-751)
- Pre-defined folder structures for 6 frameworks
- Automatically shown to the agent in context
- Includes common folders and files with descriptions

### Context Building (agent_client.py:598-644)
Each subtask receives:
1. Original goal
2. Framework & language
3. Recommended folder structure
4. List of completed steps
5. **Registry of all created files**
6. Current task
7. Reminders about structure and file references

## Supported Frameworks

### Next.js
- pages/ for routes
- components/ for React components
- api/ for API routes
- public/ for static assets
- styles/ for CSS

### React
- src/ for source code
- components/ for components
- pages/ for page components
- public/ for static files

### Flask (Python)
- routes/ for endpoints
- templates/ for HTML
- static/ for CSS/JS
- models/ for database

### Express.js (Node)
- routes/ for endpoints
- controllers/ for logic
- models/ for data
- public/ for static files

### Django (Python)
- apps/ for Django apps
- static/ for assets
- templates/ for HTML

### Vue
- src/components/ for components
- src/views/ for pages
- src/router/ for routing
- src/store/ for state

## Benefits

### ✅ Organized Projects
The agent knows where files should go and follows best practices.

### ✅ File References Work
When creating a component that needs to import another:
```javascript
// Agent knows WeatherForm.js exists at components/
import WeatherForm from '../components/WeatherForm'
```

### ✅ No Scattered Files
Everything goes in the right place:
- Components in `components/`
- Pages in `pages/`
- Styles in `styles/`
- API routes in `pages/api/`

### ✅ Can Read Previous Work
If a later step needs to modify an earlier file:
1. Agent sees it in CREATED FILES
2. Uses `read_file` to read it
3. Modifies and uses `write_file` to update it

## Example Scenario

**Request:** "Create a Next.js weather app with a form component and weather display"

**Step 3 - Create Form Component:**
```
Agent sees:
- Structure: Put components in SimpleWeather/components/
- Created files: SimpleWeather/, pages/, etc.

Agent creates: SimpleWeather/components/WeatherForm.js ✅
```

**Step 5 - Create Homepage:**
```
Agent sees:
- Structure: Pages go in SimpleWeather/pages/
- Created files: SimpleWeather/components/WeatherForm.js exists!

Agent creates: SimpleWeather/pages/index.js
Agent writes:   import WeatherForm from '../components/WeatherForm'  ✅
                (Correctly references the previously created component)
```

**Step 6 - Add Styling:**
```
Agent sees:
- Structure: Styles go in SimpleWeather/styles/
- Created files: List of all components to style

Agent creates: SimpleWeather/styles/Weather.module.css ✅
Agent can read: WeatherForm.js to see what classes to style
```

## Testing

Run the enhanced test:
```bash
python test_context.py
```

Then try in GUI:
```
> Create a Next.js app called TestApp with a navbar component and homepage
```

You should see:
- Proper folder structure (components/, pages/)
- Files in correct locations
- Later steps referencing earlier files
- Organized, professional project layout
