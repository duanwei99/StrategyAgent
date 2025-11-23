"""
Streamlit 启动诊断脚本
用于检测 Streamlit 是否能正常启动
"""
import subprocess
import sys
import time

print("=" * 70)
print("Streamlit 启动诊断")
print("=" * 70)
print()

# 1. 检查 Streamlit 是否安装
print("[步骤 1] 检查 Streamlit 是否安装...")
try:
    import streamlit
    print(f"✓ Streamlit 已安装，版本: {streamlit.__version__}")
except ImportError:
    print("✗ Streamlit 未安装！")
    print("请运行: pip install streamlit")
    sys.exit(1)

print()

# 2. 检查 Streamlit 命令是否可用
print("[步骤 2] 检查 Streamlit 命令...")
try:
    result = subprocess.run(
        [sys.executable, "-m", "streamlit", "--version"],
        capture_output=True,
        text=True,
        timeout=10
    )
    if result.returncode == 0:
        print(f"✓ Streamlit 命令可用")
        print(f"  输出: {result.stdout.strip()}")
    else:
        print(f"✗ Streamlit 命令执行失败")
        print(f"  错误: {result.stderr}")
        sys.exit(1)
except Exception as e:
    print(f"✗ 执行 Streamlit 命令时出错: {e}")
    sys.exit(1)

print()

# 3. 尝试启动 Streamlit（不阻塞）
print("[步骤 3] 尝试启动 Streamlit...")
print("  启动测试服务（5秒后自动停止）...")

try:
    # 启动 Streamlit 进程
    process = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "frontend/app.py",
         "--server.port", "8501",
         "--server.address", "localhost"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # 等待 5 秒
    time.sleep(5)
    
    # 检查进程状态
    if process.poll() is None:
        print("✓ Streamlit 进程正在运行")
        
        # 检查端口
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', 8501))
        sock.close()
        
        if result == 0:
            print("✓ Streamlit 服务可以访问（端口 8501）")
            print()
            print("=" * 70)
            print("✅ 诊断完成：Streamlit 工作正常！")
            print("=" * 70)
        else:
            print("⚠️  Streamlit 进程在运行，但端口 8501 无法访问")
            print("  可能的原因:")
            print("  1. 防火墙阻止")
            print("  2. 端口被占用")
            print("  3. Streamlit 启动过程中卡住")
        
        # 停止进程
        print()
        print("停止测试进程...")
        process.terminate()
        try:
            process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            process.kill()
        print("✓ 测试进程已停止")
        
    else:
        print(f"✗ Streamlit 进程已停止，退出代码: {process.returncode}")
        
        # 读取输出
        stdout, stderr = process.communicate(timeout=2)
        
        if stderr:
            print()
            print("错误输出:")
            print("-" * 70)
            print(stderr)
            print("-" * 70)
        
        if stdout:
            print()
            print("标准输出:")
            print("-" * 70)
            print(stdout)
            print("-" * 70)
        
        print()
        print("=" * 70)
        print("❌ 诊断完成：Streamlit 启动失败！")
        print("=" * 70)
        print()
        print("可能的原因:")
        print("  1. frontend/app.py 文件有语法错误")
        print("  2. 缺少依赖包")
        print("  3. 环境配置问题")
        print()
        print("建议：")
        print("  1. 手动运行查看详细错误:")
        print("     streamlit run frontend/app.py")
        print("  2. 检查 frontend/app.py 是否有语法错误")
        print("  3. 确保所有依赖已安装")

except KeyboardInterrupt:
    print("\n测试被用户中断")
    if process and process.poll() is None:
        process.terminate()
except Exception as e:
    print(f"\n✗ 测试过程中出错: {e}")
    import traceback
    traceback.print_exc()
    if process and process.poll() is None:
        process.terminate()

print()

