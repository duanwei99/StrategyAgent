from typing import TypedDict, Optional, List, Dict, Any

class AgentState(TypedDict):
    user_requirement: str
    current_code: Optional[str]
    iteration_count: int
    backtest_results: Optional[Dict[str, Any]]
    error_logs: List[str]
    is_satisfactory: bool
    search_results: Optional[str]  # 联网搜索结果
    factor_query_results: Optional[str]  # 因子查询结果
    strategy_report: Optional[str]  # 策略报告（适用场景和注意事项）
    pairs: Optional[List[str]]  # 交易对列表
    timeframe: Optional[str]  # 时间周期
    timerange: Optional[str]  # 回测时间范围
    has_strategy: bool  # 会话中是否已有策略代码（用于判断是优化还是生成新策略）

