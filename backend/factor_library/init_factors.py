"""
初始化因子库
基于对 NostalgiaForInfinityX7.py 中因子的深入理解，手动编写每个因子的详细信息
每个因子都包含：名称、经济直觉、信号类型、频率、计算方式、生效条件
"""
from .factor_manager import FactorManager, FactorInfo

def init_common_factors():
    """
    初始化常见因子
    基于对策略代码的深入理解，为每个因子编写详细的、有深度的描述
    """
    manager = FactorManager()
    
    # RSI 相关因子
    manager.add_factor(FactorInfo(
        name="RSI_14",
        signal_type="Mean Reversion",
        frequency="5m",
        data_source="Base timeframe OHLCV",
        calculation='import pandas_ta as pta\ndf["RSI_14"] = pta.rsi(df["close"], length=14)',
        regime_dependency="适用于震荡市场（ADX < 25），波动率中等，无明显趋势时",
        intuition="当RSI处于极端值（>70超买，<30超卖）时，市场存在单边拥挤，价格容易出现均值回归。这捕捉了市场参与者的过度反应行为",
        applicable_scenarios=["震荡市场", "超买超卖识别", "反转交易", "区间交易", "RSI策略"]
    ))
    
    manager.add_factor(FactorInfo(
        name="RSI_3",
        signal_type="Mean Reversion",
        frequency="5m",
        data_source="Base timeframe OHLCV",
        calculation='import pandas_ta as pta\ndf["RSI_3"] = pta.rsi(df["close"], length=3)',
        regime_dependency="适用于短期波动市场，需要快速响应价格变化，适合5分钟级别的快速交易",
        intuition="3周期RSI对价格变化极其敏感，能够快速捕捉短期动量的变化。当RSI_3处于极端值时，反映了市场短期的过度反应，价格容易出现快速反转",
        applicable_scenarios=["短期交易", "快速反转", "高频策略", "5分钟级别交易", "快速动量捕捉"]
    ))
    
    manager.add_factor(FactorInfo(
        name="RSI_4",
        signal_type="Mean Reversion",
        frequency="5m",
        data_source="Base timeframe OHLCV",
        calculation='import pandas_ta as pta\ndf["RSI_4"] = pta.rsi(df["close"], length=4)',
        regime_dependency="适用于短期波动，介于RSI_3和RSI_14之间",
        intuition="4周期RSI提供短期动量参考，比RSI_3更稳定，比RSI_14更敏感",
        applicable_scenarios=["短期交易", "动量分析", "超买超卖"]
    ))
    
    manager.add_factor(FactorInfo(
        name="RSI_20",
        signal_type="Mean Reversion",
        frequency="5m",
        data_source="Base timeframe OHLCV",
        calculation='import pandas_ta as pta\ndf["RSI_20"] = pta.rsi(df["close"], length=20)',
        regime_dependency="适用于中期震荡市场，需要更稳定的超买超卖信号",
        intuition="20周期RSI提供更稳定的超买超卖信号，减少了短期噪音的影响",
        applicable_scenarios=["中期震荡", "稳定超买超卖", "趋势过滤"]
    ))
    
    manager.add_factor(FactorInfo(
        name="RSI_14_1h",
        signal_type="Mean Reversion",
        frequency="1h",
        data_source="Informative timeframe",
        calculation='import pandas_ta as pta\nfrom freqtrade.strategy import merge_informative_pair\n# 在informative_1h_indicators方法中计算:\ninfo_df["RSI_14"] = pta.rsi(info_df["close"], length=14)\n# 然后合并到主数据:\ndf = merge_informative_pair(df, info_df, self.timeframe, "1h", ffill=True)\ndf["RSI_14_1h"] = df["RSI_14_1h"]',
        regime_dependency="适用于中期趋势确认，1h级别趋势明确",
        intuition="1小时级别的RSI用于过滤短期噪音，识别中期超买超卖区域",
        applicable_scenarios=["中期趋势确认", "多时间框架分析", "趋势过滤"]
    ))
    
    manager.add_factor(FactorInfo(
        name="RSI_14_4h",
        signal_type="Mean Reversion",
        frequency="4h",
        data_source="Informative timeframe",
        calculation='import pandas_ta as pta\nfrom freqtrade.strategy import merge_informative_pair\n# 在informative_4h_indicators方法中计算:\ninfo_df["RSI_14"] = pta.rsi(info_df["close"], length=14)\n# 然后合并到主数据:\ndf = merge_informative_pair(df, info_df, self.timeframe, "4h", ffill=True)\ndf["RSI_14_4h"] = df["RSI_14_4h"]',
        regime_dependency="适用于长期趋势，4h级别趋势明确，波动率较低",
        intuition="4小时级别RSI识别长期超买超卖区域，用于趋势反转判断",
        applicable_scenarios=["长期趋势", "趋势反转", "多时间框架确认"]
    ))
    
    # CCI 相关因子
    manager.add_factor(FactorInfo(
        name="CCI_20_1h",
        signal_type="Mean Reversion",
        frequency="1h",
        data_source="Informative timeframe",
        calculation='import pandas_ta as pta\nfrom freqtrade.strategy import merge_informative_pair\n# 在informative_1h_indicators方法中计算:\ninfo_df["CCI_20"] = pta.cci(info_df["high"], info_df["low"], info_df["close"], length=20)\n# 然后合并到主数据:\ndf = merge_informative_pair(df, info_df, self.timeframe, "1h", ffill=True)\ndf["CCI_20_1h"] = df["CCI_20_1h"]',
        regime_dependency="适用于趋势市场，CCI < -250 表示极度超卖",
        intuition="当CCI处于极端值时，市场存在明显的单边拥挤，价格容易出现反向波动",
        applicable_scenarios=["趋势市场", "极端值识别", "反转交易"]
    ))
    
    manager.add_factor(FactorInfo(
        name="CCI_20_4h",
        signal_type="Mean Reversion",
        frequency="4h",
        data_source="Informative timeframe",
        calculation='import pandas_ta as pta\nfrom freqtrade.strategy import merge_informative_pair\n# 在informative_4h_indicators方法中计算:\ninfo_df["CCI_20"] = pta.cci(info_df["high"], info_df["low"], info_df["close"], length=20)\n# 然后合并到主数据:\ndf = merge_informative_pair(df, info_df, self.timeframe, "4h", ffill=True)\ndf["CCI_20_4h"] = df["CCI_20_4h"]',
        regime_dependency="适用于长期趋势，CCI < -200 表示中期超卖",
        intuition="4小时级别CCI识别长期超买超卖，用于中期反转判断",
        applicable_scenarios=["长期趋势", "中期反转", "趋势确认"]
    ))
    
    # AROON 相关因子
    manager.add_factor(FactorInfo(
        name="AROONU_14_15m",
        signal_type="Trend",
        frequency="15m",
        data_source="Informative timeframe",
        calculation='import pandas_ta as pta\nimport pandas as pd\nimport numpy as np\nfrom freqtrade.strategy import merge_informative_pair\n# 在informative_15m_indicators方法中计算:\naroon_14 = pta.aroon(info_df["high"], info_df["low"], length=14)\nif isinstance(aroon_14, pd.DataFrame):\n    info_df["AROONU_14"] = aroon_14["AROONU_14"]\nelse:\n    info_df["AROONU_14"] = np.nan\n# 然后合并到主数据:\ndf = merge_informative_pair(df, info_df, self.timeframe, "15m", ffill=True)\ndf["AROONU_14_15m"] = df["AROONU_14_15m"]',
        regime_dependency="适用于趋势市场，AROONU < 70 表示上升趋势减弱",
        intuition="AROON指标识别趋势强度和方向，AROONU下降表示上升动量减弱",
        applicable_scenarios=["趋势识别", "动量分析", "趋势强度判断"]
    ))
    
    manager.add_factor(FactorInfo(
        name="AROONU_14_1h",
        signal_type="Trend",
        frequency="1h",
        data_source="Informative timeframe",
        calculation='import pandas_ta as pta\nimport pandas as pd\nimport numpy as np\nfrom freqtrade.strategy import merge_informative_pair\n# 在informative_1h_indicators方法中计算:\naroon_14 = pta.aroon(info_df["high"], info_df["low"], length=14)\nif isinstance(aroon_14, pd.DataFrame):\n    info_df["AROONU_14"] = aroon_14["AROONU_14"]\nelse:\n    info_df["AROONU_14"] = np.nan\n# 然后合并到主数据:\ndf = merge_informative_pair(df, info_df, self.timeframe, "1h", ffill=True)\ndf["AROONU_14_1h"] = df["AROONU_14_1h"]',
        regime_dependency="适用于中期趋势，需要1h级别趋势明确",
        intuition="1小时级别AROON识别中期趋势强度和方向",
        applicable_scenarios=["中期趋势", "趋势强度", "多时间框架"]
    ))
    
    manager.add_factor(FactorInfo(
        name="AROONU_14_4h",
        signal_type="Trend",
        frequency="4h",
        data_source="Informative timeframe",
        calculation='import pandas_ta as pta\nimport pandas as pd\nimport numpy as np\nfrom freqtrade.strategy import merge_informative_pair\n# 在informative_4h_indicators方法中计算:\naroon_14 = pta.aroon(info_df["high"], info_df["low"], length=14)\nif isinstance(aroon_14, pd.DataFrame):\n    info_df["AROONU_14"] = aroon_14["AROONU_14"]\nelse:\n    info_df["AROONU_14"] = np.nan\n# 然后合并到主数据:\ndf = merge_informative_pair(df, info_df, self.timeframe, "4h", ffill=True)\ndf["AROONU_14_4h"] = df["AROONU_14_4h"]',
        regime_dependency="适用于长期趋势，需要4h级别趋势明确",
        intuition="4小时级别AROON识别长期趋势强度和方向",
        applicable_scenarios=["长期趋势", "趋势强度", "趋势确认"]
    ))
    
    # STOCHRSI 相关因子
    manager.add_factor(FactorInfo(
        name="STOCHRSIk_14_14_3_3_15m",
        signal_type="Mean Reversion",
        frequency="15m",
        data_source="Informative timeframe",
        calculation='import pandas_ta as pta\nimport pandas as pd\nimport numpy as np\nfrom freqtrade.strategy import merge_informative_pair\n# 在informative_15m_indicators方法中计算:\nstochrsi = pta.stochrsi(info_df["close"])\nif isinstance(stochrsi, pd.DataFrame):\n    info_df["STOCHRSIk_14_14_3_3"] = stochrsi["STOCHRSIk_14_14_3_3"]\nelse:\n    info_df["STOCHRSIk_14_14_3_3"] = np.nan\n# 然后合并到主数据:\ndf = merge_informative_pair(df, info_df, self.timeframe, "15m", ffill=True)\ndf["STOCHRSIk_14_14_3_3_15m"] = df["STOCHRSIk_14_14_3_3_15m"]',
        regime_dependency="适用于震荡市场，STOCHRSIk < 20 表示超卖",
        intuition="随机RSI结合了RSI和随机指标，更敏感地识别超买超卖",
        applicable_scenarios=["震荡市场", "超买超卖", "短期反转"]
    ))
    
    manager.add_factor(FactorInfo(
        name="STOCHRSIk_14_14_3_3_1h",
        signal_type="Mean Reversion",
        frequency="1h",
        data_source="Informative timeframe",
        calculation='import pandas_ta as pta\nimport pandas as pd\nimport numpy as np\nfrom freqtrade.strategy import merge_informative_pair\n# 在informative_1h_indicators方法中计算:\nstochrsi = pta.stochrsi(info_df["close"])\nif isinstance(stochrsi, pd.DataFrame):\n    info_df["STOCHRSIk_14_14_3_3"] = stochrsi["STOCHRSIk_14_14_3_3"]\nelse:\n    info_df["STOCHRSIk_14_14_3_3"] = np.nan\n# 然后合并到主数据:\ndf = merge_informative_pair(df, info_df, self.timeframe, "1h", ffill=True)\ndf["STOCHRSIk_14_14_3_3_1h"] = df["STOCHRSIk_14_14_3_3_1h"]',
        regime_dependency="适用于中期震荡，需要1h级别趋势明确",
        intuition="1小时级别随机RSI识别中期超买超卖区域",
        applicable_scenarios=["中期震荡", "超买超卖", "多时间框架"]
    ))
    
    manager.add_factor(FactorInfo(
        name="STOCHRSIk_14_14_3_3_4h",
        signal_type="Mean Reversion",
        frequency="4h",
        data_source="Informative timeframe",
        calculation='import pandas_ta as pta\nimport pandas as pd\nimport numpy as np\nfrom freqtrade.strategy import merge_informative_pair\n# 在informative_4h_indicators方法中计算:\nstochrsi = pta.stochrsi(info_df["close"])\nif isinstance(stochrsi, pd.DataFrame):\n    info_df["STOCHRSIk_14_14_3_3"] = stochrsi["STOCHRSIk_14_14_3_3"]\nelse:\n    info_df["STOCHRSIk_14_14_3_3"] = np.nan\n# 然后合并到主数据:\ndf = merge_informative_pair(df, info_df, self.timeframe, "4h", ffill=True)\ndf["STOCHRSIk_14_14_3_3_4h"] = df["STOCHRSIk_14_14_3_3_4h"]',
        regime_dependency="适用于长期震荡，需要4h级别趋势明确",
        intuition="4小时级别随机RSI识别长期超买超卖区域",
        applicable_scenarios=["长期震荡", "超买超卖", "趋势反转"]
    ))
    
    # ROC 相关因子
    manager.add_factor(FactorInfo(
        name="ROC_9_1h",
        signal_type="Trend",
        frequency="1h",
        data_source="Informative timeframe",
        calculation='import pandas_ta as pta\nfrom freqtrade.strategy import merge_informative_pair\n# 在informative_1h_indicators方法中计算:\ninfo_df["ROC_9"] = pta.roc(info_df["close"], length=9)\n# 然后合并到主数据:\ndf = merge_informative_pair(df, info_df, self.timeframe, "1h", ffill=True)\ndf["ROC_9_1h"] = df["ROC_9_1h"]',
        regime_dependency="适用于趋势市场，ROC > -10 表示上升趋势",
        intuition="ROC指标衡量价格变化率，用于识别趋势强度和动量",
        applicable_scenarios=["趋势识别", "动量分析", "趋势强度"]
    ))
    
    manager.add_factor(FactorInfo(
        name="ROC_9_4h",
        signal_type="Trend",
        frequency="4h",
        data_source="Informative timeframe",
        calculation='import pandas_ta as pta\nfrom freqtrade.strategy import merge_informative_pair\n# 在informative_4h_indicators方法中计算:\ninfo_df["ROC_9"] = pta.roc(info_df["close"], length=9)\n# 然后合并到主数据:\ndf = merge_informative_pair(df, info_df, self.timeframe, "4h", ffill=True)\ndf["ROC_9_4h"] = df["ROC_9_4h"]',
        regime_dependency="适用于长期趋势，ROC < 80 表示上升趋势减弱",
        intuition="4小时级别ROC识别长期价格变化率和趋势强度",
        applicable_scenarios=["长期趋势", "动量分析", "趋势确认"]
    ))
    
    manager.add_factor(FactorInfo(
        name="ROC_9_1d",
        signal_type="Trend",
        frequency="1d",
        data_source="Informative timeframe",
        calculation='import pandas_ta as pta\nfrom freqtrade.strategy import merge_informative_pair\n# 在informative_1d_indicators方法中计算:\ninfo_df["ROC_9"] = pta.roc(info_df["close"], length=9)\n# 然后合并到主数据:\ndf = merge_informative_pair(df, info_df, self.timeframe, "1d", ffill=True)\ndf["ROC_9_1d"] = df["ROC_9_1d"]',
        regime_dependency="适用于长期趋势，ROC > -15 表示长期上升趋势",
        intuition="日线级别ROC识别长期价格变化率和趋势强度",
        applicable_scenarios=["长期趋势", "趋势确认", "长期动量"]
    ))
    
    # CMF 相关因子
    manager.add_factor(FactorInfo(
        name="CMF_20_15m",
        signal_type="Trend",
        frequency="15m",
        data_source="Informative timeframe",
        calculation='import pandas_ta as pta\nfrom freqtrade.strategy import merge_informative_pair\n# 在informative_15m_indicators方法中计算:\ninfo_df["CMF_20"] = pta.cmf(info_df["high"], info_df["low"], info_df["close"], info_df["volume"], length=20)\n# 然后合并到主数据:\ndf = merge_informative_pair(df, info_df, self.timeframe, "15m", ffill=True)\ndf["CMF_20_15m"] = df["CMF_20_15m"]',
        regime_dependency="适用于趋势市场，CMF > -0.25 表示资金流入",
        intuition="CMF指标结合价格和成交量，识别资金流向和趋势强度",
        applicable_scenarios=["趋势识别", "资金流向", "成交量分析"]
    ))
    
    manager.add_factor(FactorInfo(
        name="CMF_20_1h",
        signal_type="Trend",
        frequency="1h",
        data_source="Informative timeframe",
        calculation='import pandas_ta as pta\nfrom freqtrade.strategy import merge_informative_pair\n# 在informative_1h_indicators方法中计算:\ninfo_df["CMF_20"] = pta.cmf(info_df["high"], info_df["low"], info_df["close"], info_df["volume"], length=20)\n# 然后合并到主数据:\ndf = merge_informative_pair(df, info_df, self.timeframe, "1h", ffill=True)\ndf["CMF_20_1h"] = df["CMF_20_1h"]',
        regime_dependency="适用于中期趋势，CMF > -0.20 表示中期资金流入",
        intuition="1小时级别CMF识别中期资金流向和趋势强度",
        applicable_scenarios=["中期趋势", "资金流向", "趋势确认"]
    ))
    
    manager.add_factor(FactorInfo(
        name="CMF_20_4h",
        signal_type="Trend",
        frequency="4h",
        data_source="Informative timeframe",
        calculation='import pandas_ta as pta\nfrom freqtrade.strategy import merge_informative_pair\n# 在informative_4h_indicators方法中计算:\ninfo_df["CMF_20"] = pta.cmf(info_df["high"], info_df["low"], info_df["close"], info_df["volume"], length=20)\n# 然后合并到主数据:\ndf = merge_informative_pair(df, info_df, self.timeframe, "4h", ffill=True)\ndf["CMF_20_4h"] = df["CMF_20_4h"]',
        regime_dependency="适用于长期趋势，CMF > -0.15 表示长期资金流入",
        intuition="4小时级别CMF识别长期资金流向和趋势强度",
        applicable_scenarios=["长期趋势", "资金流向", "趋势确认"]
    ))
    
    manager.add_factor(FactorInfo(
        name="CMF_20_1d",
        signal_type="Trend",
        frequency="1d",
        data_source="Informative timeframe",
        calculation='import pandas_ta as pta\nfrom freqtrade.strategy import merge_informative_pair\n# 在informative_1d_indicators方法中计算:\ninfo_df["CMF_20"] = pta.cmf(info_df["high"], info_df["low"], info_df["close"], info_df["volume"], length=20)\n# 然后合并到主数据:\ndf = merge_informative_pair(df, info_df, self.timeframe, "1d", ffill=True)\ndf["CMF_20_1d"] = df["CMF_20_1d"]',
        regime_dependency="适用于长期趋势，CMF > -0.20 表示长期资金流入",
        intuition="日线级别CMF识别长期资金流向和趋势强度",
        applicable_scenarios=["长期趋势", "资金流向", "长期确认"]
    ))
    
    # RSI变化率因子 - 捕捉RSI的动量变化
    manager.add_factor(FactorInfo(
        name="RSI_3_change_pct",
        signal_type="Mean Reversion",
        frequency="5m",
        data_source="Base timeframe OHLCV",
        calculation='import pandas_ta as pta\n# 先计算RSI_3\ndf["RSI_3"] = pta.rsi(df["close"], length=3)\n# 计算RSI变化率\ndf["RSI_3_change_pct"] = ((df["RSI_3"] - df["RSI_3"].shift(1)) / df["RSI_3"].shift(1)) * 100.0',
        regime_dependency="适用于短期波动市场，RSI快速变化时",
        intuition="RSI变化率捕捉RSI指标的动量变化速度，当RSI快速上升或下降时，可能预示着价格动量的加速或衰减，有助于识别超买超卖的转折点",
        applicable_scenarios=["短期动量分析", "RSI转折点识别", "快速反转信号"]
    ))
    
    manager.add_factor(FactorInfo(
        name="RSI_14_change_pct",
        signal_type="Mean Reversion",
        frequency="5m",
        data_source="Base timeframe OHLCV",
        calculation='import pandas_ta as pta\n# 先计算RSI_14\ndf["RSI_14"] = pta.rsi(df["close"], length=14)\n# 计算RSI变化率\ndf["RSI_14_change_pct"] = ((df["RSI_14"] - df["RSI_14"].shift(1)) / df["RSI_14"].shift(1)) * 100.0',
        regime_dependency="适用于中期波动市场，需要识别RSI趋势变化",
        intuition="14周期RSI的变化率反映中期动量的变化速度，当RSI变化率突然增大时，可能预示着趋势的加速或反转",
        applicable_scenarios=["中期动量分析", "趋势变化识别", "反转确认"]
    ))
    
    # EMA系列因子 - 指数移动平均，对近期价格更敏感
    manager.add_factor(FactorInfo(
        name="EMA_3",
        signal_type="Trend",
        frequency="5m",
        data_source="Base timeframe OHLCV",
        calculation='import pandas_ta as pta\ndf["EMA_3"] = pta.ema(df["close"], length=3)',
        regime_dependency="适用于短期趋势，需要快速响应价格变化",
        intuition="3周期EMA对价格变化非常敏感，能够快速捕捉短期趋势方向，当价格突破EMA_3时，可能预示着短期趋势的开始",
        applicable_scenarios=["短期趋势跟踪", "快速入场信号", "高频交易"]
    ))
    
    manager.add_factor(FactorInfo(
        name="EMA_9",
        signal_type="Trend",
        frequency="5m",
        data_source="Base timeframe OHLCV",
        calculation='import pandas_ta as pta\ndf["EMA_9"] = pta.ema(df["close"], length=9)',
        regime_dependency="适用于短期趋势，波动率中等",
        intuition="9周期EMA平衡了敏感性和稳定性，常用于短期趋势确认，当价格在EMA_9上方时表示短期上升趋势",
        applicable_scenarios=["短期趋势确认", "趋势过滤", "入场时机选择"]
    ))
    
    manager.add_factor(FactorInfo(
        name="EMA_20",
        signal_type="Trend",
        frequency="5m",
        data_source="Base timeframe OHLCV",
        calculation='import pandas_ta as pta\ndf["EMA_20"] = pta.ema(df["close"], length=20)',
        regime_dependency="适用于有明确趋势的市场（ADX > 25），波动率中等，适合中期趋势跟踪",
        intuition="20周期EMA对近期价格赋予更高权重，能够快速响应趋势变化。当价格在EMA_20上方且EMA_20上升时，表示中期上升趋势确立，捕捉了市场参与者的趋势跟随行为",
        applicable_scenarios=["中期趋势确认", "趋势强度判断", "持仓管理", "趋势跟踪", "移动平均策略"]
    ))
    
    manager.add_factor(FactorInfo(
        name="EMA_50",
        signal_type="Trend",
        frequency="5m",
        data_source="Base timeframe OHLCV",
        calculation='import pandas_ta as pta\ndf["EMA_50"] = pta.ema(df["close"], length=50)',
        regime_dependency="适用于中长期趋势，需要过滤短期噪音",
        intuition="50周期EMA识别中长期趋势方向，当EMA_50上升且价格在其上方时，表示中长期上升趋势，常用于趋势过滤",
        applicable_scenarios=["中长期趋势", "趋势过滤", "大周期确认"]
    ))
    
    manager.add_factor(FactorInfo(
        name="EMA_200",
        signal_type="Trend",
        frequency="5m",
        data_source="Base timeframe OHLCV",
        calculation='import pandas_ta as pta\ndf["EMA_200"] = pta.ema(df["close"], length=200, fillna=0.0)',
        regime_dependency="适用于长期趋势，需要识别大周期方向",
        intuition="200周期EMA是长期趋势的重要参考线，当价格在EMA_200上方时表示长期上升趋势，常用于判断市场整体方向",
        applicable_scenarios=["长期趋势", "市场方向判断", "大周期过滤"]
    ))
    
    manager.add_factor(FactorInfo(
        name="EMA_12",
        signal_type="Trend",
        frequency="5m",
        data_source="Base timeframe OHLCV",
        calculation='import pandas_ta as pta\ndf["EMA_12"] = pta.ema(df["close"], length=12)',
        regime_dependency="适用于短期趋势，需要平衡敏感性和稳定性",
        intuition="12周期EMA常用于短期趋势确认，当价格在EMA_12上方时表示短期上升趋势",
        applicable_scenarios=["短期趋势", "趋势确认", "入场信号"]
    ))
    
    manager.add_factor(FactorInfo(
        name="EMA_16",
        signal_type="Trend",
        frequency="5m",
        data_source="Base timeframe OHLCV",
        calculation='import pandas_ta as pta\ndf["EMA_16"] = pta.ema(df["close"], length=16)',
        regime_dependency="适用于短期趋势，需要稳定的趋势信号",
        intuition="16周期EMA提供短期趋势参考，当价格突破EMA_16时可能预示着短期趋势变化",
        applicable_scenarios=["短期趋势", "趋势确认", "入场时机"]
    ))
    
    manager.add_factor(FactorInfo(
        name="EMA_26",
        signal_type="Trend",
        frequency="5m",
        data_source="Base timeframe OHLCV",
        calculation='import pandas_ta as pta\ndf["EMA_26"] = pta.ema(df["close"], length=26)',
        regime_dependency="适用于中期趋势，需要识别中期趋势方向",
        intuition="26周期EMA识别中期趋势方向，当价格在EMA_26上方时表示中期上升趋势",
        applicable_scenarios=["中期趋势", "趋势确认", "持仓管理"]
    ))
    
    manager.add_factor(FactorInfo(
        name="EMA_100",
        signal_type="Trend",
        frequency="5m",
        data_source="Base timeframe OHLCV",
        calculation='import pandas_ta as pta\ndf["EMA_100"] = pta.ema(df["close"], length=100, fillna=0.0)',
        regime_dependency="适用于长期趋势，需要识别长期趋势方向",
        intuition="100周期EMA识别长期趋势方向，当价格在EMA_100上方时表示长期上升趋势",
        applicable_scenarios=["长期趋势", "趋势过滤", "长期确认"]
    ))
    
    # SMA系列因子 - 简单移动平均，所有价格权重相等
    manager.add_factor(FactorInfo(
        name="SMA_9",
        signal_type="Trend",
        frequency="5m",
        data_source="Base timeframe OHLCV",
        calculation='import pandas_ta as pta\ndf["SMA_9"] = pta.sma(df["close"], length=9)',
        regime_dependency="适用于短期趋势，需要简单稳定的趋势指标",
        intuition="9周期SMA提供简单的短期趋势参考，当价格突破SMA_9时可能预示着短期趋势变化",
        applicable_scenarios=["短期趋势", "简单趋势指标", "入场信号"]
    ))
    
    manager.add_factor(FactorInfo(
        name="SMA_200",
        signal_type="Trend",
        frequency="5m",
        data_source="Base timeframe OHLCV",
        calculation='import pandas_ta as pta\ndf["SMA_200"] = pta.sma(df["close"], length=200)',
        regime_dependency="适用于长期趋势，需要识别大周期方向",
        intuition="200周期SMA是经典的长期趋势指标，当价格在SMA_200上方时表示长期上升趋势，是判断牛熊市的重要参考",
        applicable_scenarios=["长期趋势", "市场方向", "牛熊判断"]
    ))
    
    manager.add_factor(FactorInfo(
        name="SMA_16",
        signal_type="Trend",
        frequency="5m",
        data_source="Base timeframe OHLCV",
        calculation='import pandas_ta as pta\ndf["SMA_16"] = pta.sma(df["close"], length=16)',
        regime_dependency="适用于短期趋势，需要简单稳定的趋势指标",
        intuition="16周期SMA提供简单的短期趋势参考，当价格突破SMA_16时可能预示着短期趋势变化",
        applicable_scenarios=["短期趋势", "简单趋势指标", "入场信号"]
    ))
    
    manager.add_factor(FactorInfo(
        name="SMA_21",
        signal_type="Trend",
        frequency="5m",
        data_source="Base timeframe OHLCV",
        calculation='import pandas_ta as pta\ndf["SMA_21"] = pta.sma(df["close"], length=21)',
        regime_dependency="适用于短期趋势，需要稳定的趋势信号",
        intuition="21周期SMA提供短期趋势参考，当价格在SMA_21上方时表示短期上升趋势",
        applicable_scenarios=["短期趋势", "趋势确认", "入场时机"]
    ))
    
    manager.add_factor(FactorInfo(
        name="SMA_30",
        signal_type="Trend",
        frequency="5m",
        data_source="Base timeframe OHLCV",
        calculation='import pandas_ta as pta\ndf["SMA_30"] = pta.sma(df["close"], length=30)',
        regime_dependency="适用于中期趋势，需要识别中期趋势方向",
        intuition="30周期SMA识别中期趋势方向，当价格在SMA_30上方时表示中期上升趋势",
        applicable_scenarios=["中期趋势", "趋势确认", "持仓管理"]
    ))
    
    # 布林带因子 - 波动率指标
    manager.add_factor(FactorInfo(
        name="BBP_20_2.0",
        signal_type="Mean Reversion",
        frequency="5m",
        data_source="Base timeframe OHLCV",
        calculation='import pandas_ta as pta\nimport pandas as pd\nimport numpy as np\n# 计算布林带\nbbands_20_2 = pta.bbands(df["close"], length=20)\nif isinstance(bbands_20_2, pd.DataFrame):\n    df["BBL_20_2.0"] = bbands_20_2["BBL_20_2.0"]\n    df["BBM_20_2.0"] = bbands_20_2["BBM_20_2.0"]\n    df["BBU_20_2.0"] = bbands_20_2["BBU_20_2.0"]\n    df["BBB_20_2.0"] = bbands_20_2["BBB_20_2.0"]\n    df["BBP_20_2.0"] = bbands_20_2["BBP_20_2.0"]\nelse:\n    df["BBP_20_2.0"] = np.nan',
        regime_dependency="适用于震荡市场（无明显趋势），当BBP < 0.2时表示超卖，BBP > 0.8时表示超买",
        intuition="布林带位置指标（%B）衡量价格在布林带中的相对位置。当BBP接近0时表示价格接近下轨（超卖），接近1时表示价格接近上轨（超买）。这捕捉了价格偏离统计均值的程度，反映了市场参与者的过度反应，价格倾向于回归均值",
        applicable_scenarios=["震荡市场", "超买超卖", "均值回归", "布林带策略", "区间交易", "统计套利"]
    ))
    
    manager.add_factor(FactorInfo(
        name="BBB_20_2.0",
        signal_type="Volatility",
        frequency="5m",
        data_source="Base timeframe OHLCV",
        calculation='import pandas_ta as pta\nimport pandas as pd\nimport numpy as np\n# 计算布林带\nbbands_20_2 = pta.bbands(df["close"], length=20)\nif isinstance(bbands_20_2, pd.DataFrame):\n    df["BBB_20_2.0"] = bbands_20_2["BBB_20_2.0"]\nelse:\n    df["BBB_20_2.0"] = np.nan',
        regime_dependency="适用于波动率分析，BBB增大表示波动率上升",
        intuition="布林带带宽指标衡量布林带的宽度，反映市场波动率水平，当BBB增大时表示波动率上升，可能预示着趋势的开始或加速",
        applicable_scenarios=["波动率分析", "趋势开始识别", "市场状态判断"]
    ))
    
    manager.add_factor(FactorInfo(
        name="BBP_40_2.0",
        signal_type="Mean Reversion",
        frequency="5m",
        data_source="Base timeframe OHLCV",
        calculation='import talib.abstract as ta\nimport numpy as np\n# 使用talib计算40周期布林带\nupper, middle, lower = ta.BBANDS(df["close"], timeperiod=40, nbdevup=2.0, nbdevdn=2.0, matype=0)\ndf["BBL_40_2.0"] = lower\ndf["BBM_40_2.0"] = middle\ndf["BBU_40_2.0"] = upper\ndf["BBP_40_2.0"] = (df["close"] - lower) / (upper - lower)',
        regime_dependency="适用于中期震荡市场，需要更稳定的超买超卖信号",
        intuition="40周期布林带位置指标提供更稳定的超买超卖信号，减少了短期噪音的影响，适合中期均值回归策略",
        applicable_scenarios=["中期震荡", "稳定超买超卖", "中期均值回归"]
    ))
    
    manager.add_factor(FactorInfo(
        name="BBL_20_2.0",
        signal_type="Mean Reversion",
        frequency="5m",
        data_source="Base timeframe OHLCV",
        calculation='import pandas_ta as pta\nimport pandas as pd\nimport numpy as np\n# 计算布林带\nbbands_20_2 = pta.bbands(df["close"], length=20)\nif isinstance(bbands_20_2, pd.DataFrame):\n    df["BBL_20_2.0"] = bbands_20_2["BBL_20_2.0"]\nelse:\n    df["BBL_20_2.0"] = np.nan',
        regime_dependency="适用于震荡市场，当价格接近BBL时表示超卖",
        intuition="布林带下轨识别超卖区域，当价格接近或跌破BBL时表示价格处于相对低位，可能出现反弹",
        applicable_scenarios=["震荡市场", "超卖识别", "均值回归"]
    ))
    
    manager.add_factor(FactorInfo(
        name="BBU_20_2.0",
        signal_type="Mean Reversion",
        frequency="5m",
        data_source="Base timeframe OHLCV",
        calculation='import pandas_ta as pta\nimport pandas as pd\nimport numpy as np\n# 计算布林带\nbbands_20_2 = pta.bbands(df["close"], length=20)\nif isinstance(bbands_20_2, pd.DataFrame):\n    df["BBU_20_2.0"] = bbands_20_2["BBU_20_2.0"]\nelse:\n    df["BBU_20_2.0"] = np.nan',
        regime_dependency="适用于震荡市场，当价格接近BBU时表示超买",
        intuition="布林带上轨识别超买区域，当价格接近或突破BBU时表示价格处于相对高位，可能出现回调",
        applicable_scenarios=["震荡市场", "超买识别", "均值回归"]
    ))
    
    manager.add_factor(FactorInfo(
        name="BBM_20_2.0",
        signal_type="Trend",
        frequency="5m",
        data_source="Base timeframe OHLCV",
        calculation='import pandas_ta as pta\nimport pandas as pd\nimport numpy as np\n# 计算布林带\nbbands_20_2 = pta.bbands(df["close"], length=20)\nif isinstance(bbands_20_2, pd.DataFrame):\n    df["BBM_20_2.0"] = bbands_20_2["BBM_20_2.0"]\nelse:\n    df["BBM_20_2.0"] = np.nan',
        regime_dependency="适用于趋势市场，BBM作为中轨提供趋势参考",
        intuition="布林带中轨是20周期移动平均，当价格在BBM上方时表示上升趋势，下方时表示下降趋势",
        applicable_scenarios=["趋势识别", "趋势确认", "移动平均"]
    ))
    
    manager.add_factor(FactorInfo(
        name="BBB_40_2.0",
        signal_type="Volatility",
        frequency="5m",
        data_source="Base timeframe OHLCV",
        calculation='import talib.abstract as ta\nimport numpy as np\n# 使用talib计算40周期布林带\nupper, middle, lower = ta.BBANDS(df["close"], timeperiod=40, nbdevup=2.0, nbdevdn=2.0, matype=0)\ndf["BBB_40_2.0"] = (upper - lower) / middle * 100.0',
        regime_dependency="适用于波动率分析，BBB增大表示波动率上升",
        intuition="40周期布林带带宽指标衡量布林带的宽度，反映市场波动率水平，当BBB增大时表示波动率上升",
        applicable_scenarios=["波动率分析", "趋势开始识别", "市场状态判断"]
    ))
    
    manager.add_factor(FactorInfo(
        name="BBD_40_2.0",
        signal_type="Volatility",
        frequency="5m",
        data_source="Base timeframe OHLCV",
        calculation='import talib.abstract as ta\nimport numpy as np\n# 使用talib计算40周期布林带\nupper, middle, lower = ta.BBANDS(df["close"], timeperiod=40, nbdevup=2.0, nbdevdn=2.0, matype=0)\ndf["BBM_40_2.0"] = middle\ndf["BBL_40_2.0"] = lower\ndf["BBD_40_2.0"] = (df["BBM_40_2.0"] - df["BBL_40_2.0"]).abs()',
        regime_dependency="适用于波动率分析，BBD反映布林带下轨到中轨的距离",
        intuition="布林带下轨到中轨的距离反映市场波动幅度，当BBD增大时表示波动增大",
        applicable_scenarios=["波动率分析", "波动幅度", "市场状态"]
    ))
    
    manager.add_factor(FactorInfo(
        name="BBT_40_2.0",
        signal_type="Mean Reversion",
        frequency="5m",
        data_source="Base timeframe OHLCV",
        calculation='import talib.abstract as ta\nimport numpy as np\n# 使用talib计算40周期布林带\nupper, middle, lower = ta.BBANDS(df["close"], timeperiod=40, nbdevup=2.0, nbdevdn=2.0, matype=0)\ndf["BBL_40_2.0"] = lower\ndf["BBT_40_2.0"] = (df["close"] - df["BBL_40_2.0"]).abs()',
        regime_dependency="适用于震荡市场，BBT反映价格距离下轨的距离",
        intuition="价格距离布林带下轨的距离，当BBT较小时表示价格接近下轨（超卖），可能反弹",
        applicable_scenarios=["震荡市场", "超卖识别", "反弹信号"]
    ))
    
    # MFI因子 - 资金流量指标
    manager.add_factor(FactorInfo(
        name="MFI_14",
        signal_type="Trend",
        frequency="5m",
        data_source="Base timeframe OHLCV",
        calculation='import pandas_ta as pta\ndf["MFI_14"] = pta.mfi(df["high"], df["low"], df["close"], df["volume"], length=14)',
        regime_dependency="适用于趋势市场，MFI > 80表示超买，MFI < 20表示超卖",
        intuition="MFI结合价格和成交量，识别资金流入流出，当MFI处于极端值时，可能预示着价格反转，因为资金流入或流出已经达到极限",
        applicable_scenarios=["资金流向", "超买超卖", "成交量确认"]
    ))
    
    # WILLR因子 - 威廉指标
    manager.add_factor(FactorInfo(
        name="WILLR_14",
        signal_type="Mean Reversion",
        frequency="5m",
        data_source="Base timeframe OHLCV",
        calculation='import pandas_ta as pta\ndf["WILLR_14"] = pta.willr(df["high"], df["low"], df["close"], length=14)',
        regime_dependency="适用于震荡市场，WILLR < -80表示超卖，WILLR > -20表示超买",
        intuition="威廉指标衡量价格在最近14周期内的相对位置，当WILLR接近-100时表示价格接近周期最低点（超卖），接近0时表示价格接近周期最高点（超买）",
        applicable_scenarios=["震荡市场", "超买超卖", "短期反转"]
    ))
    
    manager.add_factor(FactorInfo(
        name="WILLR_480",
        signal_type="Mean Reversion",
        frequency="5m",
        data_source="Base timeframe OHLCV",
        calculation='import pandas_ta as pta\ndf["WILLR_480"] = pta.willr(df["high"], df["low"], df["close"], length=480)',
        regime_dependency="适用于长期震荡，需要识别长期超买超卖区域",
        intuition="480周期威廉指标提供长期超买超卖参考，当WILLR_480处于极端值时，表示价格在长期周期内处于极端位置，可能预示着长期反转",
        applicable_scenarios=["长期震荡", "长期超买超卖", "长期反转"]
    ))
    
    # AROOND因子 - 下降趋势强度
    manager.add_factor(FactorInfo(
        name="AROOND_14",
        signal_type="Trend",
        frequency="5m",
        data_source="Base timeframe OHLCV",
        calculation='import pandas_ta as pta\nimport pandas as pd\nimport numpy as np\n# 计算AROON指标\naroon_14 = pta.aroon(df["high"], df["low"], length=14)\nif isinstance(aroon_14, pd.DataFrame):\n    df["AROOND_14"] = aroon_14["AROOND_14"]\nelse:\n    df["AROOND_14"] = np.nan',
        regime_dependency="适用于趋势市场，AROOND < 50表示下降趋势减弱",
        intuition="AROON下降指标衡量下降趋势的强度，当AROOND较低时表示下降趋势减弱，可能预示着下降趋势的结束或反转",
        applicable_scenarios=["下降趋势", "趋势强度", "反转识别"]
    ))
    
    # STOCHRSId因子 - 随机RSI信号线
    manager.add_factor(FactorInfo(
        name="STOCHRSId_14_14_3_3",
        signal_type="Mean Reversion",
        frequency="5m",
        data_source="Base timeframe OHLCV",
        calculation='import pandas_ta as pta\nimport pandas as pd\nimport numpy as np\n# 计算随机RSI\nstochrsi = pta.stochrsi(df["close"])\nif isinstance(stochrsi, pd.DataFrame):\n    df["STOCHRSIk_14_14_3_3"] = stochrsi["STOCHRSIk_14_14_3_3"]\n    df["STOCHRSId_14_14_3_3"] = stochrsi["STOCHRSId_14_14_3_3"]\nelse:\n    df["STOCHRSId_14_14_3_3"] = np.nan',
        regime_dependency="适用于震荡市场，STOCHRSId与STOCHRSIk的金叉死叉提供交易信号",
        intuition="随机RSI信号线是随机RSI的平滑版本，当STOCHRSIk上穿STOCHRSId时表示超卖反弹，下穿时表示超买回调",
        applicable_scenarios=["震荡市场", "超买超卖", "交叉信号"]
    ))
    
    # KST因子 - 知识统计指标
    manager.add_factor(FactorInfo(
        name="KST_10_15_20_30_10_10_10_15",
        signal_type="Trend",
        frequency="5m",
        data_source="Base timeframe OHLCV",
        calculation='import pandas_ta as pta\nimport pandas as pd\nimport numpy as np\n# 计算KST指标\nkst = pta.kst(df["close"])\nif isinstance(kst, pd.DataFrame):\n    df["KST_10_15_20_30_10_10_10_15"] = kst["KST_10_15_20_30_10_10_10_15"]\n    df["KSTs_9"] = kst["KSTs_9"]\nelse:\n    df["KST_10_15_20_30_10_10_10_15"] = np.nan',
        regime_dependency="适用于趋势市场，KST > 0表示上升趋势，KST < 0表示下降趋势",
        intuition="KST指标结合多个周期的ROC，提供综合的趋势强度信号，当KST上升且为正时表示上升趋势加强，下降且为负时表示下降趋势加强",
        applicable_scenarios=["趋势识别", "趋势强度", "综合趋势信号"]
    ))
    
    manager.add_factor(FactorInfo(
        name="KSTs_9",
        signal_type="Trend",
        frequency="5m",
        data_source="Base timeframe OHLCV",
        calculation='import pandas_ta as pta\nimport pandas as pd\nimport numpy as np\n# 计算KST指标\nkst = pta.kst(df["close"])\nif isinstance(kst, pd.DataFrame):\n    df["KSTs_9"] = kst["KSTs_9"]\nelse:\n    df["KSTs_9"] = np.nan',
        regime_dependency="适用于趋势市场，KST与KSTs的金叉死叉提供趋势变化信号",
        intuition="KST信号线是KST的平滑版本，当KST上穿KSTs时表示趋势转强，下穿时表示趋势转弱",
        applicable_scenarios=["趋势变化", "趋势确认", "交叉信号"]
    ))
    
    # OBV因子 - 能量潮
    manager.add_factor(FactorInfo(
        name="OBV",
        signal_type="Trend",
        frequency="5m",
        data_source="Base timeframe OHLCV",
        calculation='import pandas_ta as pta\ndf["OBV"] = pta.obv(df["close"], df["volume"])',
        regime_dependency="适用于趋势市场，OBV上升表示资金流入，OBV下降表示资金流出",
        intuition="OBV通过累加成交量来反映资金流向，当OBV上升时表示资金流入（上涨时成交量大于下跌时），下降时表示资金流出，可用于确认价格趋势",
        applicable_scenarios=["资金流向", "趋势确认", "成交量分析"]
    ))
    
    manager.add_factor(FactorInfo(
        name="OBV_change_pct",
        signal_type="Trend",
        frequency="5m",
        data_source="Base timeframe OHLCV",
        calculation='import pandas_ta as pta\n# 先计算OBV\ndf["OBV"] = pta.obv(df["close"], df["volume"])\n# 计算OBV变化率\ndf["OBV_change_pct"] = ((df["OBV"] - df["OBV"].shift(1)) / abs(df["OBV"].shift(1))) * 100.0',
        regime_dependency="适用于趋势市场，OBV变化率反映资金流入流出的速度",
        intuition="OBV变化率捕捉资金流向的变化速度，当OBV_change_pct突然增大时，可能预示着资金流入加速，趋势可能加强",
        applicable_scenarios=["资金流向速度", "趋势加速", "动量分析"]
    ))
    
    # ROC_2因子 - 2周期变化率
    manager.add_factor(FactorInfo(
        name="ROC_2",
        signal_type="Trend",
        frequency="5m",
        data_source="Base timeframe OHLCV",
        calculation='import pandas_ta as pta\ndf["ROC_2"] = pta.roc(df["close"], length=2)',
        regime_dependency="适用于短期动量，需要快速捕捉价格变化",
        intuition="2周期ROC捕捉极短期的价格变化率，对价格变化非常敏感，可用于识别短期动量的快速变化",
        applicable_scenarios=["短期动量", "快速变化", "高频信号"]
    ))
    
    manager.add_factor(FactorInfo(
        name="ROC_9",
        signal_type="Trend",
        frequency="5m",
        data_source="Base timeframe OHLCV",
        calculation='import pandas_ta as pta\ndf["ROC_9"] = pta.roc(df["close"], length=9)',
        regime_dependency="适用于中期动量，需要识别价格变化率",
        intuition="9周期ROC识别中期价格变化率，当ROC_9为正时表示上升趋势，为负时表示下降趋势",
        applicable_scenarios=["中期动量", "趋势识别", "动量分析"]
    ))
    
    # change_pct因子 - 蜡烛变化率
    manager.add_factor(FactorInfo(
        name="change_pct",
        signal_type="Trend",
        frequency="5m",
        data_source="Base timeframe OHLCV",
        calculation='df["change_pct"] = (df["close"] - df["open"]) / df["open"] * 100.0',
        regime_dependency="适用于所有市场状态，反映单根蜡烛的涨跌幅度",
        intuition="蜡烛变化率衡量单根K线的涨跌幅度，当change_pct较大时表示该K线涨幅或跌幅较大，可能预示着短期动量的强弱",
        applicable_scenarios=["K线分析", "短期动量", "涨跌幅度"]
    ))
    
    # close_delta因子 - 收盘价变化
    manager.add_factor(FactorInfo(
        name="close_delta",
        signal_type="Trend",
        frequency="5m",
        data_source="Base timeframe OHLCV",
        calculation='import numpy as np\ndf["close_delta"] = (df["close"] - df["close"].shift()).abs()',
        regime_dependency="适用于波动率分析，close_delta增大表示价格波动增大",
        intuition="收盘价变化绝对值反映价格的波动幅度，当close_delta增大时表示价格波动增大，可能预示着趋势的开始或加速",
        applicable_scenarios=["波动率分析", "价格波动", "趋势开始"]
    ))
    
    # close_max/min因子 - 最高/最低价
    manager.add_factor(FactorInfo(
        name="close_max_12",
        signal_type="Trend",
        frequency="5m",
        data_source="Base timeframe OHLCV",
        calculation='df["close_max_12"] = df["close"].rolling(12).max()',
        regime_dependency="适用于趋势市场，当价格接近close_max时表示接近短期高点",
        intuition="12周期最高价识别短期阻力位，当价格接近close_max_12时可能遇到阻力，当价格突破close_max_12时可能预示着上升趋势的延续",
        applicable_scenarios=["阻力位识别", "突破交易", "趋势延续"]
    ))
    
    manager.add_factor(FactorInfo(
        name="close_min_12",
        signal_type="Trend",
        frequency="5m",
        data_source="Base timeframe OHLCV",
        calculation='df["close_min_12"] = df["close"].rolling(12).min()',
        regime_dependency="适用于趋势市场，当价格接近close_min时表示接近短期低点",
        intuition="12周期最低价识别短期支撑位，当价格接近close_min_12时可能遇到支撑，当价格跌破close_min_12时可能预示着下降趋势的延续",
        applicable_scenarios=["支撑位识别", "跌破交易", "趋势延续"]
    ))
    
    manager.add_factor(FactorInfo(
        name="close_max_6",
        signal_type="Trend",
        frequency="5m",
        data_source="Base timeframe OHLCV",
        calculation='df["close_max_6"] = df["close"].rolling(6).max()',
        regime_dependency="适用于短期趋势，当价格接近close_max_6时表示接近极短期高点",
        intuition="6周期最高价识别极短期阻力位，当价格接近close_max_6时可能遇到阻力",
        applicable_scenarios=["极短期阻力", "突破交易", "短期趋势"]
    ))
    
    manager.add_factor(FactorInfo(
        name="close_max_48",
        signal_type="Trend",
        frequency="5m",
        data_source="Base timeframe OHLCV",
        calculation='df["close_max_48"] = df["close"].rolling(48).max()',
        regime_dependency="适用于中期趋势，当价格接近close_max_48时表示接近中期高点",
        intuition="48周期最高价识别中期阻力位，当价格接近close_max_48时可能遇到阻力，当价格突破close_max_48时可能预示着上升趋势的延续",
        applicable_scenarios=["中期阻力", "突破交易", "趋势延续"]
    ))
    
    manager.add_factor(FactorInfo(
        name="close_min_6",
        signal_type="Trend",
        frequency="5m",
        data_source="Base timeframe OHLCV",
        calculation='df["close_min_6"] = df["close"].rolling(6).min()',
        regime_dependency="适用于短期趋势，当价格接近close_min_6时表示接近极短期低点",
        intuition="6周期最低价识别极短期支撑位，当价格接近close_min_6时可能遇到支撑",
        applicable_scenarios=["极短期支撑", "跌破交易", "短期趋势"]
    ))
    
    manager.add_factor(FactorInfo(
        name="close_min_48",
        signal_type="Trend",
        frequency="5m",
        data_source="Base timeframe OHLCV",
        calculation='df["close_min_48"] = df["close"].rolling(48).min()',
        regime_dependency="适用于中期趋势，当价格接近close_min_48时表示接近中期低点",
        intuition="48周期最低价识别中期支撑位，当价格接近close_min_48时可能遇到支撑，当价格跌破close_min_48时可能预示着下降趋势的延续",
        applicable_scenarios=["中期支撑", "跌破交易", "趋势延续"]
    ))
    
    manager.add_factor(FactorInfo(
        name="num_empty_288",
        signal_type="Risk-off",
        frequency="5m",
        data_source="Base timeframe OHLCV",
        calculation='df["num_empty_288"] = (df["volume"] <= 0).rolling(window=288, min_periods=288).sum()',
        regime_dependency="适用于数据质量检查，num_empty_288 > 0表示存在空蜡烛",
        intuition="288周期内空蜡烛数量，用于识别数据质量问题，当num_empty_288较大时表示数据不完整，应避免交易",
        applicable_scenarios=["数据质量", "风险控制", "数据验证"]
    ))
    
    # 保护因子
    manager.add_factor(FactorInfo(
        name="protections_long_global",
        signal_type="Risk-off",
        frequency="5m",
        data_source="Multiple timeframes combined",
        calculation='# 全局保护因子 - 多时间框架组合\n# 需要先计算所有相关时间框架的指标\n# 示例：综合5m、15m、1h、4h、1d的RSI、CCI、AROON、STOCHRSI\ndf["protections_long_global"] = (\n    # 第一层条件：多个时间框架显示下跌\n    ((df["RSI_3"] > 1.0) | (df["RSI_3_15m"] > 15.0) | (df["RSI_3_1h"] > 20.0) |\n     (df["RSI_3_4h"] > 20.0) | (df["RSI_3_1d"] > 20.0) |\n     (df["RSI_14_1h"] < 30.0) | (df["RSI_14_4h"] < 30.0) |\n     (df["RSI_14_1d"] < 30.0) | (df["CCI_20_1h"] < -250.0) |\n     (df["CCI_20_4h"] < -200.0))\n    # 第二层条件：进一步确认不利条件\n    & ((df["RSI_3"] > 1.0) | (df["RSI_3_4h"] > 10.0) | (df["RSI_3_1d"] > 35.0) |\n       (df["RSI_14_15m"] < 30.0) | (df["RSI_14_1h"] < 30.0) |\n       (df["RSI_14_4h"] < 30.0) | (df["STOCHRSIk_14_14_3_3_15m"] < 20.0) |\n       (df["STOCHRSIk_14_14_3_3_1d"] < 50.0))\n    # 可以继续添加更多层条件...\n)',
        regime_dependency="适用于所有市场状态，用于风险控制",
        intuition="全局保护因子通过多时间框架指标组合，识别不利的市场条件，避免在不利环境下开仓。该因子综合了5m、15m、1h、4h、1d多个时间框架的RSI、CCI、AROON、STOCHRSI等指标，当多个时间框架都显示不利条件时，触发保护机制",
        applicable_scenarios=["风险控制", "市场保护", "全局过滤", "多时间框架确认"]
    ))
    
    print(f"已初始化 {len(manager.get_all_factors())} 个因子")
    
    # 生成总览文档
    summary = manager.generate_summary_doc()
    summary_file = manager.library_dir.parent / "FACTOR_LIBRARY_SUMMARY.md"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(summary)
    print(f"因子总览文档已保存到: {summary_file}")
    
    return manager

if __name__ == "__main__":
    init_common_factors()

