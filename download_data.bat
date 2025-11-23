@echo off
chcp 65001 >nul
echo ================================================
echo 下载 Freqtrade 历史数据
echo ================================================
echo.

echo [提示] 此脚本将下载以下数据：
echo   - 交易所: OKX
echo   - 交易对: BTC/USDT, ETH/USDT
echo   - 时间范围: 2023年1月 (1个月)
echo   - 时间周期: 5分钟
echo   - 预计大小: ~10 MB
echo   - 预计时间: 2-5 分钟
echo.

set /p "confirm=是否继续下载？(y/N): "
if /i not "%confirm%"=="y" (
    echo 已取消。
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

if errorlevel 1 (
    echo.
    echo ================================================
    echo [错误] 数据下载失败！
    echo ================================================
    echo.
    echo 可能的原因：
    echo   1. 无法连接到 OKX API（网络/防火墙问题）
    echo   2. API 限流
    echo   3. 交易对名称不正确
    echo.
    echo 解决方案：
    echo   1. 检查网络连接
    echo   2. 使用代理版本: download_data_with_proxy.bat
    echo   3. 稍后重试
    echo   4. 使用模拟模式（系统会自动启用）
    echo.
    cd ..
    pause
    exit /b 1
)

REM 返回根目录
cd ..

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
echo 下一步：
echo   1. 重启后端服务（如果正在运行）
echo   2. 现在可以使用真实数据进行回测了！
echo.
pause

