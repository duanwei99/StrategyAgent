"""
Langfuse 配置检查脚本
用于验证 Langfuse 环境变量是否正确配置
"""
import os
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from dotenv import load_dotenv

def check_langfuse_config():
    """检查 Langfuse 配置是否正确"""
    
    print("=" * 60)
    print("Langfuse 配置检查")
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
    
    # 1. 检查 LANGFUSE_SECRET_KEY
    print("1️⃣ 检查 LANGFUSE_SECRET_KEY")
    secret_key = os.getenv("LANGFUSE_SECRET_KEY", "")
    if not secret_key or secret_key == "":
        print("   ❌ 未设置 LANGFUSE_SECRET_KEY")
        print("   请访问 https://cloud.langfuse.com 获取 API Key")
        all_ok = False
    else:
        masked_key = secret_key[:8] + "*" * 20 + secret_key[-4:] if len(secret_key) > 12 else "*" * len(secret_key)
        print(f"   ✅ Secret Key 已设置：{masked_key}")
    print()
    
    # 2. 检查 LANGFUSE_PUBLIC_KEY
    print("2️⃣ 检查 LANGFUSE_PUBLIC_KEY")
    public_key = os.getenv("LANGFUSE_PUBLIC_KEY", "")
    if not public_key or public_key == "":
        print("   ❌ 未设置 LANGFUSE_PUBLIC_KEY")
        print("   请访问 https://cloud.langfuse.com 获取 API Key")
        all_ok = False
    else:
        masked_key = public_key[:8] + "*" * 20 + public_key[-4:] if len(public_key) > 12 else "*" * len(public_key)
        print(f"   ✅ Public Key 已设置：{masked_key}")
    print()
    
    # 3. 检查 LANGFUSE_BASE_URL
    print("3️⃣ 检查 LANGFUSE_BASE_URL")
    base_url = os.getenv("LANGFUSE_BASE_URL", "https://cloud.langfuse.com")
    print(f"   ℹ️  Langfuse Base URL：{base_url}")
    if base_url != "https://cloud.langfuse.com":
        print("   ⚠️  使用非默认端点，确保这是正确的")
    print()
    
    # 4. 测试连接（如果配置了 keys）
    if secret_key and public_key:
        print("4️⃣ 测试 Langfuse 连接")
        try:
            from langfuse import Langfuse
            
            langfuse_client = Langfuse(
                secret_key=secret_key,
                public_key=public_key,
                host=base_url
            )
            print("   正在连接 Langfuse...")
            
            # 测试简单的操作
            try:
                # 尝试创建一个测试 trace 来验证连接
                trace = langfuse_client.trace(name="config_test")
                trace.update()
                print("   ✅ 成功连接到 Langfuse！")
                print(f"   Base URL：{base_url}")
            except Exception as e:
                print(f"   ❌ 连接测试失败：{str(e)}")
                all_ok = False
                
        except ImportError:
            print("   ⚠️  未安装 langfuse 包")
            print("   运行：pip install langfuse")
        except Exception as e:
            print(f"   ❌ 连接失败：{str(e)}")
            all_ok = False
        print()
    
    # 总结
    print("=" * 60)
    if all_ok and secret_key and public_key:
        print("✅ Langfuse 配置完成！")
        print()
        print("下一步：")
        print("1. 启动 StrategyAgent：python start_agent.py")
        print("2. 生成一个策略")
        print("3. 访问 https://cloud.langfuse.com 查看追踪记录")
    else:
        print("⚠️  配置未完成，请按照上述提示修复问题")
        print()
        print("配置步骤：")
        print("1. 访问 https://cloud.langfuse.com 注册账号")
        print("2. 进入 Settings → API Keys 创建 API Key")
        print("3. 在 .env 文件中设置：")
        print("   LANGFUSE_SECRET_KEY=你的Secret Key")
        print("   LANGFUSE_PUBLIC_KEY=你的Public Key")
        print("   LANGFUSE_BASE_URL=https://cloud.langfuse.com")
    print("=" * 60)
    
    return all_ok


if __name__ == "__main__":
    try:
        check_langfuse_config()
    except KeyboardInterrupt:
        print("\n\n检查已取消")
    except Exception as e:
        print(f"\n❌ 发生错误：{str(e)}")
        import traceback
        traceback.print_exc()






