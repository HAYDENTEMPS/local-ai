@echo off
set MODEL_QWEN=models\qwen2.5-7b-instruct-q4_0-002.gguf

if /i "%1"=="qwen" (
    echo SUCCESS: Matched qwen
    set MODEL=%MODEL_QWEN%
) else (
    echo FAILED: Did not match qwen
    echo Param was: [%1]
)

echo Model is: %MODEL%
pause
