# Docker 部署指南

本目录包含用于 Docker 容器化部署 StrategyAgent 项目的所有配置文件。

## 📁 文件说明

- `Dockerfile.backend` - 后端服务（FastAPI）的 Docker 镜像构建文件
- `Dockerfile.frontend` - 前端服务（React/Vite）的 Docker 镜像构建文件
- `docker-compose.yml` - Docker Compose 编排文件，一键启动所有服务
- `nginx.conf` - Nginx 配置文件（用于前端服务）

## 🚀 快速开始

### 前置要求

1. 安装 Docker 和 Docker Compose
   - Docker Desktop: https://www.docker.com/products/docker-desktop
   - 或使用 Linux 上的 Docker Engine + Docker Compose

2. 准备环境变量文件
   ```bash
   # 从项目根目录复制示例文件
   cp env.example .env
   
   # 编辑 .env 文件，填入你的 API 密钥等配置
   # 至少需要配置 LLM_PROVIDER 和对应的 API_KEY
   ```

### 一键启动

在项目根目录执行：

```bash
# 构建并启动所有服务
docker-compose -f docker/docker-compose.yml up -d

# 查看日志
docker-compose -f docker/docker-compose.yml logs -f

# 停止所有服务
docker-compose -f docker/docker-compose.yml down
```

### 访问服务

启动成功后，可以通过以下地址访问：

- **前端界面**: http://localhost:3000
- **后端API**: http://localhost:8000
- **API文档**: http://localhost:8000/docs

## 🔧 详细操作

### 1. 构建镜像

```bash
# 只构建后端
docker build -f docker/Dockerfile.backend -t strategy-agent-backend .

# 只构建前端
docker build -f docker/Dockerfile.frontend -t strategy-agent-frontend .

# 使用 docker-compose 构建所有服务
docker-compose -f docker/docker-compose.yml build
```

### 2. 启动服务

```bash
# 后台启动
docker-compose -f docker/docker-compose.yml up -d

# 前台启动（查看日志）
docker-compose -f docker/docker-compose.yml up
```

### 3. 查看服务状态

```bash
# 查看运行中的容器
docker-compose -f docker/docker-compose.yml ps

# 查看日志
docker-compose -f docker/docker-compose.yml logs

# 查看特定服务的日志
docker-compose -f docker/docker-compose.yml logs backend
docker-compose -f docker/docker-compose.yml logs frontend
```

### 4. 停止服务

```bash
# 停止服务（保留容器）
docker-compose -f docker/docker-compose.yml stop

# 停止并删除容器
docker-compose -f docker/docker-compose.yml down

# 停止并删除容器、网络、卷
docker-compose -f docker/docker-compose.yml down -v
```

### 5. 重启服务

```bash
# 重启所有服务
docker-compose -f docker/docker-compose.yml restart

# 重启特定服务
docker-compose -f docker/docker-compose.yml restart backend
```

### 6. 更新服务

```bash
# 重新构建并启动
docker-compose -f docker/docker-compose.yml up -d --build

# 只更新特定服务
docker-compose -f docker/docker-compose.yml up -d --build backend
```

## 📝 环境变量配置

在项目根目录创建 `.env` 文件（参考 `env.example`），至少需要配置：

```env
# LLM 提供商（openai, claude, doubao）
LLM_PROVIDER=doubao

# 根据选择的提供商配置对应的 API Key
DOUBAO_API_KEY=your_api_key_here
# 或
OPENAI_API_KEY=your_api_key_here
# 或
CLAUDE_API_KEY=your_api_key_here

# 代理配置（如果需要）
HTTP_PROXY=http://proxy:port
HTTPS_PROXY=http://proxy:port
```

## 🗂️ 数据持久化

Docker Compose 配置中已经挂载了以下目录，确保数据持久化：

- `freqtrade_worker/user_data` - Freqtrade 配置、策略、数据和回测结果
- `backend/strategies_cache` - 策略缓存

如果需要下载历史数据，可以进入容器执行：

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

## 🐛 故障排查

### 1. 端口被占用

如果 8000 或 3000 端口被占用，可以修改 `docker-compose.yml` 中的端口映射：

```yaml
ports:
  - "8001:8000"  # 将主机端口改为 8001
```

### 2. 查看容器日志

```bash
# 查看所有日志
docker-compose -f docker/docker-compose.yml logs

# 查看最近100行日志
docker-compose -f docker/docker-compose.yml logs --tail=100

# 实时查看日志
docker-compose -f docker/docker-compose.yml logs -f
```

### 3. 进入容器调试

```bash
# 进入后端容器
docker exec -it strategy-agent-backend bash

# 进入前端容器
docker exec -it strategy-agent-frontend sh
```

### 4. 检查服务健康状态

```bash
# 检查容器状态
docker-compose -f docker/docker-compose.yml ps

# 检查后端健康
curl http://localhost:8000/

# 检查前端
curl http://localhost:3000/
```

### 5. 重新构建镜像

如果代码更新后需要重新构建：

```bash
# 清理旧镜像
docker-compose -f docker/docker-compose.yml down
docker system prune -f

# 重新构建
docker-compose -f docker/docker-compose.yml build --no-cache

# 启动
docker-compose -f docker/docker-compose.yml up -d
```

## 🔒 生产环境建议

1. **使用环境变量文件**: 不要将 `.env` 文件提交到版本控制
2. **限制资源**: 在 `docker-compose.yml` 中添加资源限制
3. **使用 HTTPS**: 配置反向代理（如 Traefik 或 Nginx）处理 SSL
4. **数据备份**: 定期备份 `freqtrade_worker/user_data` 目录
5. **监控日志**: 配置日志收集和监控系统

## 📚 更多信息

- [Docker 官方文档](https://docs.docker.com/)
- [Docker Compose 文档](https://docs.docker.com/compose/)
- 项目主 README: `../README.md`

