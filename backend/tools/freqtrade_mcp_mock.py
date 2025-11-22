"""
Freqtrade 回测工具的模拟版本
用于在没有安装 Freqtrade 或没有历史数据时进行开发和测试
"""
import random
import time
from typing import Dict, Any


def run_freqtrade_backtest_mock(strategy_code: str, timerange: str = "20230101-20231231", pair_list: list = None) -> Dict[str, Any]:
    """
    模拟 Freqtrade 回测（不实际执行，返回随机的回测结果）
    
    用于：
    1. 测试系统整体流程
    2. 在没有安装 Freqtrade 时进行开发
    3. 快速验证 LLM 生成的代码语法
    
    Args:
        strategy_code: 策略的 Python 代码字符串
        timerange: 回测时间范围 (YYYYMMDD-YYYYMMDD)
        pair_list: 交易对列表 (可选)
        
    Returns:
        Dict: 包含模拟的回测结果
    """
    print(f"[MOCK MODE] 模拟回测: timerange={timerange}")
    print(f"[MOCK MODE] 策略代码长度: {len(strategy_code)} 字符")
    
    # 模拟执行时间（1-3秒）
    time.sleep(random.uniform(1, 3))
    
    # 生成随机但合理的回测结果
    total_trades = random.randint(10, 100)
    win_trades = int(total_trades * random.uniform(0.3, 0.7))
    win_rate = win_trades / total_trades if total_trades > 0 else 0
    
    # 根据胜率生成合理的盈利
    profit_pct = random.uniform(-20, 40) if win_rate < 0.5 else random.uniform(5, 60)
    
    summary = {
        "total_trades": total_trades,
        "profit_total_abs": round(profit_pct * 10, 2),  # 假设 1000 USD 本金
        "profit_total_pct": round(profit_pct, 2),
        "max_drawdown_pct": round(random.uniform(5, 25), 2),
        "sharpe": round(random.uniform(-0.5, 2.5), 2),
        "sortino": round(random.uniform(-0.5, 3.0), 2),
        "win_rate": round(win_rate * 100, 2),
        "full_result_path": "[模拟模式 - 无实际结果文件]"
    }
    
    print(f"[MOCK MODE] 模拟结果: 总交易={total_trades}, 盈利={profit_pct:.2f}%, 胜率={summary['win_rate']:.2f}%")
    
    return {
        "success": True,
        "metrics": summary,
        "raw_output": f"[MOCK MODE] 这是模拟的回测结果\n时间范围: {timerange}\n交易次数: {total_trades}\n盈利率: {profit_pct:.2f}%",
        "mock_mode": True
    }


def check_freqtrade_available() -> bool:
    """
    检查 Freqtrade 是否可用
    
    Returns:
        bool: True 如果 freqtrade 命令可用
    """
    import subprocess
    try:
        result = subprocess.run(
            ["freqtrade", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False
    except Exception:
        return False


def run_freqtrade_backtest_auto(strategy_code: str, timerange: str = "20230101-20231231", pair_list: list = None, force_mock: bool = False) -> Dict[str, Any]:
    """
    自动选择真实回测或模拟回测
    
    如果 Freqtrade 未安装或 force_mock=True，则使用模拟模式
    
    Args:
        strategy_code: 策略代码
        timerange: 时间范围
        pair_list: 交易对列表
        force_mock: 强制使用模拟模式
        
    Returns:
        Dict: 回测结果
    """
    if force_mock:
        print("[INFO] 强制使用模拟模式")
        return run_freqtrade_backtest_mock(strategy_code, timerange, pair_list)
    
    if not check_freqtrade_available():
        print("[WARNING] Freqtrade 未安装或不可用，使用模拟模式")
        print("[INFO] 如需真实回测，请运行: setup_freqtrade.bat")
        return run_freqtrade_backtest_mock(strategy_code, timerange, pair_list)
    
    # 尝试真实回测
    from .freqtrade_mcp import run_freqtrade_backtest
    result = run_freqtrade_backtest(strategy_code, timerange, pair_list)
    
    # 如果真实回测失败，回退到模拟模式
    if "error" in result:
        print(f"[WARNING] 真实回测失败: {result.get('error')}")
        print("[INFO] 回退到模拟模式")
        return run_freqtrade_backtest_mock(strategy_code, timerange, pair_list)
    
    return result

