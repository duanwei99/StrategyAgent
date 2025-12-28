"""
Freqtrade 回测工具
"""
from typing import Dict, Any


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


def run_freqtrade_backtest_auto(strategy_code: str, timerange: str = "20230101-20231231", pair_list: list = None, timeframe: str = "5m") -> Dict[str, Any]:
    """
    执行真实回测，如果失败则直接返回异常
    
    Args:
        strategy_code: 策略代码
        timerange: 时间范围
        pair_list: 交易对列表
        timeframe: 时间周期
        
    Returns:
        Dict: 回测结果，如果失败则包含 error 字段
    """
    if not check_freqtrade_available():
        error_msg = "Freqtrade 未安装或不可用，无法执行回测"
        print(f"[ERROR] {error_msg}")
        print("[INFO] 如需真实回测，请运行: setup_freqtrade.bat")
        return {
            "error": error_msg,
            "error_type": "execution_error"
        }
    
    # 执行真实回测
    from .freqtrade_mcp import run_freqtrade_backtest
    result = run_freqtrade_backtest(strategy_code, timerange, pair_list, timeframe)
    
    # 如果回测失败，直接返回错误信息
    if "error" in result:
        error_type = result.get("error_type", "execution_error")
        print(f"[ERROR] 回测失败（{error_type}）: {result.get('error')}")
        if error_type == "code_error":
            print("[INFO] 这是代码问题，错误信息将反馈给代码生成模型")
        elif error_type == "timeout":
            print("[INFO] 回测超时")
        return result
    
    return result

