@echo off
chcp 65001 >nul
echo ================================================
echo 豆包模型配置助手
echo ================================================
echo.

REM 检查 env.example 是否存在
if not exist "env.example" (
    echo [错误] env.example 文件不存在！
    echo 请确保在项目根目录下运行此脚本。
    pause
    exit /b 1
)

REM 检查 .env 是否已存在
if exist ".env" (
    echo [警告] .env 文件已存在！
    echo.
    set /p "overwrite=是否覆盖现有配置？(y/N): "
    if /i not "%overwrite%"=="y" (
        echo 配置已取消。
        pause
        exit /b 0
    )
    echo.
)

echo [步骤 1/3] 复制配置模板...
copy /Y env.example .env >nul
if errorlevel 1 (
    echo [错误] 复制文件失败！
    pause
    exit /b 1
)
echo ✓ 配置文件创建成功

REM 转换文件编码为 UTF-8
echo 正在修复文件编码...
python fix_env_encoding.py >nul 2>&1
echo.

echo [步骤 2/3] 请输入豆包 API Key
echo.
echo 如何获取 API Key：
echo 1. 访问 https://console.volcengine.com/ark
echo 2. 注册/登录账号
echo 3. 进入"火山方舟"服务
echo 4. 创建并复制 API Key
echo.
set /p "api_key=请输入你的豆包 API Key: "

if "%api_key%"=="" (
    echo [警告] 未输入 API Key，使用默认配置
    echo 请稍后手动编辑 .env 文件配置 DOUBAO_API_KEY
) else (
    echo [步骤 3/3] 更新配置文件...
    
    REM 使用 PowerShell 替换 API Key
    powershell -Command "(Get-Content .env) -replace 'DOUBAO_API_KEY=your_doubao_api_key_here', 'DOUBAO_API_KEY=%api_key%' | Set-Content .env"
    
    if errorlevel 1 (
        echo [警告] 自动配置失败，请手动编辑 .env 文件
    ) else (
        echo ✓ API Key 配置成功
    )
)

echo.
echo ================================================
echo 配置完成！
echo ================================================
echo.
echo 当前配置：
echo   - LLM 提供商: 豆包（火山引擎）
echo   - 代码生成模型: doubao-seed-code
echo   - 工具调用模型: kimi-k2
echo   - 策略优化模型: doubao-seed-1.6-thinking
echo.
echo 下一步：
echo   1. 如需修改配置，请编辑 .env 文件
echo   2. 运行测试脚本验证配置: python test_llm_config.py
echo   3. 启动应用: run_agent.bat
echo.
echo 详细文档请查看：
echo   - LLM_CONFIG_GUIDE.md (配置指南)
echo   - MODEL_UPGRADE_SUMMARY.md (升级说明)
echo.
pause

