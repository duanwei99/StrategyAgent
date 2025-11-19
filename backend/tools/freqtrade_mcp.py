import subprocess
import json
import os
import shutil
from typing import Dict, Any, Optional

# 定义 Freqtrade 工作目录路径 (相对于项目根目录)
# 假设当前脚本在 backend/tools/，项目根目录在 ../../
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(CURRENT_DIR))) # D:\StrategyAgent
FREQTRADE_WORKER_DIR = os.path.join(PROJECT_ROOT, "StrategyAgent", "freqtrade_worker")
STRATEGIES_DIR = os.path.join(FREQTRADE_WORKER_DIR, "user_data", "strategies")
BACKTEST_RESULTS_DIR = os.path.join(FREQTRADE_WORKER_DIR, "user_data", "backtest_results")

def ensure_directories():
    """确保必要的目录存在"""
    os.makedirs(STRATEGIES_DIR, exist_ok=True)
    os.makedirs(BACKTEST_RESULTS_DIR, exist_ok=True)

def run_freqtrade_backtest(strategy_code: str, timerange: str = "20230101-20231231", pair_list: list = None) -> Dict[str, Any]:
    """
    执行 Freqtrade 回测
    
    Args:
        strategy_code: 策略的 Python 代码字符串
        timerange: 回测时间范围 (YYYYMMDD-YYYYMMDD)
        pair_list: 交易对列表 (可选，目前使用 config 中的默认值)
        
    Returns:
        Dict: 包含回测结果摘要和可能的错误信息
    """
    ensure_directories()
    
    # 1. 将策略代码写入文件
    strategy_filename = "AI_Strategy.py"
    strategy_class_name = "AI_Strategy" # 假设生成的代码类名固定为 AI_Strategy
    strategy_path = os.path.join(STRATEGIES_DIR, strategy_filename)
    
    try:
        with open(strategy_path, "w", encoding="utf-8") as f:
            f.write(strategy_code)
    except Exception as e:
        return {"error": f"Failed to write strategy file: {str(e)}"}

    # 2. 构建 Freqtrade 命令
    # 注意：这里假设系统已经安装了 freqtrade 命令，或者运行在 Docker 环境中
    # 为了简化，这里假设是在同一环境下运行 'freqtrade' 命令
    # 如果是 Docker，命令需要调整
    
    config_path = os.path.join(FREQTRADE_WORKER_DIR, "user_data", "config.json")
    
    # 如果没有 config.json，创建一个最小化的 dummy config (在实际生产中应该预先存在)
    if not os.path.exists(config_path):
        # 这里只是为了防止报错，实际上用户应该提供 config
        return {"error": f"Config file not found at {config_path}"}

    cmd = [
        "freqtrade", "backtesting",
        "--strategy", strategy_class_name,
        "--config", config_path,
        "--timerange", timerange,
        "--userdir", os.path.join(FREQTRADE_WORKER_DIR, "user_data"),
        "--quiet" # 减少日志输出
    ]

    try:
        # 3. 执行命令
        print(f"Executing backtest command: {' '.join(cmd)}")
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            cwd=FREQTRADE_WORKER_DIR # 在 worker 目录下运行
        )

        if result.returncode != 0:
            return {
                "error": "Backtest execution failed",
                "stdout": result.stdout,
                "stderr": result.stderr
            }

        # 4. 解析结果
        # Freqtrade 通常会生成一个 json 结果文件，或者我们可以解析 stdout 中的表格
        # 这里为了简单，我们尝试查找最新的回测结果文件
        
        # 查找最新的 .json 结果文件
        json_files = [f for f in os.listdir(BACKTEST_RESULTS_DIR) if f.endswith(".json")]
        if not json_files:
             # 如果没有找到 JSON 文件，尝试从 stdout 解析简要信息 (这里简化处理，返回 stdout)
             return {
                 "warning": "No JSON result file found",
                 "stdout": result.stdout
             }
        
        # 按修改时间排序，取最新的
        latest_file = max([os.path.join(BACKTEST_RESULTS_DIR, f) for f in json_files], key=os.path.getmtime)
        
        with open(latest_file, "r", encoding="utf-8") as f:
            backtest_data = json.load(f)
            
        # 提取关键指标 (根据 Freqtrade 结果结构)
        # 结构可能因版本而异，这里做一些防御性编程
        strategy_stats = backtest_data.get("strategy", {}).get(strategy_class_name, {})
        
        summary = {
            "total_trades": strategy_stats.get("total_trades", 0),
            "profit_total_abs": strategy_stats.get("profit_total_abs", 0),
            "profit_total_pct": strategy_stats.get("profit_total_pct", 0),
            "max_drawdown_pct": strategy_stats.get("max_drawdown_abs", 0), # 注意：这里可能是 abs 或 pct，需确认
            "sharpe": strategy_stats.get("sharpe", 0),
            "sortino": strategy_stats.get("sortino", 0),
            "win_rate": strategy_stats.get("win_rate", 0), # 可能需要计算
            "full_result_path": latest_file
        }
        
        return {"success": True, "metrics": summary, "raw_output": result.stdout[:1000]} # 截断 raw output

    except Exception as e:
        return {"error": f"Exception during backtest execution: {str(e)}"}
