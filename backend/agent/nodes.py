import ast
import os
import json
import requests
from typing import Dict, Any, List
from pathlib import Path
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.tools import Tool
from langchain.agents import create_agent
from .state import AgentState
from .prompts import (
    STRATEGY_GENERATION_SYSTEM_PROMPT,
    STRATEGY_OPTIMIZATION_SYSTEM_PROMPT,
    generation_prompt, 
    optimization_prompt, 
    generation_with_search_prompt, 
    report_generation_prompt
)
from ..tools.freqtrade_mcp_mock import run_freqtrade_backtest_auto
from ..llm_config import llm_config

# 确保加载 .env 文件（如果存在）
try:
    from dotenv import load_dotenv
    # 获取项目根目录
    root_dir = Path(__file__).parent.parent.parent
    env_file = root_dir / ".env"
    if env_file.exists():
        # 尝试使用不同编码加载
        encodings = ['utf-8', 'utf-8-sig', 'gbk', 'gb2312', 'latin-1']
        loaded = False
        for encoding in encodings:
            try:
                load_dotenv(env_file, encoding=encoding, override=False)
                loaded = True
                break
            except (UnicodeDecodeError, Exception):
                continue
        if not loaded:
            load_dotenv(env_file, override=False)
except ImportError:
    # dotenv 未安装，跳过
    pass
except Exception:
    # 加载失败，继续执行（可能已经在其他地方加载了）
    pass

# 初始化不同用途的 LLM 模型
# 代码生成模型（用于首次生成策略代码）
code_generator_llm = llm_config.get_code_generator_llm()

# 策略优化模型（用于优化和修复策略代码）
optimizer_llm = llm_config.get_optimizer_llm()

# 工具调用模型（用于 Agent 决策，后续如果需要函数调用功能可以使用）
tool_caller_llm = llm_config.get_tool_caller_llm()

# 打印当前配置信息
print("=" * 60)
print("LLM 模型配置信息：")
llm_config.print_config()
print("=" * 60)

def clean_code(code: str) -> str:
    """清理 LLM 返回的代码，去除 markdown 标记"""
    if "```python" in code:
        code = code.split("```python")[1].split("```")[0]
    elif "```" in code:
        code = code.split("```")[1].split("```")[0]
    return code.strip()

