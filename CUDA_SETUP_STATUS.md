# CUDA Setup Status - DO NOT DELETE

**Date:** November 15, 2025
**Issue:** llama-server is slow (8 tokens/sec) because GPU isn't being used for inference
**Root Cause:** NVIDIA CUDA Toolkit not installed on system

## Current Situation

✅ **Completed:**
- Downloaded llama-server CUDA build: `llama-b7066-bin-win-cuda-12.4-x64.zip`
- Copied all files from ZIP to `C:\Apps\local-ai\`
- Model layers ARE offloading to GPU (29/29 layers)
- Flash attention is enabled
- Optimized batch file settings in `start_local_ai.bat`

❌ **Problem:**
- CUDA runtime DLLs missing (cublas64_12.dll, cudart64_12.dll, etc.)
- ggml-cuda.dll exists but can't load without NVIDIA CUDA Toolkit
- KV cache and compute buffers still using CPU instead of GPU
- Generation speed: 8 tok/s (should be 40-60 tok/s)

## ✅ CUDA Toolkit Installed!

**Installation Complete** - CUDA Toolkit 12.4
- Nsight tools installed (not needed but harmless)
- Visual Studio integrations skipped (not needed - normal)

**IMPORTANT: RESTART REQUIRED!**
CUDA needs a full system restart to add DLLs to PATH.

## After CUDA Install - Next Steps

1. **Restart your computer** (CUDA needs reboot to add to PATH)

2. **Verify CUDA is installed:**
   ```bash
   where cublas64_12.dll
   ```
   Should return: `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.4\bin\cublas64_12.dll`

3. **Restart llama-server:**
   ```batch
   cd C:\Apps\local-ai\workspace
   start_local_ai.bat qwen
   ```

4. **Check startup logs for these lines:**
   ```
   llama_kv_cache:        GPU KV buffer size = ...  ← Should say GPU not CPU!
   llm_load_tensors: using CUDA for GPU acceleration
   ```

5. **Test speed** - should see:
   - Prompt processing: 30-40 tok/s
   - **Generation: 40-60 tok/s** ← This should be MUCH faster

## Hardware

- GPU: RTX 3060 12GB
- Model: Qwen 2.5 7B Q4_0 (4.12 GB)
- Current speed: 8.17 tok/s (BAD - CPU)
- Expected speed: 40-60 tok/s (GOOD - GPU)

## Optimized Settings (Already Applied)

File: `C:\Apps\local-ai\workspace\start_local_ai.bat`

```batch
set EXTRA_FLAGS_QWEN=--jinja --gpu-layers 99 --n-gpu-layers 99 --flash-attn on --ctx-size 4096 --threads 6 --split-mode none --no-mmap
```

## If Still Slow After CUDA Install

Run this diagnostic:
```bash
cd C:\Apps\local-ai
llama-server.exe --version
nvidia-smi
where cublas64_12.dll
```

Send those outputs to Claude for further troubleshooting.

## Related Changes Made

1. **Updated `system.md`:**
   - Removed restriction on npm/pip install commands
   - Added testing & iteration workflow
   - Added import path rules for Next.js

2. **Updated `agent_client.py`:**
   - Planning includes install and testing steps
   - Max turns increased from 8 to 15
   - Better error detection for iterative fixing

3. **Updated `CLAUDE.md`:**
   - Documented new testing workflow
   - Updated execution flow details

## Quick Reference

**Start Qwen (fast model):**
```batch
start_local_ai.bat qwen
```

**Start OSS (slower but smarter):**
```batch
start_local_ai.bat oss
```

**Check GPU usage:**
```bash
nvidia-smi
```

**Test speed:**
Ask the agent: "Write a Python function to check if a number is prime"
Watch the generation speed in real-time.
