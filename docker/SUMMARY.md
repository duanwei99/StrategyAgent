# Docker 配置总结

## ✅ 已创建的文件

### 核心配置文件
1. **Dockerfile.backend** - 后端服务（FastAPI）的 Docker 镜像
   - 基于 Python 3.11-slim
   - 安装所有 Python 依赖
   - 暴露 8000 端口

2. **Dockerfile.frontend** - 前端服务（React/Vite）的 Docker 镜像
   - 多阶段构建：Node.js 构建 + Nginx 运行
   - 使用国内 npm 镜像加速
   - 暴露 80 端口

3. **docker-compose.yml** - Docker Compose 编排文件
   - 定义 backend 和 frontend 两个服务
   - 配置网络、卷挂载、健康检查
   - 支持环境变量文件

4. **nginx.conf** - Nginx 配置文件
   - 前端静态文件服务
   - API 代理到后端
   - WebSocket 支持

### 辅助文件
5. **.dockerignore** - Docker 构建忽略文件
   - 排除不必要的文件，加速构建

6. **start.sh** - Linux/Mac 启动脚本
   - 自动检查依赖
   - 创建 .env 文件（如果不存在）
   - 一键启动服务

7. **start.bat** - Windows 启动脚本
   - 功能同 start.sh，适配 Windows

8. **README.md** - 详细文档
   - 完整的部署指南
   - 故障排查
   - 生产环境建议

9. **QUICKSTART.md** - 快速启动指南
   - 简化的使用说明
   - 常用命令

## 🎯 功能特性

- ✅ 一键启动所有服务
- ✅ 自动健康检查
- ✅ 数据持久化（freqtrade 数据、策略缓存）
- ✅ 开发模式支持（代码热更新）
- ✅ WebSocket 支持
- ✅ API 代理配置
- ✅ 跨平台支持（Windows/Linux/Mac）

## 📦 服务架构

```
┌─────────────┐
│   Frontend  │ (Nginx + React)
│  Port: 3000 │
└──────┬──────┘
       │
       │ /api/* → Backend
       │ /ws/*  → Backend (WebSocket)
       │
┌──────▼──────┐
│   Backend   │ (FastAPI + Python)
│  Port: 8000 │
└─────────────┘
```

## 🚀 使用方法

### 快速启动
```bash
# Windows
docker\start.bat

# Linux/Mac
./docker/start.sh

# 或手动
docker-compose -f docker/docker-compose.yml up -d
```

### 访问地址
- 前端: http://localhost:3000
- 后端: http://localhost:8000
- API文档: http://localhost:8000/docs

## 📝 注意事项

1. **环境变量**: 需要配置 `.env` 文件（参考 `env.example`）
2. **数据下载**: 首次使用需要下载历史数据（可选）
3. **端口冲突**: 如果 8000 或 3000 端口被占用，修改 `docker-compose.yml`
4. **资源要求**: 建议至少 2GB 可用内存

## 🔧 自定义配置

### 修改端口
编辑 `docker-compose.yml`:
```yaml
ports:
  - "新端口:容器端口"
```

### 生产环境
- 移除代码目录的 volume 挂载
- 配置 HTTPS
- 设置资源限制
- 配置日志收集

## 📚 相关文档

- [README.md](README.md) - 完整文档
- [QUICKSTART.md](QUICKSTART.md) - 快速开始
- 项目主 README: `../README.md`