def get_web_search_results(query: str) -> List[Dict[str, str]]:
    """执行联网搜索，返回结构化结果"""
    
    # 设置代理端口 10808
    proxies = {
        "http": "http://127.0.0.1:10808",
        "https": "http://127.0.0.1:10808"
    }
    
    print(f"执行搜索: {query}")
    
    results_list = []
    
    # 方法1：尝试使用 DuckDuckGo HTML 接口（不需要额外库）
    try:
        import urllib.parse
        encoded_query = urllib.parse.quote(query)
        ddg_url = f"https://html.duckduckgo.com/html/?q={encoded_query}"
        
        print(f"尝试 DuckDuckGo HTML 搜索...")
        response = requests.get(
            ddg_url,
            proxies=proxies,
            timeout=10,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        )
        
        if response.status_code == 200:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            results = soup.find_all('div', class_='result')
            
            if results:
                for i, result in enumerate(results[:5]):
                    title_elem = result.find('a', class_='result__a')
                    snippet_elem = result.find('a', class_='result__snippet')
                    
                    if title_elem:
                        title = title_elem.get_text(strip=True)
                        url = title_elem.get('href', '')
                        snippet = snippet_elem.get_text(strip=True) if snippet_elem else ''
                        
                        # 从 DuckDuckGo 重定向链接中提取真实 URL
                        if 'uddg=' in url:
                            try:
                                from urllib.parse import parse_qs, urlparse
                                parsed = urlparse(url)
                                real_url = parse_qs(parsed.query).get('uddg', [''])[0]
                                if real_url:
                                    url = urllib.parse.unquote(real_url)
                            except:
                                pass
                        
                        # 确保 URL 有完整的协议
                        if url.startswith('//'):
                            url = 'https:' + url
                        elif not url.startswith('http'):
                            url = 'https://' + url
                        
                        results_list.append({
                            "title": title,
                            "url": url,
                            "snippet": snippet
                        })
                
                if results_list:
                    print(f"DuckDuckGo 搜索成功，找到 {len(results_list)} 个结果")
                    return results_list
    except Exception as e:
        print(f"DuckDuckGo HTML 搜索失败: {str(e)}")
    
    # 方法2：尝试使用 Bing 搜索（通常更稳定）
    try:
        import urllib.parse
        encoded_query = urllib.parse.quote(query)
        bing_url = f"https://www.bing.com/search?q={encoded_query}&count=5"
        
        print(f"尝试 Bing 搜索...")
        response = requests.get(
            bing_url,
            proxies=proxies,
            timeout=10,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        )
        
        if response.status_code == 200:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            results = soup.find_all('li', class_='b_algo')
            
            if results:
                for result in results[:5]:
                    title_elem = result.find('h2')
                    link_elem = title_elem.find('a') if title_elem else None
                    snippet_elem = result.find('p')
                    
                    if link_elem:
                        title = link_elem.get_text(strip=True)
                        url = link_elem.get('href', '')
                        snippet = snippet_elem.get_text(strip=True) if snippet_elem else ''
                        
                        results_list.append({
                            "title": title,
                            "url": url,
                            "snippet": snippet
                        })
                
                if results_list:
                    print(f"Bing 搜索成功，找到 {len(results_list)} 个结果")
                    return results_list
    except Exception as e:
        print(f"Bing 搜索失败: {str(e)}")
    
    # 方法3：回退到 Google 搜索库
    try:
        from googlesearch import search
        print(f"尝试 Google 搜索...")
        
        os.environ["HTTP_PROXY"] = "http://127.0.0.1:10808"
        os.environ["HTTPS_PROXY"] = "http://127.0.0.1:10808"
        
        results = search(
            query, 
            num_results=5, 
            advanced=True,
            lang="en",
            sleep_interval=2
        )
        
        count = 0
        for result in results:
            if count >= 5:
                break
            
            title = getattr(result, 'title', '无标题')
            description = getattr(result, 'description', '')
            url = getattr(result, 'url', '')
            
            results_list.append({
                "title": title,
                "url": url,
                "snippet": description
            })
            count += 1
        
        if results_list:
            print(f"Google 搜索成功，找到 {count} 个结果")
            return results_list
            
    except ImportError:
        print("未安装 googlesearch-python 库")
    except Exception as e:
        print(f"Google 搜索失败: {str(e)}")
        
    return []

def perform_web_search(query: str) -> str:
    """执行联网搜索，返回格式化的字符串结果"""
    results = get_web_search_results(query)
    
    if not results:
        return "搜索失败: 所有搜索方法都无法获取结果。请检查:\n1. 代理是否正常运行 (127.0.0.1:10808)\n2. 网络连接是否正常\n3. 是否需要安装 beautifulsoup4: pip install beautifulsoup4"
        
    search_summary = []
    for item in results:
        summary_item = f"标题: {item['title']}\n"
        if item['snippet']:
            summary_item += f"摘要: {item['snippet']}\n"
        summary_item += f"链接: {item['url']}"
        search_summary.append(summary_item)
        
    return "\n\n".join(search_summary)

