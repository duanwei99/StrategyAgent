"""
测试 OpenAI Base URL 连通性
用于验证配置的 base_url（如 https://runapi.co）是否可以正常连接 OpenAI API
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# 添加项目根目录到 Python 路径
root_dir = Path(__file__).parent.parent.absolute()
sys.path.insert(0, str(root_dir))

# 加载环境变量（支持不同编码）
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


def test_base_url_with_langchain():
    """使用 LangChain 测试 base_url 连通性"""
    print("=" * 70)
    print("测试方法 1: 使用 LangChain ChatOpenAI")
    print("=" * 70)
    
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    api_key = os.getenv("OPENAI_API_KEY", "")
    model = os.getenv("OPENAI_CODE_MODEL", "gpt-4-turbo")
    
    print(f"Base URL: {base_url}")
    print(f"Model: {model}")
    print(f"API Key: {'已配置' if api_key and api_key != 'your_openai_api_key_here' else '未配置或使用默认值'}")
    print()
    
    if not api_key or api_key == "your_openai_api_key_here":
        print("❌ 错误: OPENAI_API_KEY 未配置或使用默认值")
        print("   请在 .env 文件中设置有效的 OPENAI_API_KEY")
        return False
    
    try:
        from langchain_openai import ChatOpenAI
        from langchain_core.messages import HumanMessage
        
        print("正在初始化 ChatOpenAI...")
        llm = ChatOpenAI(
            model=model,
            api_key=api_key,
            base_url=base_url,
            temperature=0.1,
            timeout=30
        )
        print("✓ ChatOpenAI 初始化成功")
        
        print("\n正在发送测试消息...")
        test_message = HumanMessage(content="请回答：1+1等于几？只需要回答数字。")
        response = llm.invoke([test_message])
        
        print("✓ API 调用成功！")
        print(f"   响应内容: {response.content}")
        print(f"   响应类型: {type(response).__name__}")
        
        return True
        
    except Exception as e:
        print(f"❌ 错误: API 调用失败")
        print(f"   错误类型: {type(e).__name__}")
        print(f"   错误信息: {str(e)}")
        
        # 提供详细的错误分析
        error_str = str(e).lower()
        if "connection" in error_str or "timeout" in error_str or "network" in error_str:
            print("\n   可能的原因:")
            print("   1. 网络连接问题")
            print("   2. Base URL 无法访问")
            print("   3. 代理服务器配置错误")
            print("   4. 防火墙阻止连接")
        elif "authentication" in error_str or "unauthorized" in error_str or "api key" in error_str:
            print("\n   可能的原因:")
            print("   1. API Key 无效或已过期")
            print("   2. API Key 格式不正确")
        elif "not found" in error_str or "404" in error_str:
            print("\n   可能的原因:")
            print("   1. Base URL 路径不正确")
            print("   2. 服务端点不存在")
        elif "rate limit" in error_str or "429" in error_str:
            print("\n   可能的原因:")
            print("   1. API 调用频率过高")
            print("   2. 账户额度不足")
        
        return False


def test_base_url_with_openai_library():
    """使用 OpenAI 官方库测试 base_url 连通性"""
    print("\n" + "=" * 70)
    print("测试方法 2: 使用 OpenAI 官方库")
    print("=" * 70)
    
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    api_key = os.getenv("OPENAI_API_KEY", "")
    model = "gpt-5.1"
    
    print(f"Base URL: {base_url}")
    print(f"Model: {model}")
    print()
    
    if not api_key or api_key == "your_openai_api_key_here":
        print("⚠️  跳过: OPENAI_API_KEY 未配置")
        return None
    
    try:
        import requests
        from openai import OpenAI
        
        # 先测试 /v1/chat/completions 端点连通性
        print("步骤 1: 测试 /v1/chat/completions 端点连通性...")
        test_url = base_url.rstrip('/')
        if not test_url.startswith('http'):
            test_url = f"https://{test_url}"
        
        # 构建 /v1/chat/completions 端点 URL
        chat_completions_url = f"{test_url}/chat/completions"
        print(f"   测试 URL: {chat_completions_url}")
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # 准备测试请求体
        payload = {
            "model": model,
            "messages": [
                {"role": "user", "content": "test"}
            ],
            "max_tokens": 10
        }
        
        try:
            chat_response = requests.post(chat_completions_url, headers=headers, json=payload, timeout=10)
            print(f"   ✓ /v1/chat/completions 响应成功")
            print(f"   状态码: {chat_response.status_code}")
            
            if chat_response.status_code == 200:
                try:
                    chat_data = chat_response.json()
                    if "choices" in chat_data and len(chat_data["choices"]) > 0:
                        content = chat_data["choices"][0].get("message", {}).get("content", "")
                        print(f"   响应内容: {content[:50]}...")
                except:
                    pass
            elif chat_response.status_code == 401:
                print("   ⚠️  API Key 认证失败")
            else:
                print(f"   ⚠️  返回状态码: {chat_response.status_code}")
                try:
                    error_data = chat_response.json()
                    if "error" in error_data:
                        print(f"   错误信息: {error_data['error'].get('message', 'N/A')}")
                except:
                    pass
        except Exception as e:
            print(f"   ⚠️  /v1/chat/completions 测试失败: {str(e)}")
        
        print("\n步骤 2: 使用 OpenAI 客户端库测试...")
        print("正在初始化 OpenAI 客户端...")
        client = OpenAI(
            api_key=api_key,
            base_url=base_url,
            timeout=30.0
        )
        print("✓ OpenAI 客户端初始化成功")
        
        print("\n正在发送测试消息...")
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": "请回答：1+1等于几？只需要回答数字。"}
            ],
            temperature=0.1,
            max_tokens=50
        )
        
        print("✓ API 调用成功！")
        print(f"   响应内容: {response.choices[0].message.content}")
        print(f"   使用模型: {response.model}")
        print(f"   完成原因: {response.choices[0].finish_reason}")
        print(f"   使用 Token: {response.usage.total_tokens if hasattr(response, 'usage') else 'N/A'}")
        
        return True
        
    except ImportError as e:
        missing_lib = "openai" if "openai" in str(e) else "requests"
        print(f"⚠️  跳过: {missing_lib} 库未安装")
        print(f"   可以运行: pip install {missing_lib}")
        return None
    except Exception as e:
        print(f"❌ 错误: API 调用失败")
        print(f"   错误类型: {type(e).__name__}")
        print(f"   错误信息: {str(e)}")
        return False


def test_http_connectivity():
    """测试 HTTP 连通性（不进行 API 调用）"""
    print("\n" + "=" * 70)
    print("测试方法 3: HTTP 连通性测试")
    print("=" * 70)
    
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    print(f"Base URL: {base_url}")
    print()
    
    try:
        import requests
        
        # 测试基础 URL 的连通性
        test_url = base_url.rstrip('/')
        if not test_url.startswith('http'):
            test_url = f"https://{test_url}"
        
        # 提取域名部分进行连通性测试
        from urllib.parse import urlparse
        parsed = urlparse(test_url)
        domain = f"{parsed.scheme}://{parsed.netloc}"
        
        print(f"正在测试域名连通性: {domain}")
        response = requests.get(domain, timeout=10, allow_redirects=True)
        print(f"✓ HTTP 连接成功")
        print(f"   状态码: {response.status_code}")
        print(f"   响应时间: {response.elapsed.total_seconds():.2f} 秒")
        
        # 测试 API 端点 - 使用 /v1beta/models
        api_endpoint = f"{test_url}/v1beta/models"
        print(f"\n正在测试 API 端点: {api_endpoint}")
        
        api_key = os.getenv("OPENAI_API_KEY", "")
        model = os.getenv("OPENAI_CODE_MODEL", "gpt-4-turbo")
        
        headers = {
            "Content-Type": "application/json"
        }
        if api_key and api_key != "your_openai_api_key_here":
            headers["Authorization"] = f"Bearer {api_key}"
        
        # 准备 POST 请求体
        payload = {
            "model": model,
            "messages": [
                {"role": "user", "content": "test"}
            ],
            "max_tokens": 10
        }
        
        api_response = requests.post(api_endpoint, headers=headers, json=payload, timeout=10)
        print(f"✓ API 端点响应成功")
        print(f"   状态码: {api_response.status_code}")
        
        if api_response.status_code == 200:
            print("   ✓ API 端点可访问")
            try:
                response_data = api_response.json()
                if "choices" in response_data and len(response_data["choices"]) > 0:
                    print(f"   响应内容: {response_data['choices'][0].get('message', {}).get('content', 'N/A')[:50]}...")
            except:
                pass
        elif api_response.status_code == 401:
            print("   ⚠️  API Key 认证失败（但端点可访问）")
        else:
            print(f"   ⚠️  返回状态码: {api_response.status_code}")
            try:
                error_data = api_response.json()
                if "error" in error_data:
                    print(f"   错误信息: {error_data['error'].get('message', 'N/A')}")
            except:
                pass
        
        return True
        
    except ImportError:
        print("⚠️  跳过: requests 库未安装")
        print("   可以运行: pip install requests")
        return None
    except requests.exceptions.Timeout:
        print("❌ 错误: 连接超时")
        print("   可能的原因:")
        print("   1. 网络连接缓慢")
        print("   2. Base URL 无法访问")
        print("   3. 防火墙阻止连接")
        return False
    except requests.exceptions.ConnectionError as e:
        print(f"❌ 错误: 连接失败")
        print(f"   错误信息: {str(e)}")
        print("   可能的原因:")
        print("   1. Base URL 无法访问")
        print("   2. DNS 解析失败")
        print("   3. 网络连接问题")
        return False
    except Exception as e:
        print(f"❌ 错误: HTTP 测试失败")
        print(f"   错误类型: {type(e).__name__}")
        print(f"   错误信息: {str(e)}")
        return False


def main():
    """主测试函数"""
    print("\n")
    print("=" * 70)
    print("OpenAI Base URL 连通性测试工具")
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
    
    # 显示当前配置
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    api_key = os.getenv("OPENAI_API_KEY", "")
    
    print("当前配置:")
    print(f"  OPENAI_BASE_URL: {base_url}")
    print(f"  OPENAI_API_KEY: {'已配置' if api_key and api_key != 'your_openai_api_key_here' else '未配置'}")
    print()
    
    # 测试结果
    results = []
    
    # 测试 1: HTTP 连通性（最快，不消耗 API 额度）
    http_result = test_http_connectivity()
    if http_result is not None:
        results.append(("HTTP 连通性", http_result))
    
    # # 测试 2: LangChain 调用
    # langchain_result = test_base_url_with_langchain()
    # results.append(("LangChain API 调用", langchain_result))
    
    # 测试 3: OpenAI 官方库调用
    openai_result = test_base_url_with_openai_library()
    if openai_result is not None:
        results.append(("OpenAI 官方库调用", openai_result))
    
    # 汇总结果
    print("\n" + "=" * 70)
    print("测试结果汇总")
    print("=" * 70)
    
    for test_name, result in results:
        status = "✓ 通过" if result else "❌ 失败"
        print(f"  {test_name}: {status}")
    
    all_passed = all(result for _, result in results if result is not None)
    
    if all_passed:
        print("\n" + "=" * 70)
        print("🎉 所有测试通过！Base URL 可以正常连接。")
        print("=" * 70)
    else:
        print("\n" + "=" * 70)
        print("⚠️  部分测试失败，请检查配置和网络连接")
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

