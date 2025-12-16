@echo off
chcp 65001 >nul
echo ================================================
echo 启动 StrategyAgent (React 前端)
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
REM 注意：不使用 --reload 选项，避免与策略文件写入冲突
echo [1/2] 启动后端服务...
start /B "StrategyAgent Backend" cmd /c "uvicorn backend.app.app:app --host 127.0.0.1 --port 8000"

REM 等待后端启动
echo 等待后端启动...
timeout /t 5 /nobreak >nul

REM 启动前端（React）
echo.
echo [2/2] 启动前端服务（React）...
echo.

REM 切换到前端目录
cd frontend\ui

REM 检查 node_modules 是否存在
if not exist node_modules (
    echo 正在安装前端依赖（这可能需要几分钟）...
    call npm.cmd install --registry=https://registry.npmmirror.com --prefer-offline --no-audit
    if errorlevel 1 (
        echo 前端依赖安装失败
        pause
        exit /b 1
    )
)

REM 启动 React 前端
echo 启动 React 前端开发服务器...
call npm.cmd run dev

pause

