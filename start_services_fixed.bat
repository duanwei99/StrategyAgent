@echo off
chcp 65001 >nul
echo ================================================
echo 启动 StrategyAgent (修复版)
echo ================================================
echo.

REM 设置环境变量跳过本地代理
set NO_PROXY=localhost,127.0.0.1,::1
set no_proxy=localhost,127.0.0.1,::1
set HTTP_PROXY=
set HTTPS_PROXY=
set http_proxy=
set https_proxy=

echo [提示] 已配置环境变量跳过本地代理
echo.

REM 激活 conda 环境
call conda activate quant

REM 启动后端（后台运行）
echo [1/2] 启动后端服务...
start /B "StrategyAgent Backend" cmd /c "uvicorn backend.app.app:app --host 127.0.0.1 --port 8000 --reload"

REM 等待后端启动
echo 等待后端启动...
timeout /t 5 /nobreak >nul

REM 启动前端
echo.
echo [2/2] 启动前端服务...
echo.
streamlit run frontend/app.py --server.port 8501 --server.address localhost

pause

