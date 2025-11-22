#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试脚本 - 验证 StrategyAgent 环境是否正确配置

运行此脚本以检查：
1. Python 依赖是否安装
2. 目录结构是否正确
3. 配置文件是否存在
4. Freqtrade 是否可用
5. OpenAI API 是否配置
"""

import sys
import os
from pathlib import Path
import subprocess

# 设置 UTF-8 输出（Windows 兼容性）
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

def print_status(message, status="info"):
    """打印状态消息"""
    symbols = {
        "success": "[OK]",
        "error": "[!!]",
        "warning": "[**]",
        "info": "[--]"
    }
    symbol = symbols.get(status, "[--]")
    print(f"{symbol} {message}")

def check_python_version():
    """检查 Python 版本"""
    print("\n" + "="*60)
    print("1. 检查 Python 版本")
    print("="*60)
    
    version = sys.version_info
    if version.major >= 3 and version.minor >= 10:
        print_status(f"Python {version.major}.{version.minor}.{version.micro}", "success")
        return True
    else:
        print_status(f"Python {version.major}.{version.minor}.{version.micro} (需要 3.10+)", "error")
        return False

def check_dependencies():
    """检查关键依赖"""
    print("\n" + "="*60)
    print("2. 检查 Python 依赖包")
    print("="*60)
    
    required_packages = [
        "fastapi",
        "uvicorn",
        "streamlit",
        "langchain",
        "langgraph",
        "langchain_openai",
        "freqtrade",
        "pandas",
        "numpy"
    ]
    
    all_ok = True
    for package in required_packages:
        try:
            __import__(package)
            print_status(f"{package}", "success")
        except ImportError:
            print_status(f"{package} - 未安装", "error")
            all_ok = False
    
    return all_ok

def check_directory_structure():
    """检查目录结构"""
    print("\n" + "="*60)
    print("3. 检查目录结构")
    print("="*60)
    
    root = Path(__file__).parent
    
    required_dirs = [
        "backend/app",
        "backend/agent",
        "backend/tools",
        "backend/strategies_cache",
        "frontend",
        "freqtrade_worker/user_data/strategies",
        "freqtrade_worker/user_data/data",
        "freqtrade_worker/user_data/backtest_results"
    ]
    
    all_ok = True
    for dir_path in required_dirs:
        full_path = root / dir_path
        if full_path.exists():
            print_status(f"{dir_path}/", "success")
        else:
            print_status(f"{dir_path}/ - 不存在", "error")
            all_ok = False
    
    return all_ok

def check_config_files():
    """检查配置文件"""
    print("\n" + "="*60)
    print("4. 检查配置文件")
    print("="*60)
    
    root = Path(__file__).parent
    
    required_files = [
        "freqtrade_worker/user_data/config.json",
        "backend/agent/graph.py",
        "backend/agent/nodes.py",
        "backend/agent/state.py",
        "backend/agent/prompts.py",
        "backend/tools/freqtrade_mcp.py",
        "frontend/app.py",
        "start_agent.py"
    ]
    
    all_ok = True
    for file_path in required_files:
        full_path = root / file_path
        if full_path.exists():
            print_status(f"{file_path}", "success")
        else:
            print_status(f"{file_path} - 不存在", "error")
            all_ok = False
    
    return all_ok

def check_env_file():
    """检查环境变量"""
    print("\n" + "="*60)
    print("5. 检查环境变量配置")
    print("="*60)
    
    root = Path(__file__).parent
    env_file = root / ".env"
    
    if env_file.exists():
        print_status(".env 文件存在", "success")
        
        # 检查关键变量
        with open(env_file, 'r') as f:
            content = f.read()
            
        if "OPENAI_API_KEY" in content:
            # 检查是否有实际的 key（不是示例）
            if "your_" not in content or "sk-" in content:
                print_status("OPENAI_API_KEY 已配置", "success")
                return True
            else:
                print_status("OPENAI_API_KEY 需要填写实际值", "warning")
                return False
        else:
            print_status("OPENAI_API_KEY 未在 .env 中找到", "warning")
            return False
    else:
        print_status(".env 文件不存在（请从 env.example 复制）", "warning")
        return False

def check_freqtrade():
    """检查 Freqtrade 可用性"""
    print("\n" + "="*60)
    print("6. 检查 Freqtrade")
    print("="*60)
    
    try:
        result = subprocess.run(
            ["freqtrade", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            version = result.stdout.strip()
            print_status(f"Freqtrade 已安装: {version}", "success")
            return True
        else:
            print_status("Freqtrade 命令执行失败", "error")
            return False
    except FileNotFoundError:
        print_status("Freqtrade 未安装或不在 PATH 中", "error")
        return False
    except Exception as e:
        print_status(f"检查 Freqtrade 时出错: {str(e)}", "error")
        return False

def check_freqtrade_data():
    """检查 Freqtrade 数据"""
    print("\n" + "="*60)
    print("7. 检查 Freqtrade 历史数据")
    print("="*60)
    
    root = Path(__file__).parent
    data_dir = root / "freqtrade_worker" / "user_data" / "data" / "binance"
    
    if data_dir.exists():
        data_files = list(data_dir.glob("*.json"))
        if data_files:
            print_status(f"找到 {len(data_files)} 个数据文件", "success")
            for f in data_files[:5]:  # 只显示前5个
                print_status(f"  - {f.name}", "info")
            if len(data_files) > 5:
                print_status(f"  ... 还有 {len(data_files) - 5} 个文件", "info")
            return True
        else:
            print_status("数据目录为空 - 需要下载数据", "warning")
            print_status("运行: cd freqtrade_worker && freqtrade download-data ...", "info")
            return False
    else:
        print_status("数据目录不存在 - 需要下载数据", "warning")
        return False

def print_summary(results):
    """打印总结"""
    print("\n" + "="*60)
    print("检查总结")
    print("="*60)
    
    total = len(results)
    passed = sum(results.values())
    failed = total - passed
    
    print(f"\n总计: {total} 项检查")
    print(f"通过: {passed}")
    if failed > 0:
        print(f"失败: {failed}")
    
    if all(results.values()):
        print(f"\n>>> 所有检查通过！系统已准备就绪。")
        print(f"\n运行以下命令启动系统：")
        print(f"  .\\run_agent.bat  (Windows)")
        print(f"  python start_agent.py  (所有平台)")
        return True
    else:
        print(f"\n*** 部分检查未通过，请根据上述提示修复问题。")
        print(f"\n参考文档：")
        print(f"  - SETUP_GUIDE.md - 详细安装指南")
        print(f"  - FIXES_SUMMARY.md - 常见问题解决")
        return False

def main():
    """主函数"""
    print(f"\n{'='*60}")
    print("StrategyAgent 环境检查工具")
    print(f"{'='*60}\n")
    
    results = {
        "Python 版本": check_python_version(),
        "依赖包": check_dependencies(),
        "目录结构": check_directory_structure(),
        "配置文件": check_config_files(),
        "环境变量": check_env_file(),
        "Freqtrade": check_freqtrade(),
        "历史数据": check_freqtrade_data()
    }
    
    success = print_summary(results)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()

