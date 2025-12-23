"""
因子查询节点
使用 LLM 智能选择适合的因子
"""
from typing import Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import json

from ..llm_config import llm_config
from .factor_manager import FactorManager, FactorInfo
from ..agent.state import AgentState

# 全局因子管理器实例
_factor_manager = None

def get_factor_manager() -> FactorManager:
    """获取因子管理器单例"""
    global _factor_manager
    if _factor_manager is None:
        _factor_manager = FactorManager()
    return _factor_manager

# 因子查询的 Prompt 模板
FACTOR_QUERY_PROMPT = """你是一个专业的量化交易因子选择专家。你的任务是根据用户的策略需求，从因子库中智能选择最合适的因子。

## 用户需求：
{user_requirement}

## 可用因子库：
{factors_summary}

## 任务要求：
1. **深入理解用户需求**：
   - 分析策略的交易目标（趋势跟踪、均值回归、套利等）
   - 识别策略的交易风格（短期、中期、长期）
   - 理解策略偏好的市场状态（震荡、趋势、高波动等）

2. **智能选择因子**（建议选择5-15个因子）：
   - 优先选择与用户需求高度匹配的因子
   - 考虑因子的互补性：选择不同类型的因子（趋势、均值回归、波动率、风险控制等）以构建完整的策略
   - 考虑时间框架的多样性：如果策略需要多时间框架分析，选择不同频率的因子（5m、15m、1h、4h、1d）
   - 确保选择的因子能够覆盖策略的核心逻辑需求

3. **因子选择原则**：
   - 如果用户需求明确提到某个指标（如RSI、MACD、布林带等），优先选择相关因子
   - 如果用户需求提到"趋势"、"动量"等，优先选择 Trend 类型因子
   - 如果用户需求提到"反转"、"超买超卖"等，优先选择 Mean Reversion 类型因子
   - 如果用户需求提到"波动率"、"风险"等，优先选择 Volatility 或 Risk-off 类型因子
   - 如果用户需求提到"资金费率"、"利差"等，优先选择 Carry 类型因子

4. **输出要求**：
   - 必须输出有效的 JSON 格式
   - selected_factors 数组中的因子名称必须与因子库中的名称完全一致
   - reasoning 字段要详细说明选择理由，包括每个因子如何满足用户需求

## 输出格式：
请以 JSON 格式输出，包含以下字段：
{{
    "selected_factors": ["因子名称1", "因子名称2", ...],
    "reasoning": "选择这些因子的详细理由，说明为什么这些因子适合用户需求，每个因子如何满足策略需求"
}}

只输出 JSON，不要输出其他内容。"""

def format_factors_for_llm(factors: list[FactorInfo]) -> str:
    """
    格式化因子信息，方便 LLM 理解
    每个因子包含：名称、信号类型、频率、经济直觉、适用场景、生效条件
    优化描述，使其更适合 LLM 理解和选择
    """
    lines = []
    lines.append(f"## 因子库总览")
    lines.append(f"总计 {len(factors)} 个可用因子\n")
    lines.append("每个因子包含以下信息：")
    lines.append("- **名称**: 因子的唯一标识符")
    lines.append("- **信号类型**: Trend（趋势）、Mean Reversion（均值回归）、Volatility（波动率）、Risk-off（风险规避）、Carry（利差）")
    lines.append("- **频率**: 因子的时间周期（5m、15m、1h、4h、1d）")
    lines.append("- **经济直觉**: 该因子捕捉的市场非理性或结构性行为")
    lines.append("- **适用场景**: 该因子最适合的交易场景")
    lines.append("- **生效条件**: 该因子生效所需的市场状态\n")
    
    # 按信号类型分组
    by_type = {}
    for factor in factors:
        if factor.signal_type not in by_type:
            by_type[factor.signal_type] = []
        by_type[factor.signal_type].append(factor)
    
    for signal_type, type_factors in sorted(by_type.items()):
        lines.append(f"\n## {signal_type} 类型因子 ({len(type_factors)}个)")
        lines.append(f"这类因子主要用于: {_get_signal_type_description(signal_type)}\n")
        
        for factor in sorted(type_factors, key=lambda x: x.name):
            lines.append(f"### {factor.name}")
            lines.append(f"- **信号类型**: {factor.signal_type}")
            lines.append(f"- **频率**: {factor.frequency}")
            lines.append(f"- **数据来源**: {factor.data_source}")
            lines.append(f"- **经济直觉**: {factor.intuition}")
            lines.append(f"- **适用场景**: {', '.join(factor.applicable_scenarios)}")
            lines.append(f"- **生效条件**: {factor.regime_dependency}")
            lines.append("")  # 空行分隔
    
    return '\n'.join(lines)

def _get_signal_type_description(signal_type: str) -> str:
    """获取信号类型的描述"""
    descriptions = {
        "Trend": "识别和跟踪价格趋势方向，适用于趋势跟踪策略",
        "Mean Reversion": "识别价格偏离均值的情况，适用于震荡市场的反转交易",
        "Volatility": "衡量市场波动率水平，适用于波动率交易和风险管理",
        "Risk-off": "识别市场风险状态，适用于风险控制和保护性策略",
        "Carry": "捕捉利差和资金费率相关的机会，适用于套利策略"
    }
    return descriptions.get(signal_type, "通用信号类型")

