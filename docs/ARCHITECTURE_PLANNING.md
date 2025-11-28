# Architecture Planning & Cache Busting

## 🎯 Issues You Identified

### Issue 1: Cache Reuse (Skipping Steps)
**Problem:** llama-server was reusing cached conversation context from previous requests
- Your logs showed: "selected slot by LCP similarity"
- This caused npm steps to be skipped (thought they were already done)
- Old context was bleeding into new requests

**Solution:** Cache busting with random request IDs
```python
cache_buster = f"\n\n[Request ID: {random.randint(10000, 99999)}]"
```
Each request now has a unique ID, preventing cache reuse.

### Issue 2: No Architectural Thinking
**Problem:** Agent was breaking down tasks mechanically without understanding:
- How components connect to each other
- What data flows between components
- Dependencies and import relationships
- Overall application structure

**Solution:** Architecture planning phase before task breakdown

## 🏗️ New Architecture Planning Phase

### How It Works

**Step 0: Architecture Design** (NEW!)
```
🔍 Analyzing architecture and component relationships...

🏗️ Architecture designed:

COMPONENTS:
- WeatherForm.js: Input component for city name
- WeatherDisplay.js: Shows weather data (temp, condition)
- index.js: Homepage that combines both components
- /api/weather.js: API route to fetch weather data

CONNECTIONS:
- index.js imports WeatherForm and WeatherDisplay
- WeatherForm makes API call to /api/weather
- WeatherDisplay receives data from parent (index.js)
- API route calls external weather service

DATA FLOW:
- User enters city → WeatherForm (via input state)
- WeatherForm calls /api/weather?city=X
- API returns {temp, condition, city}
- index.js passes data to WeatherDisplay as props
- WeatherDisplay renders temperature and condition

DEPENDENCIES:
1. Create API route first (other components need it)
2. Create WeatherForm (handles user input)
3. Create WeatherDisplay (shows results)
4. Create index.js last (imports all components)
```

**Step 1: Task Breakdown**
```
📋 Plan created: 6 steps
📋 1. Create project folder and initialize
📋 2. Install Next.js dependencies
📋 3. Create API route /api/weather
📋 4. Create WeatherForm component
📋 5. Create WeatherDisplay component
📋 6. Create homepage that connects everything
```

### What Each Subtask Now Sees

**Previous (Without Architecture):**
```
CURRENT TASK: Create weather display component
```

**Now (With Architecture):**
```
OVERALL GOAL: Create Next.js weather app...

ARCHITECTURE PLAN:
[Full architecture with components, connections, data flow]

CURRENT TASK: Create WeatherDisplay component

REMINDER:
  - Check the architecture plan for how components should connect
  - WeatherDisplay receives {temp, condition, city} as props
  - Should be imported by index.js (see CONNECTIONS)
```

## 📊 What This Solves

### ✅ Component Relationships
**Before:** Agent doesn't know WeatherForm should be imported by Homepage
**After:** Architecture specifies: "index.js imports WeatherForm and WeatherDisplay"

### ✅ Data Flow Understanding
**Before:** Creates components that don't pass data correctly
**After:** Architecture specifies: "WeatherDisplay receives data as props from index.js"

### ✅ Proper Dependencies
**Before:** Creates homepage before API route (broken imports)
**After:** Architecture specifies order: API → Components → Homepage

### ✅ Import Paths
**Before:** Components don't import each other
**After:** Agent knows WeatherForm is used by index.js and adds correct import

### ✅ API Integration
**Before:** Components don't know how to call the API
**After:** Architecture specifies: "WeatherForm calls /api/weather?city=X"

## 🔧 Implementation Details

### Cache Busting (agent_client.py:802, 469)
```python
import random
cache_buster = f"\n\n[Request ID: {random.randint(10000, 99999)}]"

payload = {
    "messages": [...],
    "cache_prompt": False  # Disable caching if supported
}
```

Adds unique ID to each request to prevent llama-server from reusing cached context.

