# llama-server Cache Management

## 🧠 How the Cache Works

### What is Getting Cached?
llama-server maintains an **in-memory cache** of conversation context to speed up similar requests.

**From your logs:**
```
slot get_availabl: id 3 | task -1 | selected slot by LCP similarity, sim_best = 0.833
```

This means:
- **LCP**: Longest Common Prefix matching
- **sim_best = 0.833**: Found 83.3% similarity to a previous request
- **Result**: Reused old conversation context instead of starting fresh

### Why This Caused Problems

**Scenario 1: First Request**
```
You: "Create a Next.js app called WeatherApp"
Server: Creates project, runs npm install, creates files
Cache: Stores the entire conversation history
```

**Scenario 2: Second Request (10 minutes later)**
```
You: "Create a Next.js app called BlogApp"
Server: Finds 83% similarity to WeatherApp request
Cache: "This looks similar! Reusing old context..."
Result: Thinks npm is already installed, skips steps ❌
```

## ✅ Our Solution: Cache Busting

We added random IDs to every request:
```python
cache_buster = f"\n\n[Request ID: {random.randint(10000, 99999)}]"
```

**Now:**
```
Request 1: "Create Next.js app [Request ID: 45821]"
Request 2: "Create Next.js app [Request ID: 93047]"
Similarity: 0% (different IDs)
Result: Both start fresh ✓
```

## 🔄 Manual Cache Clearing

### Method 1: Use the Quick Script (Recommended)
```batch
restart_fresh.bat
```

What it does:
1. Kills llama-server (clears cache)
2. Kills GUI
3. Restarts both fresh

### Method 2: Just Clear Cache (Don't Restart)
```batch
clear_cache.bat
```

Then manually run `start_local_ai.bat` when ready.

### Method 3: Manual Process
**In Windows:**
1. Press `Ctrl+Shift+Esc` to open Task Manager
2. Find `llama-server.exe`
3. Right-click → End Task
4. Restart with `start_local_ai.bat`

**In Terminal:**
1. Find the window running llama-server
2. Press `Ctrl+C`
3. Restart with `start_local_ai.bat`

## 🔍 When to Clear Cache

### ✅ You SHOULD Clear Cache When:
- Testing the same type of request multiple times
- Agent is behaving weirdly (referencing old projects)
- You see steps being skipped that shouldn't be
- Starting a new work session

### ❌ You DON'T Need to Clear When:
- Making different types of requests
- Our cache busting is working (should be automatic now)
- Just continuing to work normally

## 🎯 Best Practices

### Daily Workflow:
```batch
# Morning - Start fresh
start_local_ai.bat

# Work on projects...

# End of day - Close everything
# (Cache automatically cleared when llama-server stops)
```

### Testing Workflow:
```batch
# Test request 1
# See issue?

restart_fresh.bat

# Test request 2
# Still seeing issues?

restart_fresh.bat
```

## 🐛 Troubleshooting Cache Issues

### Symptom: "Steps are being skipped"
**Check the llama-server logs for:**
```
slot get_availabl: selected slot by LCP similarity
```

**If you see this:**
1. The cache buster might not be working
2. Run `restart_fresh.bat` to clear immediately
3. Check that `agent_client.py` has cache busting code

### Symptom: "Agent references old project names"
**Example:**
```
You: "Create a React app called ProjectB"
Agent: "I'll continue working on ProjectA..."
```

**Cause:** Cache from previous request

**Fix:**
```batch
restart_fresh.bat
```

### Symptom: "npm already installed" on fresh projects
**Cause:** Cache thinks dependencies from old project still exist

**Fix:**
```batch
restart_fresh.bat
```

## 📊 Cache Behavior Details

### What Gets Cached:
- Full conversation history
- Tool call results
- Model responses
- System prompts

### What Doesn't Get Cached:
- File system state (actual files on disk)
- Your Python variables
- GUI state

### Cache Lifetime:
- **Lives:** As long as llama-server.exe is running
- **Dies:** When llama-server stops
- **Size:** Limited by `--ctx-size 4096` (context window)

## ⚙️ Advanced: Disabling Cache in llama-server

If you want to **completely disable** caching:

**Edit your startup command:**
```batch
llama-server.exe -m model.gguf --no-cache-prompt
```

**Note:** This will make every request slower but ensures 100% fresh context.

**We don't recommend this** because:
- Our cache busting already solves the problem
- Caching does provide some speed benefits for legitimate reuse
- `--no-cache-prompt` might not be supported in all versions

## 🧪 Verify Cache is Clear

After restarting, check llama-server logs:
```
main: server is listening on http://127.0.0.1:8080 - starting the main loop
srv update_slots: all slots are idle
```

**Good signs:**
- "all slots are idle"
- No "LCP similarity" messages initially
- First request shows "slot get_availabl: id 3 | task -1 | selected slot by LRU"
  (LRU = Least Recently Used = no similarity match = fresh!)

## 📝 Quick Reference

| Task | Command |
|------|---------|
| **Restart everything fresh** | `restart_fresh.bat` |
| **Just clear cache** | `clear_cache.bat` |
| **Manual kill** | Task Manager → llama-server.exe → End Task |
| **Check if running** | Task Manager → Look for llama-server.exe |

## 💡 Pro Tip

Add this to your workflow:
1. **Morning:** Run `restart_fresh.bat`
2. **After major changes:** Run `restart_fresh.bat`
3. **When weird behavior:** Run `restart_fresh.bat`

The cache buster we added should handle most cases, but manual clearing ensures 100% fresh state when needed!
