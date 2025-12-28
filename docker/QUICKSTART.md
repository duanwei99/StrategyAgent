# 🚀 Docker 快速启动指南

## 前置要求

1. **安装 Docker Desktop** (Windows/Mac) 或 Docker Engine (Linux)
   - 下载地址: https://www.docker.com/products/docker-desktop

2. **准备环境变量文件**
   ```bash
   # 在项目根目录
   cp env.example .env
   # 编辑 .env 文件，至少配置 LLM_PROVIDER 和对应的 API_KEY
   ```

## 一键启动（推荐）

### Windows 用户
```bash
# 双击运行
docker\start.bat

# 或命令行运行
cd docker
start.bat
```

### Linux/Mac 用户
```bash
# 添加执行权限
chmod +x docker/start.sh

# 运行
./docker/start.sh
```

### 手动启动
```bash
# 在项目根目录执行
docker-compose -f docker/docker-compose.yml up -d

# 查看日志
docker-compose -f docker/docker-compose.yml logs -f
```

## 访问服务

启动成功后，访问：

- 🌐 **前端界面**: http://localhost:3000
- 🔧 **后端API**: http://localhost:8000
- 📚 **API文档**: http://localhost:8000/docs

## 常用命令

```bash
# 查看运行状态
docker-compose -f docker/docker-compose.yml ps

# 查看日志
docker-compose -f docker/docker-compose.yml logs -f

# 停止服务
docker-compose -f docker/docker-compose.yml down

# 重启服务
docker-compose -f docker/docker-compose.yml restart

# 重新构建并启动
docker-compose -f docker/docker-compose.yml up -d --build
```

## 下载历史数据（可选）

如果需要回测功能，需要先下载历史数据：

```bash
# 进入后端容器
docker exec -it strategy-agent-backend bash

# 下载数据
cd /app/freqtrade_worker
freqtrade download-data \
  --config user_data/config.json \
  --timerange 20230101-20231231 \
  --timeframe 5m \
  --pairs BTC/USDT ETH/USDT
```

## 故障排查

### 端口被占用
修改 `docker/docker-compose.yml` 中的端口映射：
```yaml
ports:
  - "8001:8000"  # 改为其他端口
```

### 查看详细日志
```bash
docker-compose -f docker/docker-compose.yml logs backend
docker-compose -f docker/docker-compose.yml logs frontend
```

### 重新构建
```bash
docker-compose -f docker/docker-compose.yml down
docker-compose -f docker/docker-compose.yml build --no-cache
docker-compose -f docker/docker-compose.yml up -d
```

## 更多信息

详细文档请查看 [docker/README.md](README.md)