### Architecture Planning (agent_client.py:766-831)
```python
def _plan_architecture(self, user_prompt, progress_callback):
    """Design overall architecture before implementation"""

    # Ask model to design:
    # 1. COMPONENTS: What files/components needed?
    # 2. RELATIONSHIPS: What imports what?
    # 3. DATA FLOW: How data moves between components?
    # 4. DEPENDENCIES: What order to create them?
```

### Context Integration (agent_client.py:621-624)
```python
if architecture:
    context_parts.append(f"\nARCHITECTURE PLAN:")
    context_parts.append(architecture)
```

Architecture is included in EVERY subtask's context.

## 📝 Example: Weather App

### Request:
```
Create a Next.js app called WeatherApp with a form to enter city
and display live weather from a free API
```

### Architecture Plan Generated:
```
COMPONENTS:
- pages/index.js: Main homepage
- components/CityInput.js: Input field + submit button
- components/WeatherCard.js: Displays temp and condition
- pages/api/weather.js: Fetches from wttr.in API

CONNECTIONS:
- index.js imports CityInput and WeatherCard
- CityInput has onChange for city state
- CityInput onSubmit calls /api/weather
- index.js passes weather data to WeatherCard as props

DATA FLOW:
- User types city name → CityInput state
- User clicks submit → API call to /api/weather?city={city}
- API fetches from wttr.in/{city}?format=j1
- API returns {temp, condition}
- index.js receives response, updates state
- WeatherCard receives props, renders data

DEPENDENCIES:
1. API route first (required by frontend)
2. Components next (used by homepage)
3. Homepage last (imports all components)
```

### Subtask 4: Create CityInput Component

**Context Sent to Model:**
```
OVERALL GOAL: Create Next.js app called WeatherApp...

FRAMEWORK: Next.js
PROJECT FOLDER: WeatherApp

ARCHITECTURE PLAN:
[Full plan above]

RECOMMENDED STRUCTURE:
WeatherApp/
├── pages/
├── components/
└── api/

PROGRESS: Step 4 of 6

COMPLETED STEPS:
  ✓ Step 1: Created project
  ✓ Step 2: Installed Next.js
  ✓ Step 3: Created API route

CREATED FILES:
  📄 WeatherApp/pages/api/weather.js

CURRENT TASK: Create CityInput component

REMINDER:
  - Check the architecture plan for how components should connect
  - CityInput needs onChange and onSubmit
  - Will be imported by index.js (see CONNECTIONS)
  - Should call /api/weather when submitted
```

**Result:**
Agent creates properly connected component that:
- ✅ Has onChange to track city state
- ✅ Has onSubmit that calls /api/weather
- ✅ Exports correctly for import by index.js
- ✅ Follows the architecture plan

## 🧪 Testing

### Check Architecture Planning:
```bash
cd C:\Apps\local-ai\workspace
python test_architecture.py  # (create this if needed)
```

### Try in GUI:
```
> Create a React app called TaskManager with:
  - TaskList component showing all tasks
  - AddTask form component
  - Each task has delete button
  - Homepage that combines them
```

You should see:
```
🔍 Analyzing architecture and component relationships...

🏗️ Architecture designed:
COMPONENTS:
- TaskList.js: Displays array of tasks
- TaskItem.js: Single task with delete button
- AddTask.js: Form with input + submit
- App.js: Main component combining all

CONNECTIONS:
- App.js imports TaskList and AddTask
- TaskList maps over tasks and renders TaskItem
- AddTask onSubmit adds task to App state
- TaskItem onClick deletes task from App state

DATA FLOW:
- App.js manages tasks array in state
- tasks passed to TaskList as prop
- TaskList passes individual task to TaskItem
- AddTask passes new task up via callback
- TaskItem passes task.id up to delete callback
...
```

## 🎉 Benefits

### Before:
- ❌ Components created in isolation
- ❌ No proper imports between files
- ❌ Data flow not considered
- ❌ API calls not connected
- ❌ Cache causing skipped steps

### After:
- ✅ Architecture designed upfront
- ✅ Components understand their relationships
- ✅ Proper imports and data flow
- ✅ API integration works correctly
- ✅ Each request is independent (no cache reuse)

Your agent now **thinks like an architect** before **acting like a builder**! 🏗️