def factor_query_node(state: AgentState) -> Dict[str, Any]:
    """
    因子查询节点
    使用 LLM 根据用户需求智能选择合适的因子
    """
    print("--- Node: Factor Query ---")
    
    user_requirement = state.get("user_requirement", "")
    iteration_count = state.get("iteration_count", 0)
    
    # 如果非首次生成，跳过因子查询
    if iteration_count > 0:
        print("跳过因子查询（非首次生成）")
        return {}
    
    if not user_requirement:
        print("用户需求为空，跳过因子查询")
        return {}
    
    manager = get_factor_manager()
    all_factors = manager.get_all_factors()
    
    if not all_factors:
        print("因子库为空，跳过因子查询")
        return {"factor_query_results": "因子库为空"}
    
    print(f"因子库中共有 {len(all_factors)} 个因子，使用 LLM 智能选择...")
    
    # 格式化因子信息供 LLM 阅读
    factors_summary = format_factors_for_llm(all_factors)
    
    # 使用最强大的模型（optimizer）进行因子选择
    llm = llm_config.get_optimizer_llm()
    
    # 创建 prompt chain
    prompt = ChatPromptTemplate.from_template(FACTOR_QUERY_PROMPT)
    chain = prompt | llm | StrOutputParser()
    
    try:
        # 调用 LLM 选择因子
        response = chain.invoke({
            "user_requirement": user_requirement,
            "factors_summary": factors_summary
        })
        
        # 解析 LLM 返回的 JSON
        # 移除可能的 markdown 代码块标记
        response_clean = response.strip()
        if response_clean.startswith("```json"):
            response_clean = response_clean[7:]
        if response_clean.startswith("```"):
            response_clean = response_clean[3:]
        if response_clean.endswith("```"):
            response_clean = response_clean[:-3]
        response_clean = response_clean.strip()
        
        result = json.loads(response_clean)
        selected_factor_names = result.get("selected_factors", [])
        reasoning = result.get("reasoning", "")
        
        print(f"LLM 选择了 {len(selected_factor_names)} 个因子")
        print(f"选择理由: {reasoning[:200]}...")
        
        # 获取选中的因子详细信息
        selected_factors = []
        for name in selected_factor_names:
            factor = manager.get_factor(name)
            if factor:
                selected_factors.append(factor)
            else:
                print(f"警告: 因子 {name} 不存在于因子库中")
        
        if not selected_factors:
            print("LLM 选择的因子都不存在于因子库中，使用所有因子")
            selected_factors = all_factors[:15]  # 最多返回15个
        
        # 格式化查询结果
        result_text = f"根据您的需求「{user_requirement}」，LLM 智能选择了以下 {len(selected_factors)} 个适用的量化因子：\n\n"
        result_text += f"**选择理由**: {reasoning}\n\n"
        
        for i, factor in enumerate(selected_factors, 1):
            result_text += f"## {i}. {factor.name}\n"
            result_text += f"- **信号类型**: {factor.signal_type}\n"
            result_text += f"- **频率**: {factor.frequency}\n"
            result_text += f"- **数据来源**: {factor.data_source}\n"
            result_text += f"- **经济直觉**: {factor.intuition}\n"
            result_text += f"- **适用场景**: {', '.join(factor.applicable_scenarios)}\n"
            result_text += f"- **生效条件**: {factor.regime_dependency}\n"
            result_text += f"- **计算方式**:\n```python\n{factor.calculation}\n```\n\n"
        
        return {"factor_query_results": result_text}
        
    except json.JSONDecodeError as e:
        print(f"LLM 返回格式错误，尝试使用关键词匹配: {e}")
        # 如果 LLM 返回格式错误，回退到关键词匹配
        factors = manager.query_factors_by_requirement(user_requirement)
        if factors:
            selected_factors = factors[:15]
            result_text = f"根据您的需求「{user_requirement}」，找到以下 {len(selected_factors)} 个适用的量化因子：\n\n"
            for i, factor in enumerate(selected_factors, 1):
                result_text += f"## {i}. {factor.name}\n"
                result_text += f"- **信号类型**: {factor.signal_type}\n"
                result_text += f"- **频率**: {factor.frequency}\n"
                result_text += f"- **数据来源**: {factor.data_source}\n"
                result_text += f"- **经济直觉**: {factor.intuition}\n"
                result_text += f"- **适用场景**: {', '.join(factor.applicable_scenarios)}\n"
                result_text += f"- **生效条件**: {factor.regime_dependency}\n"
                result_text += f"- **计算方式**:\n```python\n{factor.calculation}\n```\n\n"
            return {"factor_query_results": result_text}
        else:
            return {"factor_query_results": "未找到匹配的因子"}
    
    except Exception as e:
        print(f"因子查询出错: {e}")
        return {"factor_query_results": f"因子查询出错: {str(e)}"}
