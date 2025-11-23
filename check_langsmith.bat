@echo off
chcp 65001 >nul
echo ================================================
echo LangSmith 配置检查工具
echo ================================================
echo.

python test\test_langsmith_config.py

echo.
pause

