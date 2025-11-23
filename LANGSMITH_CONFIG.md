# LangSmith 配置变量速查表

## 🔑 必需配置的环境变量

在 `.env` 文件中配置以下变量：

### 1. LANGCHAIN_TRACING_V2
```bash
LANGCHAIN_TRACING_V2=true
```
- **作用**: 启用 LangSmith 追踪功能
- **取值**: `true` (启用) 或 `false` (禁用)
- **必需**: 是

### 2. LANGCHAIN_API_KEY
```bash
LANGCHAIN_API_KEY=ls-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```
- **作用**: LangSmith 认证密钥
- **获取**: 从 [https://smith.langchain.com](https://smith.langchain.com) 获取
- **格式**: 通常以 `ls-` 开头
- **必需**: 是

## 📦 可选配置的环境变量

### 3. LANGCHAIN_PROJECT
```bash
LANGCHAIN_PROJECT=StrategyAgent
```
- **作用**: 指定追踪记录所属的项目名称
- **默认**: 如不设置，使用默认项目
- **建议**: 设置为 `StrategyAgent` 或你的项目名
- **必需**: 否（但建议设置）

### 4. LANGCHAIN_ENDPOINT
```bash
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
```
- **作用**: LangSmith API 服务器地址
- **默认**: `https://api.smith.langchain.com`
- **必需**: 否（通常使用默认值）

## 📝 完整配置示例

在 `.env` 文件中添加：

```bash
# =========================
# LangSmith 配置
# =========================
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=ls-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
LANGCHAIN_PROJECT=StrategyAgent
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
```

## 🚀 快速配置步骤

1. **获取 API Key**
   - 访问 [https://smith.langchain.com](https://smith.langchain.com)
   - 注册/登录账号
   - 进入 Settings → API Keys
   - 创建并复制 API Key

2. **配置环境变量**
   ```bash
   # 复制示例文件
   cp env.example .env
   
   # 编辑 .env 文件，添加上述配置
   ```

3. **验证配置**
   ```bash
   # Windows
   .\check_langsmith.bat
   
   # 或直接运行
   python test\test_langsmith_config.py
   ```

## 🎯 配置后的效果

启用 LangSmith 后，你可以：

✅ 在 [https://smith.langchain.com](https://smith.langchain.com) 查看：
- 每次策略生成的完整过程
- LLM 调用的输入和输出
- 各个节点的执行时间
- Token 使用统计
- 错误和调试信息

## 📚 更多信息

- 详细配置指南：[files/LANGSMITH_SETUP_GUIDE.md](files/LANGSMITH_SETUP_GUIDE.md)
- LangSmith 官方文档：[https://docs.smith.langchain.com/](https://docs.smith.langchain.com/)

## ⚠️ 注意事项

1. **API Key 安全**
   - 不要将 `.env` 文件提交到 Git
   - 不要在代码中硬编码 API Key

2. **数据隐私**
   - LangSmith 会记录所有 LLM 的输入输出
   - 如处理敏感数据，考虑禁用追踪

3. **网络要求**
   - 需要能够访问 `api.smith.langchain.com`
   - 如使用代理，确保配置正确

---

**配置完成后，运行** `python start_agent.py` **即可开始使用！**

