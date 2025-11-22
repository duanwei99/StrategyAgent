@echo off
chcp 65001 >nul
echo ================================================
echo .env 文件编码修复工具
echo ================================================
echo.

python fix_env_encoding.py

echo.
pause

