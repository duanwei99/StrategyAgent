from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from .state import AgentState
from .nodes import strategy_generator, syntax_checker, backtest_executor, evaluator, web_search_node, report_generator
from ..factor_library.factor_query_node import factor_query_node

# 定义最大迭代次数常量 (也可以从 state 中读取配置)
MAX_ITERATIONS = 5

# 创建内存检查点保存器，用于管理会话记忆
checkpointer = MemorySaver()

def route_after_syntax_check(state: AgentState):
    """根据语法检查结果路由"""
    if state.get("error_logs"):
        return "strategy_generator"
    return "backtest_executor"

def route_after_evaluation(state: AgentState):
    """根据评估结果路由"""
    # 如果满意或达到最大迭代次数，生成报告
    if state.get("is_satisfactory"):
        return "report_generator"
    
    if state["iteration_count"] >= MAX_ITERATIONS:
        return "report_generator"
        
    return "strategy_generator"

def create_graph():
    """构建 LangGraph 工作流"""
    workflow = StateGraph(AgentState)

    # 添加节点
    workflow.add_node("web_search", web_search_node)  # 联网搜索节点
    workflow.add_node("factor_query", factor_query_node)  # 因子查询节点
    workflow.add_node("strategy_generator", strategy_generator)
    workflow.add_node("syntax_checker", syntax_checker)
    workflow.add_node("backtest_executor", backtest_executor)
    workflow.add_node("evaluator", evaluator)
    workflow.add_node("report_generator", report_generator)  # 报告生成节点

    # 定义边
    # 工作流从搜索节点开始
    workflow.set_entry_point("web_search")
    
    # 搜索完成后进入因子查询
    workflow.add_edge("web_search", "factor_query")
    
    # 因子查询完成后进入策略生成
    workflow.add_edge("factor_query", "strategy_generator")
    
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
            "report_generator": "report_generator",
            "strategy_generator": "strategy_generator"
        }
    )
    
    # 报告生成后结束
    workflow.add_edge("report_generator", END)

    # 编译图，添加 checkpointer 以支持会话记忆
    app = workflow.compile(checkpointer=checkpointer)
    return app
