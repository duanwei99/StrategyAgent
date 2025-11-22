@echo off
chcp 65001 >nul
echo ================================================
echo Freqtrade 快速安装脚本
echo ================================================
echo.

echo [提示] 此脚本将：
echo   1. 安装 Freqtrade
echo   2. 下载 BTC/USDT 和 ETH/USDT 的历史数据（2023年1月）
echo   3. 验证安装
echo.

set /p "confirm=是否继续？(y/N): "
if /i not "%confirm%"=="y" (
    echo 安装已取消。
    pause
    exit /b 0
)

echo.
echo ================================================
echo 步骤 1/3: 安装 Freqtrade
echo ================================================
echo.

python -m pip install freqtrade

if errorlevel 1 (
    echo.
    echo [错误] Freqtrade 安装失败！
    echo.
    echo 可能的原因：
    echo   - 网络连接问题
    echo   - Python 版本不兼容（需要 Python 3.9-3.11）
    echo.
    echo 解决方案：
    echo   - 尝试使用国内镜像：
    echo     pip install -i https://pypi.tuna.tsinghua.edu.cn/simple freqtrade
    echo.
    pause
    exit /b 1
)

echo.
echo [OK] Freqtrade 安装成功！
echo.

echo ================================================
echo 步骤 2/3: 下载历史数据
echo ================================================
echo.
echo [提示] 下载数据可能需要 2-5 分钟，请耐心等待...
echo.

cd freqtrade_worker

freqtrade download-data --exchange binance --pairs BTC/USDT ETH/USDT --timerange 20230101-20230131 --timeframe 5m --config user_data/config.json --userdir user_data

if errorlevel 1 (
    echo.
    echo [警告] 数据下载可能失败或不完整
    echo.
    echo 可能的原因：
    echo   - 网络连接问题
    echo   - 交易所 API 限制
    echo.
    echo 建议：
    echo   - 稍后重试
    echo   - 或使用更短的时间范围
    echo.
    cd ..
    pause
    exit /b 1
)

cd ..

echo.
echo [OK] 数据下载完成！
echo.

echo ================================================
echo 步骤 3/3: 验证安装
echo ================================================
echo.

freqtrade --version

if errorlevel 1 (
    echo [警告] 版本检查失败
) else (
    echo [OK] Freqtrade 工作正常！
)

echo.
echo ================================================
echo 安装完成！
echo ================================================
echo.
echo 下载的数据位置：
echo   freqtrade_worker\user_data\data\binance\
echo.
echo 下一步：
echo   1. 运行应用：.\run_agent.bat
echo   2. 访问前端：http://localhost:8501
echo   3. 开始生成策略！
echo.
pause

