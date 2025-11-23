import ast
import os
import requests
from typing import Dict, Any
from langchain_core.output_parsers import StrOutputParser
from .state import AgentState
from .prompts import generation_prompt, optimization_prompt, generation_with_search_prompt, report_generation_prompt
from ..tools.freqtrade_mcp_mock import run_freqtrade_backtest_auto
from ..llm_config import llm_config

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

def web_search_node(state: AgentState) -> Dict[str, Any]:
    """
    联网搜索节点
    在首次生成策略前，搜索相关的策略开发最佳实践和建议
    """
    print("--- Node: Web Search ---")
    user_requirement = state["user_requirement"]
    iteration_count = state["iteration_count"]
    
    # 只在首次生成时进行搜索
    if iteration_count > 0:
        print("跳过搜索（非首次生成）")
        return {}
    
    # 构建搜索查询
    search_query = f"freqtrade trading strategy {user_requirement} best practices technical indicators"
    print(f"搜索查询: {search_query}")
    
    try:
        # 使用 DuckDuckGo 搜索 API (免费且无需API key)
        search_url = "https://api.duckduckgo.com/"
        params = {
            "q": search_query,
            "format": "json",
            "no_html": "1",
            "skip_disambig": "1"
        }
        
        response = requests.get(search_url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # 提取摘要和相关主题
            search_summary = []
            
            # 获取抽象摘要
            if data.get("AbstractText"):
                search_summary.append(f"摘要: {data['AbstractText']}")
            
            # 获取相关主题
            if data.get("RelatedTopics"):
                topics = []
                for topic in data["RelatedTopics"][:5]:  # 只取前5个
                    if isinstance(topic, dict) and "Text" in topic:
                        topics.append(topic["Text"])
                if topics:
                    search_summary.append("相关信息:\n" + "\n".join(f"- {t}" for t in topics))
            
            if search_summary:
                result_text = "\n\n".join(search_summary)
                print(f"搜索成功，获得 {len(search_summary)} 条信息")
                return {"search_results": result_text}
            else:
                print("搜索未返回有用信息")
                return {"search_results": "未找到相关搜索结果"}
        else:
            print(f"搜索API返回错误: {response.status_code}")
            return {"search_results": "搜索服务暂时不可用"}
            
    except Exception as e:
        print(f"搜索出错: {str(e)}")
        # 搜索失败不影响整体流程，返回空结果继续
        return {"search_results": f"搜索出错: {str(e)}"}

def strategy_generator(state: AgentState) -> Dict[str, Any]:
    """
    策略生成节点
    根据用户需求或优化反馈生成/修改代码
    使用不同的专用模型处理代码生成和优化任务
    """
    print("--- Node: Strategy Generator ---")
    user_requirement = state["user_requirement"]
    current_code = state.get("current_code")
    iteration_count = state["iteration_count"]
    backtest_results = state.get("backtest_results")
    error_logs = state.get("error_logs")
    search_results = state.get("search_results", "")
    
    # 判断是首次生成还是优化
    if not current_code or iteration_count == 0:
        # 首次生成 - 使用代码生成模型，整合搜索结果
        print(f"使用代码生成模型生成初始策略: {user_requirement}")
        
        # 如果有搜索结果，使用包含搜索结果的提示词
        if search_results:
            print("整合搜索结果到策略生成中...")
            chain = generation_with_search_prompt | code_generator_llm | StrOutputParser()
            code = chain.invoke({
                "user_requirement": user_requirement,
                "search_results": search_results
            })
        else:
            chain = generation_prompt | code_generator_llm | StrOutputParser()
            code = chain.invoke({"user_requirement": user_requirement})
    else:
        # 优化/修复 - 使用策略优化模型
        print(f"使用策略优化模型优化策略 (迭代 {iteration_count})")
        
        feedback = ""
        if error_logs:
            feedback += f"Errors encountered:\n{error_logs}\n"
        if backtest_results:
            metrics = backtest_results.get("metrics", {})
            feedback += f"Backtest Metrics:\n{metrics}\n"
            
        chain = optimization_prompt | optimizer_llm | StrOutputParser()
        code = chain.invoke({
            "user_requirement": user_requirement,
            "iteration_count": iteration_count,
            "feedback": feedback,
            "current_code": current_code
        })

    clean_c = clean_code(code)
    return {"current_code": clean_c, "iteration_count": iteration_count + 1}

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

    # 执行回测（自动选择真实回测或模拟回测）
    # 这里为了演示，使用硬编码的 timerange，实际可从 state 或 config 读取
    result = run_freqtrade_backtest_auto(code, timerange="20230101-20230201")
    
    if "error" in result:
        print(f"Backtest failed: {result['error']}")
        return {"error_logs": [result["error"]], "backtest_results": None}
    
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
    
    # 设定简单的通过标准：盈利 > 0 且 有交易
    # 实际项目中这里会更复杂
    is_good = profit_pct > 0 and trades > 0
    
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
