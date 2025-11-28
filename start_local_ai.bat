@echo off
title Local AI Launcher

REM DETECT GPU MODE
set USE_GPU=auto
if /i "%2"=="cpu" (
    set USE_GPU=no
    echo [FORCED CPU MODE]
    echo.
) else if /i "%2"=="gpu" (
    set USE_GPU=yes
    echo [FORCED GPU MODE]
    echo.
) else (
    nvidia-smi >nul 2>&1
    if %errorlevel% equ 0 (
        set USE_GPU=yes
        echo [GPU DETECTED] Will use GPU acceleration
        echo.
    ) else (
        set USE_GPU=no
        echo [NO GPU] Will use CPU mode
        echo.
    )
)

REM MODEL + TEMPLATE SELECTION
set MODEL_QWEN=models\qwen2.5-7b-instruct-q4_0-002.gguf
set TEMPLATE_QWEN=workspace\qwen_template.jinja
set MODEL_OSS=models\gpt-oss-20b-Q4_0.gguf
set TEMPLATE_OSS=workspace\oss_template.jinja

REM Set flags based on GPU mode
if /i "%USE_GPU%"=="yes" (
    set EXTRA_FLAGS_QWEN=--jinja --gpu-layers 99 --n-gpu-layers 99 --flash-attn on --ctx-size 4096 --threads 6 --split-mode none --no-mmap
    set EXTRA_FLAGS_OSS=--jinja --gpu-layers 99 --n-gpu-layers 99 --flash-attn on --ctx-size 4096 --threads 6 --no-mmap
) else (
    set EXTRA_FLAGS_QWEN=--jinja --n-gpu-layers 0 --main-gpu -1 --ctx-size 4096 --threads 6 --no-mmap
    set EXTRA_FLAGS_OSS=--jinja --n-gpu-layers 0 --main-gpu -1 --ctx-size 4096 --threads 6 --no-mmap
)

REM Choose model/template
if /i "%1"=="qwen" (
    set MODEL=%MODEL_QWEN%
    set TEMPLATE=%TEMPLATE_QWEN%
    set EXTRA_FLAGS=%EXTRA_FLAGS_QWEN%
    goto start_server
)

if /i "%1"=="oss" (
    set MODEL=%MODEL_OSS%
    set TEMPLATE=%TEMPLATE_OSS%
    set EXTRA_FLAGS=%EXTRA_FLAGS_OSS%
    goto start_server
)

echo.
echo Invalid or missing model argument.
echo Usage:
echo   start_local_ai.bat qwen         (auto-detect GPU)
echo   start_local_ai.bat qwen cpu     (force CPU mode)
echo   start_local_ai.bat qwen gpu     (force GPU mode)
echo   start_local_ai.bat oss          (auto-detect GPU)
echo   start_local_ai.bat oss cpu      (force CPU mode)
echo   start_local_ai.bat oss gpu      (force GPU mode)
echo.
pause
exit /b

:start_server
REM Switch to correct folder
cd /d "%~dp0.."

REM Validate model exists
if not exist "%MODEL%" (
    echo.
    echo ERROR: Model file not found:
    echo   %MODEL%
    echo.
    pause
    exit /b
)

REM START SERVER
echo Starting Llama Server:
echo   Model:    %MODEL%
echo   Template: %TEMPLATE%
echo   Flags:    %EXTRA_FLAGS%
echo.

start "Llama Server" cmd /k llama-server.exe -m "%MODEL%" --chat-template-file "%TEMPLATE%" %EXTRA_FLAGS% --port 8080

echo Waiting 3 seconds...
timeout /t 3 >nul

REM START GUI
cd /d "%~dp0gui"
start "Local AI GUI" cmd /k python main.py

echo Done.
