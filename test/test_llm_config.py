"""
LLM 配置测试脚本
用于验证 LLM 模型配置是否正确，以及各个模型是否可以正常调用
"""
import os
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
root_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(root_dir))

# 加载环境变量（支持不同编码）
from dotenv import load_dotenv

def load_env_with_fallback():
    """尝试使用不同编码加载 .env 文件"""
    encodings = ['utf-8', 'utf-8-sig', 'gbk', 'gb2312', 'latin-1']
    
    for encoding in encodings:
        try:
            load_dotenv(encoding=encoding)
            return True
        except UnicodeDecodeError:
            continue
        except Exception:
            continue
    
    # 如果所有编码都失败，尝试不指定编码
    try:
        load_dotenv()
        return True
    except:
        return False

# 加载环境变量
if not load_env_with_fallback():
    print("警告: 无法加载 .env 文件，请检查文件编码")

from backend.llm_config import llm_config


def test_config_loading():
    """测试配置是否正确加载"""
    print("=" * 70)
    print("测试 1: 配置加载测试")
    print("=" * 70)
    
    llm_config.print_config()
    
    provider = llm_config.provider
    
    if provider == "openai":
        if not llm_config.openai_api_key or llm_config.openai_api_key == "your_openai_api_key_here":
            print("⚠️  警告: OpenAI API Key 未配置或使用默认值")
            return False
        print("✓ OpenAI 配置已加载")
        
    elif provider == "claude":
        if not llm_config.claude_api_key or llm_config.claude_api_key == "your_claude_api_key_here":
            print("⚠️  警告: Claude API Key 未配置或使用默认值")
            return False
        print("✓ Claude 配置已加载")
        
    elif provider == "doubao":
        if not llm_config.doubao_api_key or llm_config.doubao_api_key == "your_doubao_api_key_here":
            print("⚠️  警告: 豆包 API Key 未配置或使用默认值")
            return False
        print("✓ 豆包配置已加载")
    
    else:
        print(f"❌ 错误: 不支持的提供商 '{provider}'")
        return False
    
    print("\n")
    return True


def test_model_initialization():
    """测试模型是否能够正常初始化"""
    print("=" * 70)
    print("测试 2: 模型初始化测试")
    print("=" * 70)
    
    try:
        print("初始化代码生成模型...")
        code_gen_llm = llm_config.get_code_generator_llm()
        print(f"✓ 代码生成模型初始化成功: {code_gen_llm.__class__.__name__}")
        
        print("\n初始化工具调用模型...")
        tool_llm = llm_config.get_tool_caller_llm()
        print(f"✓ 工具调用模型初始化成功: {tool_llm.__class__.__name__}")
        
        print("\n初始化策略优化模型...")
        optimizer_llm = llm_config.get_optimizer_llm()
        print(f"✓ 策略优化模型初始化成功: {optimizer_llm.__class__.__name__}")
        
        print("\n")
        return True, code_gen_llm
        
    except Exception as e:
        print(f"❌ 错误: 模型初始化失败")
        print(f"   错误信息: {str(e)}")
        print("\n")
        return False, None


def test_simple_call(llm):
    """测试简单的模型调用"""
    print("=" * 70)
    print("测试 3: 模型调用测试")
    print("=" * 70)
    
    print("正在测试模型调用（这可能需要几秒钟）...")
    
    try:
        from langchain_core.messages import HumanMessage
        
        # 简单的测试提示
        test_message = HumanMessage(content="请回答：1+1等于几？只需要回答数字。")
        
        print("发送测试消息...")
        response = llm.invoke([test_message])
        
        print(f"✓ 模型调用成功！")
        print(f"   响应内容: {response.content[:100]}...")
        print("\n")
        return True
        
    except Exception as e:
        print(f"❌ 错误: 模型调用失败")
        print(f"   错误信息: {str(e)}")
        print("\n   可能的原因:")
        print("   1. API Key 无效或已过期")
        print("   2. 网络连接问题")
        print("   3. 模型名称不正确")
        print("   4. 账户额度不足")
        print("   5. Base URL 配置错误")
        print("\n")
        return False


def main():
    """主测试函数"""
    print("\n")
    print("=" * 70)
    print("StrategyAgent LLM 配置测试工具")
    print("=" * 70)
    print("\n")
    
    # 检查 .env 文件是否存在
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ 错误: .env 文件不存在")
        print("   请先复制 env.example 为 .env 并配置相关参数")
        print("\n   Windows 命令: copy env.example .env")
        print("   Linux/Mac 命令: cp env.example .env")
        return
    
    print("✓ .env 文件存在\n")
    
    # 测试 1: 配置加载
    if not test_config_loading():
        print("❌ 配置加载失败，请检查 .env 文件配置")
        return
    
    # 测试 2: 模型初始化
    success, llm = test_model_initialization()
    if not success:
        print("❌ 模型初始化失败，请检查 API Key 和配置")
        return
    
    # 测试 3: 模型调用（可选）
    print("是否要测试实际的模型调用？这将消耗少量 API 额度。")
    user_input = input("输入 'y' 继续，其他键跳过: ").strip().lower()
    
    if user_input == 'y':
        if test_simple_call(llm):
            print("=" * 70)
            print("🎉 所有测试通过！LLM 配置正确，可以正常使用。")
            print("=" * 70)
        else:
            print("=" * 70)
            print("⚠️  模型调用测试失败，但配置可能没问题，请检查网络和 API 状态")
            print("=" * 70)
    else:
        print("=" * 70)
        print("✓ 跳过模型调用测试")
        print("✓ 配置和初始化测试通过！")
        print("=" * 70)
    
    print("\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n测试被用户中断")
    except Exception as e:
        print(f"\n\n❌ 发生未预期的错误: {str(e)}")
        import traceback
        traceback.print_exc()

