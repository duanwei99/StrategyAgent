@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ================================================
echo 使用代理下载数据
echo ================================================
echo.

echo [提示] 请先配置你的代理地址
echo.

REM ============================================
REM 在这里修改你的代理地址
REM ============================================
set "PROXY_HOST=127.0.0.1"
set "PROXY_PORT=10808"
REM ============================================

set "HTTP_PROXY=http://%PROXY_HOST%:%PROXY_PORT%"
set "HTTPS_PROXY=http://%PROXY_HOST%:%PROXY_PORT%"

echo 当前代理设置:
echo   HTTP_PROXY: %HTTP_PROXY%
echo   HTTPS_PROXY: %HTTPS_PROXY%
echo.

set /p "confirm=代理地址正确吗？(y/N): "
if /i not "%confirm%"=="y" (
    echo.
    echo 请编辑此脚本文件，修改 PROXY_HOST 和 PROXY_PORT 的值
    echo 文件位置: download_data_with_proxy.bat
    echo.
    pause
    exit /b 0
)

echo.
echo ================================================
echo 开始下载数据...
echo ================================================
echo.

REM 激活 conda 环境
call conda activate quant

REM 进入工作目录
cd freqtrade_worker

REM 下载数据（使用OKX交易所，与config.json一致）
freqtrade download-data --exchange okx --pairs BTC/USDT ETH/USDT --timerange 20230101-20230131 --timeframe 5m --config user_data/config.json --userdir user_data

REM 返回根目录
cd ..

if errorlevel 1 (
    echo.
    echo ================================================
    echo [失败] 即使使用代理也无法下载
    echo ================================================
    echo.
    echo 建议: 
    echo   1. 检查代理是否正常运行
    echo   2. 尝试使用不同的代理端口
    echo   3. 使用模拟模式（系统已自动启用）
    echo.
) else (
    echo.
    echo ================================================
    echo [成功] 数据下载完成！
    echo ================================================
    echo.
    echo 数据保存位置：
    echo   freqtrade_worker\user_data\data\okx\
    echo.
    echo 文件列表：
    dir /b freqtrade_worker\user_data\data\okx\*.json 2>nul
    echo.
)

pause
endlocal
