@echo off
REM StrategyAgent Docker 启动脚本 (Windows)

echo 🚀 Starting StrategyAgent with Docker...

REM 检查 Docker 是否安装
where docker >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Docker is not installed. Please install Docker Desktop first.
    pause
    exit /b 1
)

REM 检查 .env 文件
if not exist "..\.env" (
    echo ⚠️  .env file not found. Creating from env.example...
    if exist "..\env.example" (
        copy /Y ..\env.example ..\.env >nul
        echo ✅ Created .env file. Please edit it with your API keys.
    ) else (
        echo ❌ env.example not found. Please create .env file manually.
        pause
        exit /b 1
    )
)

REM 切换到项目根目录
cd /d "%~dp0\.."

REM 构建并启动
echo 📦 Building and starting containers...
docker-compose -f docker\docker-compose.yml up -d --build

REM 等待服务启动
echo ⏳ Waiting for services to start...
timeout /t 5 /nobreak >nul

REM 检查服务状态
echo 📊 Checking service status...
docker-compose -f docker\docker-compose.yml ps

echo.
echo ✅ StrategyAgent is running!
echo.
echo 📍 Access points:
echo    Frontend: http://localhost:3000
echo    Backend API: http://localhost:8000
echo    API Docs: http://localhost:8000/docs
echo.
echo 📝 Useful commands:
echo    View logs: docker-compose -f docker\docker-compose.yml logs -f
echo    Stop: docker-compose -f docker\docker-compose.yml down
echo    Restart: docker-compose -f docker\docker-compose.yml restart
echo.

pause

