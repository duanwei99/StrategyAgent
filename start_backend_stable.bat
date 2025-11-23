@echo off
echo Starting Backend (Stable Mode - No Auto Reload)...
conda activate quant
uvicorn backend.app.app:app --host 127.0.0.1 --port 8000
pause

