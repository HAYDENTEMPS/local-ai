# How the Subtask Agent Works

## Overview

Your AI agent now automatically breaks down complex tasks into smaller, faster subtasks. Each subtask gets its own focused LLM call, making the entire process much faster and more reliable.

## Example Flow

### User Request:
```
Create a Next.js 14 weather app with a city input and weather display
```

### What Happens:

**Step 1: Planning (5-10 seconds)**
```
🔍 Breaking down task into steps...
📋 Plan created: 6 steps
📋   1. Create Next.js project structure
📋   2. Install required dependencies
📋   3. Create weather API route
📋   4. Create weather display component
📋   5. Create home page with input form
📋   6. Add error handling and styling
```

**Step 2-7: Execute Each Subtask (10-30 seconds each)**
```
▶ Step 1/6: Create Next.js project structure
  ✓ Created directory: weather-app
  ✓ Executed command
✓ Completed step 1/6

▶ Step 2/6: Install required dependencies
  ✓ Executed command
✓ Completed step 2/6

▶ Step 3/6: Create weather API route
  ✓ Wrote file: weather-app/pages/api/weather.js
✓ Completed step 3/6

... etc ...

🎉 All 6 steps completed!
```

**Total Time: 2-4 minutes** (instead of 10+ minutes or timeout)

## How It Works

### For Simple Tasks
- **Detection**: Tasks with < 15 words or keywords like "create a file"
- **Action**: Runs directly without planning phase
- **Example**: "Create a file called test.txt" → Direct execution (5-10 seconds)

### For Complex Tasks
1. **Planning Call** (fast)
   - Sends short prompt asking model to break down the task
   - Limited to 300 tokens
   - Timeout: 60 seconds
   - Result: List of 3-8 subtasks

2. **Execution Calls** (focused & fast)
   - Each subtask runs in its own fresh conversation
   - No accumulated context from previous steps
   - Each call is simple and focused
   - Timeout: 3 minutes per subtask
   - Result: Specific action completed

3. **Progress Updates**
   - Real-time updates after each action
   - GUI stays responsive throughout
   - User sees exactly what's happening

## Benefits

### Speed
- **Before**: One giant call → 10+ minutes → timeout
- **After**: 1 planning call + N small calls → 2-4 minutes total

### Reliability
- Small tasks rarely timeout
- Error in one subtask doesn't break the whole process
- Can retry individual failed steps

### Visibility
- See the plan before execution
- Track progress in real-time
- Understand what the agent is doing

### Efficiency
- Model processes less context per call
- Faster token generation
- Better use of the 7B model's capabilities

## Configuration

### In agent_client.py:
- `self.use_subtasks = True` - Enable/disable feature
- Planning timeout: 60 seconds
- Subtask timeout: 180 seconds (3 minutes)
- Max subtasks: 8

### Simple Task Detection:
Keywords that skip planning:
- "create a file"
- "create a folder"
- "read"
- "list"
- "write a file"

Or tasks with < 15 words

## Tips for Users

### For Best Results:
✅ **Good**: "Create a React app with authentication and a dashboard"
✅ **Good**: "Build a Python API with 3 endpoints for user management"
✅ **Good**: "Set up a Node.js project with Express and MongoDB"

### Too Simple (wastes time on planning):
❌ "Create a file called test.txt"
❌ "List files in the current directory"

Use simple commands for simple tasks - the agent will skip planning automatically.

### Too Vague:
❌ "Make me an app"
❌ "Build something cool"

Be specific about what you want - the model needs clear requirements to create a good plan.

## Troubleshooting

### "Request timed out - subtask may be too complex"
- One of the subtasks is taking > 3 minutes
- Try breaking down your request manually into smaller parts
- Or run the slow subtask separately

### Planning fails / falls back to single task
- Model couldn't create a valid plan
- Will automatically retry as a single conversation
- May take longer but will still work

### Too many/few subtasks
- Model decides based on task complexity
- Typically creates 4-6 subtasks
- Capped at 8 to prevent too much overhead
