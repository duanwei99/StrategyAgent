@echo off
echo ================================================
echo Download Data with Proxy
echo ================================================
echo.

REM ============================================
REM Configure your proxy here
REM ============================================
set PROXY_HOST=127.0.0.1
set PROXY_PORT=10808
REM ============================================

set HTTP_PROXY=http://%PROXY_HOST%:%PROXY_PORT%
set HTTPS_PROXY=http://%PROXY_HOST%:%PROXY_PORT%

echo Current Proxy Settings:
echo   HTTP_PROXY: %HTTP_PROXY%
echo   HTTPS_PROXY: %HTTPS_PROXY%
echo.

echo Starting download...
echo.

call conda activate quant
cd freqtrade_worker

freqtrade download-data --exchange okx --pairs BTC/USDT ETH/USDT --timerange 20230101-20230131 --timeframe 5m --config user_data/config.json --userdir user_data

cd ..

if errorlevel 1 (
    echo.
    echo [FAILED] Download failed even with proxy
    echo.
    echo Suggestions:
    echo   1. Check if proxy is running
    echo   2. Try different proxy port
    echo   3. Use simulation mode
    echo.
) else (
    echo.
    echo [SUCCESS] Data downloaded successfully!
    echo.
    echo Data location: freqtrade_worker\user_data\data\okx\
    echo.
    dir /b freqtrade_worker\user_data\data\okx\*.json 2>nul
    echo.
)

pause

