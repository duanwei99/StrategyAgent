@echo off
echo Starting StrategyAgent (without proxy for localhost)...

REM 设置环境变量，跳过本地地址的代理
set NO_PROXY=localhost,127.0.0.1
set no_proxy=localhost,127.0.0.1
set HTTP_PROXY=
set HTTPS_PROXY=
set http_proxy=
set https_proxy=

REM 启动应用
python -X utf8 start_agent.py
pause

