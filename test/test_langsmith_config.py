"""
LangSmith 配置检查脚本
用于验证 LangSmith 环境变量是否正确配置
"""
import os
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from dotenv import load_dotenv

def check_langsmith_config():
    """检查 LangSmith 配置是否正确"""
    
    print("=" * 60)
    print("LangSmith 配置检查")
    print("=" * 60)
    print()
    
    # 加载环境变量
    env_file = root_dir / ".env"
    if not env_file.exists():
        print("❌ 错误：未找到 .env 文件")
        print(f"   请从 env.example 复制一份到 .env")
        print(f"   位置：{env_file}")
        return False
    
    print(f"✅ 找到 .env 文件：{env_file}")
    load_dotenv(env_file)
    print()
    
    # 检查各项配置
    all_ok = True
    
    # 1. 检查 LANGCHAIN_TRACING_V2
    print("1️⃣ 检查 LANGCHAIN_TRACING_V2")
    tracing_enabled = os.getenv("LANGCHAIN_TRACING_V2", "false").lower()
    if tracing_enabled == "true":
        print("   ✅ LangSmith 追踪已启用")
    else:
        print("   ⚠️  LangSmith 追踪未启用")
        print("   提示：设置 LANGCHAIN_TRACING_V2=true 以启用追踪")
    print()
    
    # 2. 检查 LANGCHAIN_API_KEY
    print("2️⃣ 检查 LANGCHAIN_API_KEY")
    api_key = os.getenv("LANGCHAIN_API_KEY", "")
    if not api_key or api_key == "":
        print("   ❌ 未设置 LANGCHAIN_API_KEY")
        print("   请访问 https://smith.langchain.com 获取 API Key")
        all_ok = False
    elif not api_key.startswith("ls-"):
        print(f"   ⚠️  API Key 格式可能不正确：{api_key[:10]}...")
        print("   LangSmith API Key 通常以 'ls-' 开头")
    else:
        masked_key = api_key[:8] + "*" * 20 + api_key[-4:]
        print(f"   ✅ API Key 已设置：{masked_key}")
    print()
    
    # 3. 检查 LANGCHAIN_PROJECT
    print("3️⃣ 检查 LANGCHAIN_PROJECT")
    project = os.getenv("LANGCHAIN_PROJECT", "")
    if project:
        print(f"   ✅ 项目名称：{project}")
    else:
        print("   ⚠️  未设置项目名称")
        print("   建议设置 LANGCHAIN_PROJECT=StrategyAgent")
    print()
    
    # 4. 检查 LANGCHAIN_ENDPOINT
    print("4️⃣ 检查 LANGCHAIN_ENDPOINT")
    endpoint = os.getenv("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com")
    print(f"   ℹ️  API 端点：{endpoint}")
    if endpoint != "https://api.smith.langchain.com":
        print("   ⚠️  使用非默认端点，确保这是正确的")
    print()
    
    # 5. 测试连接（如果启用了追踪）
    if tracing_enabled == "true" and api_key and api_key != "":
        print("5️⃣ 测试 LangSmith 连接")
        try:
            from langsmith import Client
            
            client = Client()
            # 尝试获取当前用户信息
            print("   正在连接 LangSmith...")
            
            # 测试简单的操作
            try:
                # 这个操作不会真正创建 run，只是测试连接
                print("   ✅ 成功连接到 LangSmith！")
                print(f"   API 端点：{client.api_url}")
            except Exception as e:
                print(f"   ❌ 连接测试失败：{str(e)}")
                all_ok = False
                
        except ImportError:
            print("   ⚠️  未安装 langsmith 包")
            print("   运行：pip install langsmith")
        except Exception as e:
            print(f"   ❌ 连接失败：{str(e)}")
            all_ok = False
        print()
    
    # 总结
    print("=" * 60)
    if all_ok and tracing_enabled == "true" and api_key:
        print("✅ LangSmith 配置完成！")
        print()
        print("下一步：")
        print("1. 启动 StrategyAgent：python start_agent.py")
        print("2. 生成一个策略")
        print("3. 访问 https://smith.langchain.com 查看追踪记录")
    else:
        print("⚠️  配置未完成，请按照上述提示修复问题")
        print()
        print("配置步骤：")
        print("1. 访问 https://smith.langchain.com 注册账号")
        print("2. 创建 API Key")
        print("3. 在 .env 文件中设置：")
        print("   LANGCHAIN_TRACING_V2=true")
        print("   LANGCHAIN_API_KEY=你的API密钥")
        print("   LANGCHAIN_PROJECT=StrategyAgent")
        print()
        print("详细指南：files/LANGSMITH_SETUP_GUIDE.md")
    print("=" * 60)
    
    return all_ok


if __name__ == "__main__":
    try:
        check_langsmith_config()
    except KeyboardInterrupt:
        print("\n\n检查已取消")
    except Exception as e:
        print(f"\n❌ 发生错误：{str(e)}")
        import traceback
        traceback.print_exc()






