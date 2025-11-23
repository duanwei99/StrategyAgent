@echo off
chcp 65001 >nul
echo ================================================
echo Binance API 连接测试
echo ================================================
echo.

call conda activate quant
python test_binance_connection.py

pause

