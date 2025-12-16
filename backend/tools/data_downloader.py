"""
数据下载工具
封装 freqtrade download-data 命令，用于下载历史K线数据
"""
import subprocess
import os
import sys
from typing import List, Optional, Dict, Any

# 定义 Freqtrade 工作目录路径
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(CURRENT_DIR))
FREQTRADE_WORKER_DIR = os.path.join(PROJECT_ROOT, "freqtrade_worker")
CONFIG_PATH = os.path.join(FREQTRADE_WORKER_DIR, "user_data", "config.json")


def download_market_data(
    pairs: List[str],
    timeframe: str,
    timerange: str = "20230101-20231231",
    exchange: str = "okx"
) -> Dict[str, Any]:
    """
    下载指定交易对和时间周期的历史数据
    
    Args:
        pairs: 交易对列表，例如 ["BTC/USDT", "ETH/USDT"]
        timeframe: 时间周期，例如 "5m", "1h", "1d"
        timerange: 时间范围，格式 "YYYYMMDD-YYYYMMDD"
        exchange: 交易所名称，默认 "okx"
        
    Returns:
        Dict: 包含下载结果的字典
        {
            "success": bool,
            "message": str,
            "stdout": str,
            "stderr": str
        }
    """
    if not os.path.exists(CONFIG_PATH):
        return {
            "success": False,
            "message": f"配置文件不存在: {CONFIG_PATH}",
            "stdout": "",
            "stderr": ""
        }
    
    # 构建 freqtrade download-data 命令
    cmd = [
        "freqtrade", "download-data",
        "--exchange", exchange,
        "--timeframe", timeframe,
        "--timerange", timerange,
        "--config", CONFIG_PATH,
        "--userdir", os.path.join(FREQTRADE_WORKER_DIR, "user_data")
    ]
    
    # 添加交易对
    for pair in pairs:
        cmd.extend(["--pairs", pair])
    
    try:
        print(f"执行数据下载命令: {' '.join(cmd)}")
        print(f"交易对: {pairs}")
        print(f"时间周期: {timeframe}")
        print(f"时间范围: {timerange}")
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=FREQTRADE_WORKER_DIR,
            timeout=300,  # 5分钟超时
            creationflags=0x00000200 if os.name == 'nt' else 0  # Windows 下创建新进程组
        )
        
        if result.returncode == 0:
            return {
                "success": True,
                "message": f"数据下载成功: {', '.join(pairs)} ({timeframe})",
                "stdout": result.stdout,
                "stderr": result.stderr
            }
        else:
            return {
                "success": False,
                "message": f"数据下载失败 (返回码: {result.returncode})",
                "stdout": result.stdout,
                "stderr": result.stderr
            }
            
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "message": "数据下载超时（超过5分钟）",
            "stdout": "",
            "stderr": ""
        }
    except FileNotFoundError:
        return {
            "success": False,
            "message": "freqtrade 命令未找到，请确保已安装 Freqtrade",
            "stdout": "",
            "stderr": ""
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"数据下载异常: {str(e)}",
            "stdout": "",
            "stderr": ""
        }


def check_data_exists(pairs: List[str], timeframe: str, exchange: str = "okx") -> Dict[str, bool]:
    """
    检查指定交易对和时间周期的数据是否已存在
    
    Args:
        pairs: 交易对列表
        timeframe: 时间周期
        exchange: 交易所名称
        
    Returns:
        Dict: 每个交易对的数据是否存在
        {
            "BTC/USDT": True,
            "ETH/USDT": False
        }
    """
    data_dir = os.path.join(FREQTRADE_WORKER_DIR, "user_data", "data", exchange)
    result = {}
    
    for pair in pairs:
        # 将交易对格式转换为文件名格式: BTC/USDT -> BTC_USDT
        filename = pair.replace("/", "_") + f"-{timeframe}.json"
        filepath = os.path.join(data_dir, filename)
        result[pair] = os.path.exists(filepath) and os.path.getsize(filepath) > 0
    
    return result


def download_data_if_needed(
    pairs: List[str],
    timeframe: str,
    timerange: str = "20230101-20231231",
    exchange: str = "okx",
    force_download: bool = False
) -> Dict[str, Any]:
    """
    检查数据是否存在，如果不存在则下载
    
    Args:
        pairs: 交易对列表
        timeframe: 时间周期
        timerange: 时间范围
        exchange: 交易所名称
        force_download: 是否强制重新下载
        
    Returns:
        Dict: 下载结果
    """
    if not force_download:
        # 检查数据是否已存在
        data_status = check_data_exists(pairs, timeframe, exchange)
        missing_pairs = [pair for pair, exists in data_status.items() if not exists]
        
        if not missing_pairs:
            print(f"数据已存在，跳过下载: {pairs}")
            return {
                "success": True,
                "message": f"数据已存在: {', '.join(pairs)} ({timeframe})",
                "skipped": True,
                "stdout": "",
                "stderr": ""
            }
        
        # 只下载缺失的交易对
        pairs_to_download = missing_pairs
        print(f"部分数据缺失，仅下载: {pairs_to_download}")
    else:
        pairs_to_download = pairs
        print(f"强制下载: {pairs_to_download}")
    
    return download_market_data(pairs_to_download, timeframe, timerange, exchange)

