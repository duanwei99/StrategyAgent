from typing import TypedDict, Optional, List, Dict, Any

class AgentState(TypedDict):
    user_requirement: str
    current_code: Optional[str]
    iteration_count: int
    backtest_results: Optional[Dict[str, Any]]
    error_logs: List[str]
    is_satisfactory: bool

