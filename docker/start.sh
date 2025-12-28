#!/bin/bash

# StrategyAgent Docker 启动脚本

set -e

echo "🚀 Starting StrategyAgent with Docker..."

# 检查 Docker 是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# 检查 Docker Compose 是否安装
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# 检查 .env 文件
if [ ! -f "../.env" ]; then
    echo "⚠️  .env file not found. Creating from env.example..."
    if [ -f "../env.example" ]; then
        cp ../env.example ../.env
        echo "✅ Created .env file. Please edit it with your API keys."
    else
        echo "❌ env.example not found. Please create .env file manually."
        exit 1
    fi
fi

# 获取项目根目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_ROOT"

# 使用 docker-compose 或 docker compose
if command -v docker-compose &> /dev/null; then
    COMPOSE_CMD="docker-compose"
else
    COMPOSE_CMD="docker compose"
fi

# 构建并启动
echo "📦 Building and starting containers..."
$COMPOSE_CMD -f docker/docker-compose.yml up -d --build

# 等待服务启动
echo "⏳ Waiting for services to start..."
sleep 5

# 检查服务状态
echo "📊 Checking service status..."
$COMPOSE_CMD -f docker/docker-compose.yml ps

echo ""
echo "✅ StrategyAgent is running!"
echo ""
echo "📍 Access points:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "📝 Useful commands:"
echo "   View logs: $COMPOSE_CMD -f docker/docker-compose.yml logs -f"
echo "   Stop: $COMPOSE_CMD -f docker/docker-compose.yml down"
echo "   Restart: $COMPOSE_CMD -f docker/docker-compose.yml restart"
echo ""

