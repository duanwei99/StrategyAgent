from langgraph.graph import StateGraph, END
from .state import AgentState
from .nodes import strategy_generator, syntax_checker, backtest_executor, evaluator

# 定义最大迭代次数常量 (也可以从 state 中读取配置)
MAX_ITERATIONS = 5

def route_after_syntax_check(state: AgentState):
    """根据语法检查结果路由"""
    if state.get("error_logs"):
        return "strategy_generator"
    return "backtest_executor"

def route_after_evaluation(state: AgentState):
    """根据评估结果路由"""
    if state.get("is_satisfactory"):
        return END
    
    if state["iteration_count"] >= MAX_ITERATIONS:
        return END
        
    return "strategy_generator"

def create_graph():
    """构建 LangGraph 工作流"""
    workflow = StateGraph(AgentState)

    # 添加节点
    workflow.add_node("strategy_generator", strategy_generator)
    workflow.add_node("syntax_checker", syntax_checker)
    workflow.add_node("backtest_executor", backtest_executor)
    workflow.add_node("evaluator", evaluator)

    # 定义边
    workflow.set_entry_point("strategy_generator")
    
    workflow.add_edge("strategy_generator", "syntax_checker")
    
    # 语法检查后的条件分支
    workflow.add_conditional_edges(
        "syntax_checker",
        route_after_syntax_check,
        {
            "strategy_generator": "strategy_generator",
            "backtest_executor": "backtest_executor"
        }
    )
    
    workflow.add_edge("backtest_executor", "evaluator")
    
    # 评估后的条件分支
    workflow.add_conditional_edges(
        "evaluator",
        route_after_evaluation,
        {
            END: END,
            "strategy_generator": "strategy_generator"
        }
    )

    # 编译图
    app = workflow.compile()
    return app
