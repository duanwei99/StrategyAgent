from typing import TypedDict, Optional, List, Dict, Any

class AgentState(TypedDict):
    user_requirement: str
    current_code: Optional[str]
    iteration_count: int
    backtest_results: Optional[Dict[str, Any]]
    error_logs: List[str]
    is_satisfactory: bool
    search_results: Optional[str]  # 联网搜索结果
    strategy_report: Optional[str]  # 策略报告（适用场景和注意事项）