def fetch_url_content(url: str) -> str:
    """获取网页内容"""
    proxies = {
        "http": "http://127.0.0.1:10808",
        "https": "http://127.0.0.1:10808"
    }
    
    try:
        print(f"Fetching content from: {url}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, proxies=proxies, timeout=10)
        
        if response.status_code == 200:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 移除 script 和 style 标签
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.extract()
                
            text = soup.get_text()
            
            # 清理空白字符
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            return text[:10000] # 限制长度
            
    except Exception as e:
        print(f"Error fetching {url}: {e}")
    
    return ""

def summarize_web_content(content: str, query: str) -> str:
    """使用 LLM 总结网页内容"""
    if not content:
        return ""
        
    prompt = f"""
    你是一个专业的量化交易策略专家。请阅读以下网页内容，并提取与用户需求 "{query}" 相关的具体策略逻辑、技术指标、参数设置或代码片段。
    忽略无关的导航、广告或通用介绍。重点关注如何实现该策略的具体细节。
    
    网页内容:
    {content[:8000]}
    
    请总结有用的信息（如果内容不相关，请返回空字符串）:
    """
    
    try:
        response = code_generator_llm.invoke(prompt)
        return response.content
    except Exception as e:
        print(f"Summarization failed: {e}")
        return ""

# 定义搜索工具
search_tool = Tool(
    name="web_search",
    func=perform_web_search,
    description="Useful for searching trading strategy ideas, technical indicators, and best practices online. Input should be a search query."
)

def web_search_node(state: AgentState) -> Dict[str, Any]:
    """
    联网搜索节点 (首次生成前的预搜索)
    包含深度阅读和内容总结功能
    """
    print("--- Node: Web Search ---")
    user_requirement = state["user_requirement"]
    iteration_count = state["iteration_count"]
    has_strategy = state.get("has_strategy", False)
    
    if has_strategy or iteration_count > 0:
        print("跳过搜索")
        return {}
    
    search_query = f"freqtrade trading strategy {user_requirement} best practices technical indicators"
    
    # 1. 获取搜索结果
    search_results_list = get_web_search_results(search_query)
    
    if not search_results_list:
        return {"search_results": "未找到相关搜索结果"}
    
    final_summary_parts = []
    
    # 2. 遍历结果，提取前 3 个进行深入阅读
    # 过滤掉 PDF 和非 HTML 内容（虽然 get_web_search_results 已经尽力过滤，但 url 检查更保险）
    valid_results = [r for r in search_results_list if not r['url'].endswith('.pdf')][:3]
    
    for i, item in enumerate(valid_results):
        url = item['url']
        title = item['title']
        snippet = item['snippet']
        
        print(f"正在深入分析网页 ({i+1}/{len(valid_results)}): {title}")
        
        # 获取网页内容
        content = fetch_url_content(url)
        detailed_summary = ""
        
        if content:
            # 总结内容
            print(f"正在生成摘要: {url}")
            detailed_summary = summarize_web_content(content, user_requirement)
        
        # 构建这一条目的完整报告
        entry = f"### 来源 {i+1}: {title}\n链接: {url}\n"
        if snippet:
            entry += f"搜索摘要: {snippet}\n"
        if detailed_summary:
            entry += f"**详细内容分析**: \n{detailed_summary}\n"
        else:
            entry += "(无法获取详细内容或内容不相关)\n"
            
        final_summary_parts.append(entry)
        
    result_text = "\n\n".join(final_summary_parts)
    
    print(f"深度搜索分析完成，包含 {len(final_summary_parts)} 个来源")
    return {"search_results": result_text}

def strategy_generator(state: AgentState) -> Dict[str, Any]:
    """
    策略生成节点 (支持 ReAct 模式)
    """
    print("--- Node: Strategy Generator (ReAct) ---")
    user_requirement = state["user_requirement"]
    current_code = state.get("current_code")
    iteration_count = state["iteration_count"]
    backtest_results = state.get("backtest_results")
    error_logs = state.get("error_logs")
    search_results = state.get("search_results", "")
    factor_query_results = state.get("factor_query_results", "")
    
    has_strategy = state.get("has_strategy", False)
    
    # 准备工具列表
    tools = [search_tool]
    
    if has_strategy and current_code:
        # 优化模式
        print(f"使用策略优化模型优化现有策略 (迭代 {iteration_count})")
        
        feedback = ""
        if error_logs:
            feedback += f"代码执行错误:\n" + "\n".join(error_logs) + "\n请修复代码中的错误并重新生成策略。\n"
        if backtest_results:
            metrics = backtest_results.get("metrics", {})
            feedback += f"Backtest Metrics:\n{metrics}\n"
        
        if not feedback:
            feedback = f"用户新的优化需求: {user_requirement}\n"
            
        # 格式化系统提示词
        system_message = STRATEGY_OPTIMIZATION_SYSTEM_PROMPT.format(
            iteration_count=iteration_count,
            user_requirement=user_requirement,
            feedback=feedback
        )
        
        # 使用 LangGraph React Agent 进行优化
        agent_executor = create_agent(optimizer_llm, tools, system_prompt=system_message)
        
        # 输入消息包含当前代码
        inputs = {"messages": [("user", f"Current Code:\n{current_code}")]}
        
        response = agent_executor.invoke(inputs)
        code = response["messages"][-1].content
        
    else:
        # 首次生成模式
        print(f"使用代码生成模型生成初始策略: {user_requirement}")
        
        additional_info = []
        if search_results:
            additional_info.append(f"搜索到的相关信息:\n{search_results}")
        if factor_query_results:
            additional_info.append(f"推荐的量化因子:\n{factor_query_results}")
            
        # 系统提示词直接使用常量
        system_message = STRATEGY_GENERATION_SYSTEM_PROMPT
        
        # 构建用户输入消息
        user_input = f"请根据以下用户需求生成策略代码：\n{user_requirement}"
        if additional_info:
            user_input += "\n\n" + "\n\n".join(additional_info)
            
        # 使用 LangGraph React Agent
        agent_executor = create_agent(code_generator_llm, tools, system_prompt=system_message)
        
        inputs = {"messages": [("user", user_input)]}
        
        response = agent_executor.invoke(inputs)
        code = response["messages"][-1].content

    clean_c = clean_code(code)
    return {
        "current_code": clean_c, 
        "iteration_count": iteration_count + 1,
        "has_strategy": True
    }

def syntax_checker(state: AgentState) -> Dict[str, Any]:
    """
    语法检查节点
    """
    print("--- Node: Syntax Checker ---")
    code = state["current_code"]
    try:
        ast.parse(code)
        print("Syntax check passed.")
        return {"error_logs": []} # 清除之前的错误（如果有）
    except SyntaxError as e:
        error_msg = f"SyntaxError: {e}"
        print(error_msg)
        return {"error_logs": [error_msg]} # 将错误传递给状态，以便生成器修复

def backtest_executor(state: AgentState) -> Dict[str, Any]:
    """
    回测执行节点
    调用 Freqtrade MCP 工具
    """
    print("--- Node: Backtest Executor ---")
    code = state["current_code"]
    
    # 如果在上一步（语法检查）发现了错误，则跳过回测，直接返回（这将导致流程回到生成器）
    if state.get("error_logs"):
        print("Skipping backtest due to syntax errors.")
        return {} 

    # 从 state 中获取回测参数
    pairs = state.get("pairs", ["BTC/USDT", "ETH/USDT"])
    timeframe = state.get("timeframe", "5m")
    timerange = state.get("timerange", "20230101-20231231")
    
    print(f"回测参数: pairs={pairs}, timeframe={timeframe}, timerange={timerange}")
    
    # 执行真实回测，如果失败则直接返回异常
    result = run_freqtrade_backtest_auto(
        code, 
        timerange=timerange,
        pair_list=pairs,
        timeframe=timeframe
    )
    
    if "error" in result:
        error_type = result.get("error_type", "execution_error")
        error_msg = result["error"]
        
        # 如果是代码错误，提取详细的错误信息（包括 stderr）反馈给生成器
        if error_type == "code_error":
            stderr = result.get("stderr", "")
            stdout = result.get("stdout", "")
            # 提取关键错误信息
            detailed_error = f"{error_msg}\n"
            if stderr:
                # 提取完整的 Traceback 和错误信息
                lines = stderr.split('\n')
                error_lines = []
                in_traceback = False
                last_error_line = -1
                
                # 找到 Traceback 开始的位置
                for i, line in enumerate(lines):
                    if 'Traceback' in line or 'Fatal exception' in line.lower():
                        in_traceback = True
                        error_lines.append(line)
                    elif in_traceback:
                        error_lines.append(line)
                        # 记录最后一个包含 Error 或 Exception 的行
                        if any(keyword in line for keyword in ['Error', 'Exception', 'AttributeError', 'SyntaxError', 
                                                               'ImportError', 'NameError', 'TypeError', 'ValueError']):
                            last_error_line = len(error_lines) - 1
                        # 如果遇到空行且已经找到了错误信息，可以停止（但继续收集一些上下文）
                        if not line.strip() and last_error_line >= 0 and len(error_lines) > last_error_line + 3:
                            break
                
                # 如果找到了错误，提取完整的 Traceback 和错误信息
                if error_lines:
                    # 如果找到了最后一个错误行，只取到该行及之后2行
                    if last_error_line >= 0:
                        detailed_error += "\n详细错误信息:\n" + "\n".join(error_lines[:last_error_line + 3])
                    else:
                        # 否则取所有错误行（最多30行）
                        detailed_error += "\n详细错误信息:\n" + "\n".join(error_lines[:30])
            print(f"Backtest failed (代码错误): {error_msg}")
            return {
                "error_logs": [detailed_error],
                "backtest_results": None,
                "is_code_error": True  # 标记为代码错误，用于后续处理
            }
        elif error_type == "timeout":
            print(f"Backtest failed (超时): {error_msg}")
            return {
                "error_logs": [f"回测超时: {error_msg}"],
                "backtest_results": None,
                "is_timeout": True  # 标记为超时
            }
        else:
            print(f"Backtest failed: {error_msg}")
            return {"error_logs": [error_msg], "backtest_results": None}
    
    print("Backtest completed successfully.")
    return {"backtest_results": result, "error_logs": []}

def evaluator(state: AgentState) -> Dict[str, Any]:
    """
    评估节点
    决定是否满足要求
    """
    print("--- Node: Evaluator ---")
    results = state.get("backtest_results")
    errors = state.get("error_logs")
    iteration_count = state["iteration_count"]
    
    # 如果有错误，肯定不满意
    if errors:
        return {"is_satisfactory": False}
        
    if not results or "metrics" not in results:
        # 异常情况
        return {"is_satisfactory": False, "error_logs": ["No metrics found in backtest results"]}
        
    metrics = results["metrics"]
    
    # 简单的评估逻辑
    profit_pct = metrics.get("profit_total_pct", 0)
    trades = metrics.get("total_trades", 0)
    
    print(f"Evaluation: Profit={profit_pct}%, Trades={trades}")
    
    # 设定评估标准：盈利 > 10% 且 有交易
    # 如果收益率 > 10%，则不需要优化
    is_good = profit_pct > 10 and trades > 0
    
    # 或者达到最大迭代次数 (在 graph 中通常会检查，但这里也可以标记)
    # 注意：graph 路由逻辑通常处理最大迭代退出，这里主要评估质量
    
    return {"is_satisfactory": is_good}

def report_generator(state: AgentState) -> Dict[str, Any]:
    """
    报告生成节点
    根据策略代码和回测结果生成策略报告
    """
    print("--- Node: Report Generator ---")
    user_requirement = state["user_requirement"]
    current_code = state.get("current_code", "")
    backtest_results = state.get("backtest_results", {})
    
    # 如果没有代码或回测结果，返回空报告
    if not current_code:
        print("警告：没有策略代码，无法生成报告")
        return {"strategy_report": "策略生成失败，无法生成报告。"}
    
    # 格式化回测结果
    if backtest_results and "metrics" in backtest_results:
        metrics = backtest_results["metrics"]
        formatted_results = f"""
总收益率: {metrics.get('profit_total_pct', 0):.2f}%
总交易次数: {metrics.get('total_trades', 0)}
胜率: {metrics.get('wins', 0) / max(metrics.get('total_trades', 1), 1) * 100:.2f}%
平均收益: {metrics.get('profit_mean_pct', 0):.2f}%
最大回撤: {metrics.get('max_drawdown_pct', 0):.2f}%
"""
    else:
        formatted_results = "回测未成功完成或无结果数据。"
    
    try:
        print("使用代码生成模型生成策略报告...")
        chain = report_generation_prompt | code_generator_llm | StrOutputParser()
        report = chain.invoke({
            "user_requirement": user_requirement,
            "strategy_code": current_code,
            "backtest_results": formatted_results
        })
        
        print("策略报告生成成功")
        return {"strategy_report": report}
    except Exception as e:
        error_msg = f"报告生成失败: {str(e)}"
        print(error_msg)
        return {"strategy_report": error_msg}
