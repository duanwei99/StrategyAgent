import ast
import os
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from .state import AgentState
from .prompts import generation_prompt, optimization_prompt
from ..tools.freqtrade_mcp import run_freqtrade_backtest

# 初始化 LLM
# 假设环境变量 OPENAI_API_KEY 已设置，或者使用其他兼容 OpenAI 协议的模型
llm = ChatOpenAI(model="gpt-4-turbo", temperature=0.2)

def clean_code(code: str) -> str:
    """清理 LLM 返回的代码，去除 markdown 标记"""
    if "```python" in code:
        code = code.split("```python")[1].split("```")[0]
    elif "```" in code:
        code = code.split("```")[1].split("```")[0]
    return code.strip()

def strategy_generator(state: AgentState) -> Dict[str, Any]:
    """
    策略生成节点
    根据用户需求或优化反馈生成/修改代码
    """
    print("--- Node: Strategy Generator ---")
    user_requirement = state["user_requirement"]
    current_code = state.get("current_code")
    iteration_count = state["iteration_count"]
    backtest_results = state.get("backtest_results")
    error_logs = state.get("error_logs")
    
    # 判断是首次生成还是优化
    if not current_code or iteration_count == 0:
        # 首次生成
        print(f"Generating initial strategy for: {user_requirement}")
        chain = generation_prompt | llm | StrOutputParser()
        code = chain.invoke({"user_requirement": user_requirement})
    else:
        # 优化/修复
        print(f"Optimizing strategy (Iteration {iteration_count})")
        
        feedback = ""
        if error_logs:
            feedback += f"Errors encountered:\n{error_logs}\n"
        if backtest_results:
            metrics = backtest_results.get("metrics", {})
            feedback += f"Backtest Metrics:\n{metrics}\n"
            
        chain = optimization_prompt | llm | StrOutputParser()
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

    # 执行回测
    # 这里为了演示，使用硬编码的 timerange，实际可从 state 或 config 读取
    result = run_freqtrade_backtest(code, timerange="20230101-20230201")
    
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
