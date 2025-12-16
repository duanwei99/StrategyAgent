"""
检查代理环境变量的来源
帮助诊断为什么会有代理设置
"""
import os
import sys
from pathlib import Path

print("=" * 70)
print("代理环境变量来源诊断")
print("=" * 70)
print()

# 1. 检查当前进程的环境变量
print("[1] 当前 Python 进程的环境变量:")
http_proxy = os.environ.get('HTTP_PROXY') or os.environ.get('http_proxy')
https_proxy = os.environ.get('HTTPS_PROXY') or os.environ.get('https_proxy')
print(f"  HTTP_PROXY: {http_proxy if http_proxy else '未设置'}")
print(f"  HTTPS_PROXY: {https_proxy if https_proxy else '未设置'}")
print(f"  http_proxy: {os.environ.get('http_proxy', '未设置')}")
print(f"  https_proxy: {os.environ.get('https_proxy', '未设置')}")
print()

# 2. 检查 .env 文件
print("[2] 检查 .env 文件:")
env_file = Path(__file__).parent.parent / ".env"
if env_file.exists():
    print(f"  ✓ 找到 .env 文件: {env_file}")
    try:
        with open(env_file, 'r', encoding='utf-8') as f:
            content = f.read()
            proxy_lines = [line.strip() for line in content.split('\n') 
                          if 'PROXY' in line.upper() and not line.strip().startswith('#')]
            if proxy_lines:
                print("  包含的代理配置:")
                for line in proxy_lines:
                    print(f"    {line}")
            else:
                print("  - .env 文件中没有代理配置")
    except Exception as e:
        print(f"  ⚠ 无法读取 .env 文件: {e}")
else:
    print(f"  - 未找到 .env 文件: {env_file}")
print()

# 3. 检查是否加载了 .env
print("[3] 检查是否已加载 .env 文件:")
try:
    from dotenv import load_dotenv
    # 尝试重新加载（不会覆盖已存在的环境变量）
    loaded = load_dotenv(env_file, override=False)
    if loaded:
        print("  ✓ dotenv 可以加载 .env 文件")
        # 检查加载后的值
        after_load_http = os.environ.get('HTTP_PROXY') or os.environ.get('http_proxy')
        if after_load_http and after_load_http != http_proxy:
            print(f"  ⚠ 加载 .env 后 HTTP_PROXY 变为: {after_load_http}")
    else:
        print("  - dotenv 无法加载 .env 文件（可能不存在）")
except ImportError:
    print("  - python-dotenv 未安装")
except Exception as e:
    print(f"  ⚠ 加载 .env 时出错: {e}")
print()

# 4. 检查 Windows 系统环境变量
if os.name == 'nt':
    print("[4] 检查 Windows 系统环境变量:")
    import winreg
    try:
        # 用户环境变量
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment")
            try:
                user_http, _ = winreg.QueryValueEx(key, "HTTP_PROXY")
                print(f"  用户环境变量 HTTP_PROXY: {user_http}")
            except FileNotFoundError:
                print("  用户环境变量 HTTP_PROXY: 未设置")
            try:
                user_https, _ = winreg.QueryValueEx(key, "HTTPS_PROXY")
                print(f"  用户环境变量 HTTPS_PROXY: {user_https}")
            except FileNotFoundError:
                print("  用户环境变量 HTTPS_PROXY: 未设置")
            winreg.CloseKey(key)
        except Exception as e:
            print(f"  ⚠ 无法读取用户环境变量: {e}")
        
        # 系统环境变量
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                                r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment")
            try:
                sys_http, _ = winreg.QueryValueEx(key, "HTTP_PROXY")
                print(f"  系统环境变量 HTTP_PROXY: {sys_http}")
            except FileNotFoundError:
                print("  系统环境变量 HTTP_PROXY: 未设置")
            try:
                sys_https, _ = winreg.QueryValueEx(key, "HTTPS_PROXY")
                print(f"  系统环境变量 HTTPS_PROXY: {sys_https}")
            except FileNotFoundError:
                print("  系统环境变量 HTTPS_PROXY: 未设置")
            winreg.CloseKey(key)
        except Exception as e:
            print(f"  ⚠ 无法读取系统环境变量: {e}")
    except Exception as e:
        print(f"  ⚠ 无法检查 Windows 注册表: {e}")
    print()

# 5. 检查 Conda 环境变量
print("[5] 检查 Conda 环境变量:")
conda_env = os.environ.get('CONDA_DEFAULT_ENV', '未激活')
print(f"  当前 Conda 环境: {conda_env}")
if conda_env != '未激活':
    # Conda 环境变量通常在激活脚本中设置
    conda_prefix = os.environ.get('CONDA_PREFIX', '')
    if conda_prefix:
        print(f"  Conda 环境路径: {conda_prefix}")
        # 检查 conda 环境的激活脚本
        activate_d = Path(conda_prefix) / "etc" / "conda" / "activate.d"
        if activate_d.exists():
            print(f"  ✓ 找到 conda activate.d 目录: {activate_d}")
            for script in activate_d.glob("*.sh"):
                print(f"    脚本: {script.name}")
                try:
                    content = script.read_text(encoding='utf-8', errors='ignore')
                    if 'PROXY' in content.upper():
                        print(f"      ⚠ 包含代理配置!")
                        for line in content.split('\n'):
                            if 'PROXY' in line.upper():
                                print(f"        {line.strip()}")
                except:
                    pass
        else:
            print(f"  - 未找到 conda activate.d 目录")
print()

# 6. 检查 IDE 配置（VS Code）
print("[6] 检查可能的 IDE 配置:")
vscode_settings = Path(__file__).parent.parent / ".vscode" / "settings.json"
if vscode_settings.exists():
    print(f"  ✓ 找到 VS Code 配置文件: {vscode_settings}")
    try:
        import json
        with open(vscode_settings, 'r', encoding='utf-8') as f:
            settings = json.load(f)
            if 'terminal.integrated.env.windows' in settings:
                env_vars = settings['terminal.integrated.env.windows']
                proxy_vars = {k: v for k, v in env_vars.items() if 'PROXY' in k.upper()}
                if proxy_vars:
                    print("  ⚠ VS Code 终端环境变量中包含代理:")
                    for k, v in proxy_vars.items():
                        print(f"    {k} = {v}")
                else:
                    print("  - VS Code 配置中没有代理设置")
    except Exception as e:
        print(f"  ⚠ 无法读取 VS Code 配置: {e}")
else:
    print(f"  - 未找到 VS Code 配置文件")
print()

# 7. 总结
print("=" * 70)
print("诊断总结")
print("=" * 70)
print()

if http_proxy:
    print(f"当前检测到的代理: {http_proxy}")
    print()
    print("可能来源（按优先级）:")
    print("  1. IDE（VS Code/PyCharm）的终端环境变量配置")
    print("  2. Conda 环境的激活脚本")
    print("  3. .env 文件（如果存在）")
    print("  4. Windows 系统环境变量")
    print("  5. 父进程继承的环境变量")
    print()
    print("建议:")
    print("  1. 检查 IDE 的设置（VS Code: settings.json 中的 terminal.integrated.env）")
    print("  2. 检查 Conda 环境的激活脚本")
    print("  3. 如果不需要代理，可以在代码中清除:")
    print("     os.environ.pop('HTTP_PROXY', None)")
    print("     os.environ.pop('http_proxy', None)")
else:
    print("未检测到代理环境变量")
    print("（这是正常的，如果不需要代理）")

print()
print("=" * 70)

