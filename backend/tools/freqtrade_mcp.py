import subprocess
import json
import os
import shutil
import sys
from typing import Dict, Any, Optional

# 定义 Freqtrade 工作目录路径 (相对于项目根目录)
# 假设当前脚本在 backend/tools/，项目根目录在 ../../
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# backend/tools/ -> backend/ -> project_root/
PROJECT_ROOT = os.path.dirname(os.path.dirname(CURRENT_DIR))
FREQTRADE_WORKER_DIR = os.path.join(PROJECT_ROOT, "freqtrade_worker")
STRATEGIES_DIR = os.path.join(FREQTRADE_WORKER_DIR, "user_data", "strategies")
BACKTEST_RESULTS_DIR = os.path.join(FREQTRADE_WORKER_DIR, "user_data", "backtest_results")

def ensure_directories():
    """确保必要的目录存在"""
    os.makedirs(STRATEGIES_DIR, exist_ok=True)
    os.makedirs(BACKTEST_RESULTS_DIR, exist_ok=True)

def parse_backtest_stdout(stdout: str, strategy_name: str) -> Dict[str, Any]:
    """
    从 Freqtrade 回测的 stdout 输出中解析关键指标
    
    Args:
        stdout: 回测命令的标准输出
        strategy_name: 策略名称
        
    Returns:
        Dict: 包含解析出的指标
    """
    import re
    
    metrics = {
        "total_trades": 0,
        "profit_total_abs": 0.0,
        "profit_total_pct": 0.0,
        "max_drawdown_pct": 0.0,
        "sharpe": 0.0,
        "sortino": 0.0,
        "win_rate": 0.0
    }
    
    # 解析 BACKTESTING REPORT 表格
    # 示例行: |    TOTAL |    204 |     -0.25 | -153.672 |    -15.37 |  0:40:00 |        26 |
    # 或者: | BTC/USDT |     98 |     -0.24 |  -71.127 |     -7.11 |  0:44:00 |        14 |
    lines = stdout.split('\n')
    
    # 用于收集所有交易对的数据（以防TOTAL行缺失）
    pair_trades = []
    pair_profits_abs = []
    pair_profits_pct = []
    pair_wins = []
    total_wins = 0
    
    for i, line in enumerate(lines):
        # 查找 TOTAL 行（优先）
        if '|' in line and 'TOTAL' in line.upper():
            parts = [p.strip() for p in line.split('|') if p.strip()]
            if len(parts) >= 4:
                try:
                    # parts[0] = 'TOTAL'
                    # parts[1] = trades count
                    # parts[2] = avg profit %
                    # parts[3] = total profit (abs)
                    # parts[4] = total profit %
                    
                    if len(parts) > 1:
                        metrics["total_trades"] = int(parts[1])
                    if len(parts) > 3:
                        metrics["profit_total_abs"] = float(parts[3])
                    if len(parts) > 4:
                        metrics["profit_total_pct"] = float(parts[4])
                    
                    # 如果找到TOTAL行，尝试从后续行获取胜率
                    for j in range(i+1, min(i+5, len(lines))):
                        next_line = lines[j]
                        # 查找胜率百分比（通常在TOTAL行后的几行）
                        if '%' in next_line and any(char.isdigit() for char in next_line):
                            match = re.search(r'(\d+\.?\d*)\s*%', next_line)
                            if match:
                                metrics["win_rate"] = float(match.group(1))
                                break
                except (ValueError, IndexError) as e:
                    print(f"Warning: Failed to parse TOTAL line: {e}")
        
        # 解析单个交易对行（备选方案）
        elif '|' in line and '/USDT' in line:
            parts = [p.strip() for p in line.split('|') if p.strip()]
            if len(parts) >= 5:
                try:
                    # parts[0] = pair name (e.g., BTC/USDT)
                    # parts[1] = trades
                    # parts[2] = avg profit %
                    # parts[3] = total profit abs
                    # parts[4] = total profit %
                    
                    trades = int(parts[1])
                    profit_abs = float(parts[3])
                    profit_pct = float(parts[4])
                    
                    pair_trades.append(trades)
                    pair_profits_abs.append(profit_abs)
                    pair_profits_pct.append(profit_pct)
                    
                    # 尝试从后续行获取该交易对的胜场数
                    if i+2 < len(lines):
                        # 胜率行通常在两行后
                        win_line = lines[i+2]
                        if '%' in win_line:
                            match = re.search(r'(\d+\.?\d*)\s*%', win_line)
                            if match:
                                pair_wins.append(float(match.group(1)))
                    
                    # 尝试提取胜场数（在同一行或下一行）
                    if len(parts) > 6:
                        try:
                            wins = int(parts[6])
                            total_wins += wins
                        except:
                            pass
                    
                except (ValueError, IndexError) as e:
                    print(f"Warning: Failed to parse pair line: {e}")
        
        # 查找其他指标 (Max Drawdown, Sharpe, Sortino 等)
        # 示例: | Max Drawdown              |  154.45 USDT  |  15.45 %  | ... |
        if 'Max Drawdown' in line or 'Max drawdown' in line or 'MAX DRAWDOWN' in line:
            try:
                # 提取百分比
                match = re.search(r'(\d+\.?\d*)\s*%', line)
                if match:
                    metrics["max_drawdown_pct"] = float(match.group(1))
            except Exception as e:
                print(f"Warning: Failed to parse max drawdown: {e}")
                
        if 'Sharpe' in line:
            try:
                match = re.search(r'Sharpe[^\d]*?([-\d]+\.?\d*)', line)
                if match:
                    metrics["sharpe"] = float(match.group(1))
            except Exception as e:
                print(f"Warning: Failed to parse Sharpe: {e}")
                
        if 'Sortino' in line:
            try:
                match = re.search(r'Sortino[^\d]*?([-\d]+\.?\d*)', line)
                if match:
                    metrics["sortino"] = float(match.group(1))
            except Exception as e:
                print(f"Warning: Failed to parse Sortino: {e}")
    
    # 如果没有找到TOTAL行，从单个交易对数据汇总
    if metrics["total_trades"] == 0 and pair_trades:
        metrics["total_trades"] = sum(pair_trades)
        metrics["profit_total_abs"] = sum(pair_profits_abs)
        # 总盈利百分比需要根据总本金计算，这里简化为加总（不完全准确）
        metrics["profit_total_pct"] = sum(pair_profits_pct)
        
        # 计算平均胜率
        if pair_wins:
            metrics["win_rate"] = sum(pair_wins) / len(pair_wins)
    
    return metrics

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
        "--userdir", os.path.join(FREQTRADE_WORKER_DIR, "user_data")
        # 注意：移除了 --quiet 参数，因为某些版本的 freqtrade 不支持此参数
    ]

    try:
        # 3. 执行命令
        print(f"Executing backtest command: {' '.join(cmd)}")
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            cwd=FREQTRADE_WORKER_DIR, # 在 worker 目录下运行
            timeout=120,  # 设置超时时间为2分钟
            creationflags=0x00000200 if os.name == 'nt' else 0  # Windows 下创建新进程组 (CREATE_NEW_PROCESS_GROUP)
        )

        if result.returncode != 0:
            error_msg = f"Backtest execution failed with return code {result.returncode}"
            print(f"ERROR: {error_msg}")
            print(f"STDOUT: {result.stdout}")
            print(f"STDERR: {result.stderr}")
            return {
                "error": error_msg,
                "stdout": result.stdout,
                "stderr": result.stderr
            }

        # 4. 解析结果
        # 新版 Freqtrade 将结果保存在 .meta.json 和 .zip 文件中
        # 我们直接从 stdout 解析表格数据，这样更可靠
        
        metrics = parse_backtest_stdout(result.stdout, strategy_class_name)
        
        # 查找结果文件路径（用于记录）
        meta_files = [f for f in os.listdir(BACKTEST_RESULTS_DIR) if f.endswith(".meta.json")]
        result_path = ""
        if meta_files:
            latest_meta = max([os.path.join(BACKTEST_RESULTS_DIR, f) for f in meta_files], key=os.path.getmtime)
            result_path = latest_meta.replace(".meta.json", ".zip")
        
        metrics["full_result_path"] = result_path
        
        return {"success": True, "metrics": metrics, "raw_output": result.stdout[:2000]}

    except Exception as e:
        return {"error": f"Exception during backtest execution: {str(e)}"}
