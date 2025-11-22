"""
测试代理配置和本地连接的脚本
"""
import os
import requests

print("=" * 70)
print("代理配置测试")
print("=" * 70)

# 显示当前代理设置
print("\n当前环境变量：")
print(f"  HTTP_PROXY: {os.environ.get('HTTP_PROXY', '未设置')}")
print(f"  HTTPS_PROXY: {os.environ.get('HTTPS_PROXY', '未设置')}")
print(f"  http_proxy: {os.environ.get('http_proxy', '未设置')}")
print(f"  https_proxy: {os.environ.get('https_proxy', '未设置')}")
print(f"  NO_PROXY: {os.environ.get('NO_PROXY', '未设置')}")
print(f"  no_proxy: {os.environ.get('no_proxy', '未设置')}")

# 设置 NO_PROXY 绕过本地地址
os.environ["NO_PROXY"] = "localhost,127.0.0.1"
os.environ["no_proxy"] = "localhost,127.0.0.1"

print("\n" + "=" * 70)
print("测试本地连接（localhost:8000）")
print("=" * 70)

try:
    # 测试连接
    response = requests.get('http://localhost:8000', timeout=5)
    
    print(f"\n[OK] 连接成功！")
    print(f"  状态码: {response.status_code}")
    print(f"  响应: {response.json()}")
    print("\n[SUCCESS] 问题已解决！现在可以正常访问本地服务。")
    
except requests.exceptions.ProxyError as e:
    print(f"\n[ERROR] 代理错误")
    print(f"  错误详情: {str(e)[:100]}")
    print("\n解决方案：")
    print("  1. 停止当前运行的服务（在终端按 Ctrl+C）")
    print("  2. 使用新的启动脚本: .\\run_agent_no_proxy.bat")
    print("  3. 或者临时关闭系统代理")
    
except requests.exceptions.ConnectionError as e:
    print(f"\n[ERROR] 连接错误: 后端服务未运行")
    print("  请先启动后端服务: .\\run_agent.bat")
    
except Exception as e:
    print(f"\n[ERROR] 其他错误: {str(e)[:100]}")

print("\n" + "=" * 70)

