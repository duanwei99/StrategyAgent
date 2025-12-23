"""
因子库管理器
管理量化因子的存储、查询和检索
"""
import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict

@dataclass
class FactorInfo:
    """因子信息数据类"""
    name: str  # 因子名称
    signal_type: str  # 信号类型: Trend, Mean Reversion, Carry, Volatility, Risk-off
    frequency: str  # 数据频率: 5m, 15m, 1h, 4h, 1d
    data_source: str  # 数据来源
    calculation: str  # 计算方式（代码或描述）
    regime_dependency: str  # 生效市场状态
    intuition: str  # 经济/行为直觉
    applicable_scenarios: List[str]  # 适用场景列表
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FactorInfo':
        return cls(**data)

class FactorManager:
    """因子库管理器"""
    
    def __init__(self, library_dir: Optional[str] = None):
        if library_dir is None:
            # 默认使用当前文件所在目录
            current_dir = Path(__file__).parent
            library_dir = str(current_dir / "factors")
        self.library_dir = Path(library_dir)
        self.library_dir.mkdir(parents=True, exist_ok=True)
        self.index_file = self.library_dir.parent / "factor_index.json"
        self.factors: Dict[str, FactorInfo] = {}
        self._load_index()
    
    def _load_index(self):
        """加载因子索引"""
        if self.index_file.exists():
            try:
                with open(self.index_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.factors = {
                        name: FactorInfo.from_dict(factor_data)
                        for name, factor_data in data.items()
                    }
            except Exception as e:
                print(f"加载因子索引失败: {e}")
                self.factors = {}
        else:
            self.factors = {}
    
    def _save_index(self):
        """保存因子索引"""
        data = {
            name: factor.to_dict()
            for name, factor in self.factors.items()
        }
        with open(self.index_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def add_factor(self, factor: FactorInfo):
        """添加因子"""
        self.factors[factor.name] = factor
        self._save_index()
    
    def get_factor(self, name: str) -> Optional[FactorInfo]:
        """获取因子"""
        return self.factors.get(name)
    
    def search_factors(
        self,
        signal_type: Optional[str] = None,
        frequency: Optional[str] = None,
        scenario_keywords: Optional[List[str]] = None,
        name_keywords: Optional[List[str]] = None
    ) -> List[FactorInfo]:
        """搜索因子"""
        results = []
        
        for factor in self.factors.values():
            # 按信号类型过滤
            if signal_type and factor.signal_type != signal_type:
                continue
            
            # 按频率过滤
            if frequency and factor.frequency != frequency:
                continue
            
            # 按场景关键词过滤
            if scenario_keywords:
                factor_text = ' '.join([
                    factor.intuition,
                    ' '.join(factor.applicable_scenarios),
                    factor.regime_dependency
                ]).lower()
                if not any(kw.lower() in factor_text for kw in scenario_keywords):
                    continue
            
            # 按名称关键词过滤
            if name_keywords:
                factor_name_lower = factor.name.lower()
                if not any(kw.lower() in factor_name_lower for kw in name_keywords):
                    continue
            
            results.append(factor)
        
        return results
    
    def query_factors_by_requirement(self, requirement: str) -> List[FactorInfo]:
        """根据用户需求查询合适的因子"""
        requirement_lower = requirement.lower()
        
        # 提取关键词
        keywords = []
        
        # 检测信号类型关键词
        signal_type = None
        if any(x in requirement_lower for x in ['趋势', 'trend', '动量', 'momentum']):
            signal_type = 'Trend'
        elif any(x in requirement_lower for x in ['均值回归', 'mean reversion', '反转', 'reversal', '超买', '超卖']):
            signal_type = 'Mean Reversion'
        elif any(x in requirement_lower for x in ['波动', 'volatility', '波动率']):
            signal_type = 'Volatility'
        elif any(x in requirement_lower for x in ['利差', 'carry', '资金费率', 'funding']):
            signal_type = 'Carry'
        elif any(x in requirement_lower for x in ['风险', 'risk', '保护', 'protection']):
            signal_type = 'Risk-off'
        
        # 检测频率关键词
        frequency = None
        if '5m' in requirement_lower or '5分钟' in requirement_lower:
            frequency = '5m'
        elif '15m' in requirement_lower or '15分钟' in requirement_lower:
            frequency = '15m'
        elif '1h' in requirement_lower or '1小时' in requirement_lower:
            frequency = '1h'
        elif '4h' in requirement_lower or '4小时' in requirement_lower:
            frequency = '4h'
        elif '1d' in requirement_lower or '1天' in requirement_lower or '日线' in requirement_lower:
            frequency = '1d'
        
        # 提取其他关键词
        common_keywords = ['rsi', 'macd', 'bollinger', '布林', 'kdj', 'cci', 'aroon', 
                          'stoch', 'willr', 'roc', 'adx', 'ema', 'sma', 'ma']
        for kw in common_keywords:
            if kw in requirement_lower:
                keywords.append(kw)
        
        # 搜索因子
        factors = self.search_factors(
            signal_type=signal_type,
            frequency=frequency,
            name_keywords=keywords if keywords else None,
            scenario_keywords=None
        )
        
        # 如果没有找到，尝试更宽泛的搜索
        if not factors:
            factors = self.search_factors(
                name_keywords=keywords if keywords else None
            )
        
        return factors
    
    def get_all_factors(self) -> List[FactorInfo]:
        """获取所有因子"""
        return list(self.factors.values())
    
    def generate_summary_doc(self) -> str:
        """生成因子总览文档"""
        lines = ["# 量化因子库总览\n"]
        lines.append(f"总计因子数量: {len(self.factors)}\n\n")
        
        # 按信号类型分组
        by_type = {}
        for factor in self.factors.values():
            if factor.signal_type not in by_type:
                by_type[factor.signal_type] = []
            by_type[factor.signal_type].append(factor)
        
        for signal_type, factors in sorted(by_type.items()):
            lines.append(f"## {signal_type} 类型因子 ({len(factors)}个)\n")
            for factor in sorted(factors, key=lambda x: x.name):
                lines.append(f"### {factor.name}\n")
                lines.append(f"- **频率**: {factor.frequency}\n")
                lines.append(f"- **数据来源**: {factor.data_source}\n")
                lines.append(f"- **直觉**: {factor.intuition}\n")
                lines.append(f"- **适用场景**: {', '.join(factor.applicable_scenarios)}\n")
                lines.append(f"- **生效条件**: {factor.regime_dependency}\n")
                lines.append(f"- **计算方式**: `{factor.calculation[:100]}...`\n\n")
        
        return '\n'.join(lines)

