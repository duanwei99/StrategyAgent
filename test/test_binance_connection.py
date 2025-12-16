"""
Binance API 连接测试脚本
用于诊断网络连接问题
"""
import requests
import time
import os
import dotenv

dotenv.load_dotenv()

print("=" * 70)
print("Binance API 连接测试")
print("=" * 70)
print()

# 显示代理设置
print("[信息] 当前代理设置:")
print(f"  HTTP_PROXY: {os.environ.get('HTTP_PROXY', '未设置')}")
print(f"  HTTPS_PROXY: {os.environ.get('HTTPS_PROXY', '未设置')}")
print(f"  http_proxy: {os.environ.get('http_proxy', '未设置')}")
print(f"  https_proxy: {os.environ.get('https_proxy', '未设置')}")
print()

# 测试的 API 端点列表
test_endpoints = [
    ("Spot API (现货)", "https://api.binance.com/api/v3/ping"),
    ("Spot Exchange Info", "https://api.binance.com/api/v3/exchangeInfo"),
    ("Futures API (期货)", "https://fapi.binance.com/fapi/v1/ping"),
    ("Delivery API", "https://dapi.binance.com/dapi/v1/ping"),
]

results = []

for name, url in test_endpoints:
    print(f"[测试] {name}")
    print(f"  URL: {url}")
    
    try:
        start_time = time.time()
        response = requests.get(url, timeout=10)
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            print(f"  [OK] 成功! 响应时间: {elapsed:.2f}秒")
            results.append((name, True, elapsed))
        else:
            print(f"  [FAILED] 状态码: {response.status_code}")
            results.append((name, False, elapsed))
    
    except requests.exceptions.Timeout:
        print(f"  [TIMEOUT] 连接超时 (>10秒)")
        results.append((name, False, None))
    
    except requests.exceptions.ConnectionError as e:
        print(f"  [ERROR] 连接错误: {str(e)[:100]}")
        results.append((name, False, None))
    
    except Exception as e:
        print(f"  [ERROR] 其他错误: {str(e)[:100]}")
        results.append((name, False, None))
    
    print()
    time.sleep(0.5)  # 避免请求过快

# 总结
print("=" * 70)
print("测试总结")
print("=" * 70)
print()

success_count = sum(1 for _, success, _ in results if success)
total_count = len(results)

print(f"成功: {success_count}/{total_count}")
print()

for name, success, elapsed in results:
    status = "[OK]" if success else "[FAILED]"
    time_info = f"({elapsed:.2f}秒)" if elapsed else "(超时或错误)"
    print(f"  {status} {name} {time_info}")

print()
print("=" * 70)

if success_count == 0:
    print("诊断结果: 无法连接到 Binance API")
    print()
    print("可能的原因:")
    print("  1. 网络防火墙阻止")
    print("  2. Binance 在当地被限制访问")
    print("  3. 需要使用代理")
    print("  4. DNS 解析问题")
    print()
    print("解决方案:")
    print("  1. 使用 VPN 或代理")
    print("  2. 配置系统代理")
    print("  3. 使用模拟模式（系统已自动启用）")
    print()
    print("使用模拟模式:")
    print("  系统已经自动使用模拟回测模式")
    print("  可以正常测试所有功能，只是回测结果是模拟的")

elif success_count < total_count:
    print("诊断结果: 部分 API 可用")
    print()
    print("说明:")
    print("  某些 Binance API 端点无法访问")
    print("  可能影响某些功能，但基本功能应该可用")
    print()
    print("建议:")
    print("  1. 尝试配置代理")
    print("  2. 或使用模拟模式")

else:
    print("诊断结果: 所有 API 连接正常！")
    print()
    print("可以正常下载数据和使用真实回测功能")

print("=" * 70)
print()

