@echo off
chcp 65001 >nul
echo ================================================
echo 测试 OKX API 连接
echo ================================================
echo.

REM 激活 conda 环境
call conda activate quant

REM 进入工作目录
cd freqtrade_worker

echo 测试连接到 OKX...
echo.

REM 测试获取市场信息（不需要下载数据，只是测试连接）
freqtrade list-markets --exchange okx --config user_data/config.json --userdir user_data --quote USDT --print-json >nul 2>&1

if errorlevel 1 (
    echo [失败] 无法连接到 OKX API
    echo.
    echo 建议：
    echo   1. 检查网络连接
    echo   2. 尝试使用代理: download_data_with_proxy.bat
    echo   3. 检查防火墙设置
    echo.
) else (
    echo [成功] 可以正常连接到 OKX API！
    echo.
    echo 现在可以运行 download_data.bat 下载数据
    echo.
)

cd ..
pause

