# 量化因子库总览

总计因子数量: 67


## Mean Reversion 类型因子 (21个)

### BBL_20_2.0

- **频率**: 5m

- **数据来源**: Base timeframe OHLCV

- **直觉**: 布林带下轨识别超卖区域，当价格接近或跌破BBL时表示价格处于相对低位，可能出现反弹

- **适用场景**: 震荡市场, 超卖识别, 均值回归

- **生效条件**: 适用于震荡市场，当价格接近BBL时表示超卖

- **计算方式**: `import pandas_ta as pta
import pandas as pd
import numpy as np
# 计算布林带
bbands_20_2 = pta.bbands(df["...`


### BBP_20_2.0

- **频率**: 5m

- **数据来源**: Base timeframe OHLCV

- **直觉**: 布林带位置指标（%B）衡量价格在布林带中的相对位置。当BBP接近0时表示价格接近下轨（超卖），接近1时表示价格接近上轨（超买）。这捕捉了价格偏离统计均值的程度，反映了市场参与者的过度反应，价格倾向于回归均值

- **适用场景**: 震荡市场, 超买超卖, 均值回归, 布林带策略, 区间交易, 统计套利

- **生效条件**: 适用于震荡市场（无明显趋势），当BBP < 0.2时表示超卖，BBP > 0.8时表示超买

- **计算方式**: `import pandas_ta as pta
import pandas as pd
import numpy as np
# 计算布林带
bbands_20_2 = pta.bbands(df["...`


### BBP_40_2.0

- **频率**: 5m

- **数据来源**: Base timeframe OHLCV

- **直觉**: 40周期布林带位置指标提供更稳定的超买超卖信号，减少了短期噪音的影响，适合中期均值回归策略

- **适用场景**: 中期震荡, 稳定超买超卖, 中期均值回归

- **生效条件**: 适用于中期震荡市场，需要更稳定的超买超卖信号

- **计算方式**: `import talib.abstract as ta
import numpy as np
# 使用talib计算40周期布林带
upper, middle, lower = ta.BBANDS(d...`


### BBT_40_2.0

- **频率**: 5m

- **数据来源**: Base timeframe OHLCV

- **直觉**: 价格距离布林带下轨的距离，当BBT较小时表示价格接近下轨（超卖），可能反弹

- **适用场景**: 震荡市场, 超卖识别, 反弹信号

- **生效条件**: 适用于震荡市场，BBT反映价格距离下轨的距离

- **计算方式**: `import talib.abstract as ta
import numpy as np
# 使用talib计算40周期布林带
upper, middle, lower = ta.BBANDS(d...`


### BBU_20_2.0

- **频率**: 5m

- **数据来源**: Base timeframe OHLCV

- **直觉**: 布林带上轨识别超买区域，当价格接近或突破BBU时表示价格处于相对高位，可能出现回调

- **适用场景**: 震荡市场, 超买识别, 均值回归

- **生效条件**: 适用于震荡市场，当价格接近BBU时表示超买

- **计算方式**: `import pandas_ta as pta
import pandas as pd
import numpy as np
# 计算布林带
bbands_20_2 = pta.bbands(df["...`


### CCI_20_1h

- **频率**: 1h

- **数据来源**: Informative timeframe

- **直觉**: 当CCI处于极端值时，市场存在明显的单边拥挤，价格容易出现反向波动

- **适用场景**: 趋势市场, 极端值识别, 反转交易

- **生效条件**: 适用于趋势市场，CCI < -250 表示极度超卖

- **计算方式**: `import pandas_ta as pta
from freqtrade.strategy import merge_informative_pair
# 在informative_1h_indi...`


### CCI_20_4h

- **频率**: 4h

- **数据来源**: Informative timeframe

- **直觉**: 4小时级别CCI识别长期超买超卖，用于中期反转判断

- **适用场景**: 长期趋势, 中期反转, 趋势确认

- **生效条件**: 适用于长期趋势，CCI < -200 表示中期超卖

- **计算方式**: `import pandas_ta as pta
from freqtrade.strategy import merge_informative_pair
# 在informative_4h_indi...`


### RSI_14

- **频率**: 5m

- **数据来源**: Base timeframe OHLCV

- **直觉**: 当RSI处于极端值（>70超买，<30超卖）时，市场存在单边拥挤，价格容易出现均值回归。这捕捉了市场参与者的过度反应行为

- **适用场景**: 震荡市场, 超买超卖识别, 反转交易, 区间交易, RSI策略

- **生效条件**: 适用于震荡市场（ADX < 25），波动率中等，无明显趋势时

- **计算方式**: `import pandas_ta as pta
df["RSI_14"] = pta.rsi(df["close"], length=14)...`


### RSI_14_1h

- **频率**: 1h

- **数据来源**: Informative timeframe

- **直觉**: 1小时级别的RSI用于过滤短期噪音，识别中期超买超卖区域

- **适用场景**: 中期趋势确认, 多时间框架分析, 趋势过滤

- **生效条件**: 适用于中期趋势确认，1h级别趋势明确

- **计算方式**: `import pandas_ta as pta
from freqtrade.strategy import merge_informative_pair
# 在informative_1h_indi...`


### RSI_14_4h

- **频率**: 4h

- **数据来源**: Informative timeframe

- **直觉**: 4小时级别RSI识别长期超买超卖区域，用于趋势反转判断

- **适用场景**: 长期趋势, 趋势反转, 多时间框架确认

- **生效条件**: 适用于长期趋势，4h级别趋势明确，波动率较低

- **计算方式**: `import pandas_ta as pta
from freqtrade.strategy import merge_informative_pair
# 在informative_4h_indi...`


### RSI_14_change_pct

- **频率**: 5m

- **数据来源**: Base timeframe OHLCV

- **直觉**: 14周期RSI的变化率反映中期动量的变化速度，当RSI变化率突然增大时，可能预示着趋势的加速或反转

- **适用场景**: 中期动量分析, 趋势变化识别, 反转确认

- **生效条件**: 适用于中期波动市场，需要识别RSI趋势变化

- **计算方式**: `import pandas_ta as pta
# 先计算RSI_14
df["RSI_14"] = pta.rsi(df["close"], length=14)
# 计算RSI变化率
df["RS...`


### RSI_20

- **频率**: 5m

- **数据来源**: Base timeframe OHLCV

- **直觉**: 20周期RSI提供更稳定的超买超卖信号，减少了短期噪音的影响

- **适用场景**: 中期震荡, 稳定超买超卖, 趋势过滤

- **生效条件**: 适用于中期震荡市场，需要更稳定的超买超卖信号

- **计算方式**: `import pandas_ta as pta
df["RSI_20"] = pta.rsi(df["close"], length=20)...`


### RSI_3

- **频率**: 5m

- **数据来源**: Base timeframe OHLCV

- **直觉**: 3周期RSI对价格变化极其敏感，能够快速捕捉短期动量的变化。当RSI_3处于极端值时，反映了市场短期的过度反应，价格容易出现快速反转

- **适用场景**: 短期交易, 快速反转, 高频策略, 5分钟级别交易, 快速动量捕捉

- **生效条件**: 适用于短期波动市场，需要快速响应价格变化，适合5分钟级别的快速交易

- **计算方式**: `import pandas_ta as pta
df["RSI_3"] = pta.rsi(df["close"], length=3)...`


### RSI_3_change_pct

- **频率**: 5m

- **数据来源**: Base timeframe OHLCV

- **直觉**: RSI变化率捕捉RSI指标的动量变化速度，当RSI快速上升或下降时，可能预示着价格动量的加速或衰减，有助于识别超买超卖的转折点

- **适用场景**: 短期动量分析, RSI转折点识别, 快速反转信号

- **生效条件**: 适用于短期波动市场，RSI快速变化时

- **计算方式**: `import pandas_ta as pta
# 先计算RSI_3
df["RSI_3"] = pta.rsi(df["close"], length=3)
# 计算RSI变化率
df["RSI_3...`


### RSI_4

- **频率**: 5m

- **数据来源**: Base timeframe OHLCV

- **直觉**: 4周期RSI提供短期动量参考，比RSI_3更稳定，比RSI_14更敏感

- **适用场景**: 短期交易, 动量分析, 超买超卖

- **生效条件**: 适用于短期波动，介于RSI_3和RSI_14之间

- **计算方式**: `import pandas_ta as pta
df["RSI_4"] = pta.rsi(df["close"], length=4)...`


### STOCHRSId_14_14_3_3

- **频率**: 5m

- **数据来源**: Base timeframe OHLCV

- **直觉**: 随机RSI信号线是随机RSI的平滑版本，当STOCHRSIk上穿STOCHRSId时表示超卖反弹，下穿时表示超买回调

- **适用场景**: 震荡市场, 超买超卖, 交叉信号

- **生效条件**: 适用于震荡市场，STOCHRSId与STOCHRSIk的金叉死叉提供交易信号

- **计算方式**: `import pandas_ta as pta
import pandas as pd
import numpy as np
# 计算随机RSI
stochrsi = pta.stochrsi(df[...`


### STOCHRSIk_14_14_3_3_15m

- **频率**: 15m

- **数据来源**: Informative timeframe

- **直觉**: 随机RSI结合了RSI和随机指标，更敏感地识别超买超卖

- **适用场景**: 震荡市场, 超买超卖, 短期反转

- **生效条件**: 适用于震荡市场，STOCHRSIk < 20 表示超卖

- **计算方式**: `import pandas_ta as pta
import pandas as pd
import numpy as np
from freqtrade.strategy import merge_...`


### STOCHRSIk_14_14_3_3_1h

- **频率**: 1h

- **数据来源**: Informative timeframe

- **直觉**: 1小时级别随机RSI识别中期超买超卖区域

- **适用场景**: 中期震荡, 超买超卖, 多时间框架

- **生效条件**: 适用于中期震荡，需要1h级别趋势明确

- **计算方式**: `import pandas_ta as pta
import pandas as pd
import numpy as np
from freqtrade.strategy import merge_...`


### STOCHRSIk_14_14_3_3_4h

- **频率**: 4h

- **数据来源**: Informative timeframe

- **直觉**: 4小时级别随机RSI识别长期超买超卖区域

- **适用场景**: 长期震荡, 超买超卖, 趋势反转

- **生效条件**: 适用于长期震荡，需要4h级别趋势明确

- **计算方式**: `import pandas_ta as pta
import pandas as pd
import numpy as np
from freqtrade.strategy import merge_...`


### WILLR_14

- **频率**: 5m

- **数据来源**: Base timeframe OHLCV

- **直觉**: 威廉指标衡量价格在最近14周期内的相对位置，当WILLR接近-100时表示价格接近周期最低点（超卖），接近0时表示价格接近周期最高点（超买）

- **适用场景**: 震荡市场, 超买超卖, 短期反转

- **生效条件**: 适用于震荡市场，WILLR < -80表示超卖，WILLR > -20表示超买

- **计算方式**: `import pandas_ta as pta
df["WILLR_14"] = pta.willr(df["high"], df["low"], df["close"], length=14)...`


### WILLR_480

- **频率**: 5m

- **数据来源**: Base timeframe OHLCV

- **直觉**: 480周期威廉指标提供长期超买超卖参考，当WILLR_480处于极端值时，表示价格在长期周期内处于极端位置，可能预示着长期反转

- **适用场景**: 长期震荡, 长期超买超卖, 长期反转

- **生效条件**: 适用于长期震荡，需要识别长期超买超卖区域

- **计算方式**: `import pandas_ta as pta
df["WILLR_480"] = pta.willr(df["high"], df["low"], df["close"], length=480)...`


## Risk-off 类型因子 (2个)

### num_empty_288

- **频率**: 5m

- **数据来源**: Base timeframe OHLCV

- **直觉**: 288周期内空蜡烛数量，用于识别数据质量问题，当num_empty_288较大时表示数据不完整，应避免交易

- **适用场景**: 数据质量, 风险控制, 数据验证

- **生效条件**: 适用于数据质量检查，num_empty_288 > 0表示存在空蜡烛

- **计算方式**: `df["num_empty_288"] = (df["volume"] <= 0).rolling(window=288, min_periods=288).sum()...`


### protections_long_global

- **频率**: 5m

- **数据来源**: Multiple timeframes combined

- **直觉**: 全局保护因子通过多时间框架指标组合，识别不利的市场条件，避免在不利环境下开仓。该因子综合了5m、15m、1h、4h、1d多个时间框架的RSI、CCI、AROON、STOCHRSI等指标，当多个时间框架都显示不利条件时，触发保护机制

- **适用场景**: 风险控制, 市场保护, 全局过滤, 多时间框架确认

- **生效条件**: 适用于所有市场状态，用于风险控制

- **计算方式**: `# 全局保护因子 - 多时间框架组合
# 需要先计算所有相关时间框架的指标
# 示例：综合5m、15m、1h、4h、1d的RSI、CCI、AROON、STOCHRSI
df["protections_...`


## Trend 类型因子 (41个)

### AROOND_14

- **频率**: 5m

- **数据来源**: Base timeframe OHLCV

- **直觉**: AROON下降指标衡量下降趋势的强度，当AROOND较低时表示下降趋势减弱，可能预示着下降趋势的结束或反转

- **适用场景**: 下降趋势, 趋势强度, 反转识别

- **生效条件**: 适用于趋势市场，AROOND < 50表示下降趋势减弱

- **计算方式**: `import pandas_ta as pta
import pandas as pd
import numpy as np
# 计算AROON指标
aroon_14 = pta.aroon(df["...`


### AROONU_14_15m

- **频率**: 15m

- **数据来源**: Informative timeframe

- **直觉**: AROON指标识别趋势强度和方向，AROONU下降表示上升动量减弱

- **适用场景**: 趋势识别, 动量分析, 趋势强度判断

- **生效条件**: 适用于趋势市场，AROONU < 70 表示上升趋势减弱

- **计算方式**: `import pandas_ta as pta
import pandas as pd
import numpy as np
from freqtrade.strategy import merge_...`


### AROONU_14_1h

- **频率**: 1h

- **数据来源**: Informative timeframe

- **直觉**: 1小时级别AROON识别中期趋势强度和方向

- **适用场景**: 中期趋势, 趋势强度, 多时间框架

- **生效条件**: 适用于中期趋势，需要1h级别趋势明确

- **计算方式**: `import pandas_ta as pta
import pandas as pd
import numpy as np
from freqtrade.strategy import merge_...`


### AROONU_14_4h

- **频率**: 4h

- **数据来源**: Informative timeframe

- **直觉**: 4小时级别AROON识别长期趋势强度和方向

- **适用场景**: 长期趋势, 趋势强度, 趋势确认

- **生效条件**: 适用于长期趋势，需要4h级别趋势明确

- **计算方式**: `import pandas_ta as pta
import pandas as pd
import numpy as np
from freqtrade.strategy import merge_...`


### BBM_20_2.0

- **频率**: 5m

- **数据来源**: Base timeframe OHLCV

- **直觉**: 布林带中轨是20周期移动平均，当价格在BBM上方时表示上升趋势，下方时表示下降趋势

- **适用场景**: 趋势识别, 趋势确认, 移动平均

- **生效条件**: 适用于趋势市场，BBM作为中轨提供趋势参考

- **计算方式**: `import pandas_ta as pta
import pandas as pd
import numpy as np
# 计算布林带
bbands_20_2 = pta.bbands(df["...`


### CMF_20_15m

- **频率**: 15m

- **数据来源**: Informative timeframe

- **直觉**: CMF指标结合价格和成交量，识别资金流向和趋势强度

- **适用场景**: 趋势识别, 资金流向, 成交量分析

- **生效条件**: 适用于趋势市场，CMF > -0.25 表示资金流入

- **计算方式**: `import pandas_ta as pta
from freqtrade.strategy import merge_informative_pair
# 在informative_15m_ind...`


### CMF_20_1d

- **频率**: 1d

- **数据来源**: Informative timeframe

- **直觉**: 日线级别CMF识别长期资金流向和趋势强度

- **适用场景**: 长期趋势, 资金流向, 长期确认

- **生效条件**: 适用于长期趋势，CMF > -0.20 表示长期资金流入

- **计算方式**: `import pandas_ta as pta
from freqtrade.strategy import merge_informative_pair
# 在informative_1d_indi...`


### CMF_20_1h

- **频率**: 1h

- **数据来源**: Informative timeframe

- **直觉**: 1小时级别CMF识别中期资金流向和趋势强度

- **适用场景**: 中期趋势, 资金流向, 趋势确认

- **生效条件**: 适用于中期趋势，CMF > -0.20 表示中期资金流入

- **计算方式**: `import pandas_ta as pta
from freqtrade.strategy import merge_informative_pair
# 在informative_1h_indi...`


### CMF_20_4h

- **频率**: 4h

- **数据来源**: Informative timeframe

- **直觉**: 4小时级别CMF识别长期资金流向和趋势强度

- **适用场景**: 长期趋势, 资金流向, 趋势确认

- **生效条件**: 适用于长期趋势，CMF > -0.15 表示长期资金流入

- **计算方式**: `import pandas_ta as pta
from freqtrade.strategy import merge_informative_pair
# 在informative_4h_indi...`


### EMA_100

- **频率**: 5m

- **数据来源**: Base timeframe OHLCV

- **直觉**: 100周期EMA识别长期趋势方向，当价格在EMA_100上方时表示长期上升趋势

- **适用场景**: 长期趋势, 趋势过滤, 长期确认

- **生效条件**: 适用于长期趋势，需要识别长期趋势方向

- **计算方式**: `import pandas_ta as pta
df["EMA_100"] = pta.ema(df["close"], length=100, fillna=0.0)...`


### EMA_12

- **频率**: 5m

- **数据来源**: Base timeframe OHLCV

- **直觉**: 12周期EMA常用于短期趋势确认，当价格在EMA_12上方时表示短期上升趋势

- **适用场景**: 短期趋势, 趋势确认, 入场信号

- **生效条件**: 适用于短期趋势，需要平衡敏感性和稳定性

- **计算方式**: `import pandas_ta as pta
df["EMA_12"] = pta.ema(df["close"], length=12)...`


### EMA_16

- **频率**: 5m

- **数据来源**: Base timeframe OHLCV

- **直觉**: 16周期EMA提供短期趋势参考，当价格突破EMA_16时可能预示着短期趋势变化

- **适用场景**: 短期趋势, 趋势确认, 入场时机

- **生效条件**: 适用于短期趋势，需要稳定的趋势信号

- **计算方式**: `import pandas_ta as pta
df["EMA_16"] = pta.ema(df["close"], length=16)...`


### EMA_20

- **频率**: 5m

- **数据来源**: Base timeframe OHLCV

- **直觉**: 20周期EMA对近期价格赋予更高权重，能够快速响应趋势变化。当价格在EMA_20上方且EMA_20上升时，表示中期上升趋势确立，捕捉了市场参与者的趋势跟随行为

- **适用场景**: 中期趋势确认, 趋势强度判断, 持仓管理, 趋势跟踪, 移动平均策略

- **生效条件**: 适用于有明确趋势的市场（ADX > 25），波动率中等，适合中期趋势跟踪

- **计算方式**: `import pandas_ta as pta
df["EMA_20"] = pta.ema(df["close"], length=20)...`


### EMA_200

- **频率**: 5m

- **数据来源**: Base timeframe OHLCV

- **直觉**: 200周期EMA是长期趋势的重要参考线，当价格在EMA_200上方时表示长期上升趋势，常用于判断市场整体方向

- **适用场景**: 长期趋势, 市场方向判断, 大周期过滤

- **生效条件**: 适用于长期趋势，需要识别大周期方向

- **计算方式**: `import pandas_ta as pta
df["EMA_200"] = pta.ema(df["close"], length=200, fillna=0.0)...`


### EMA_26

- **频率**: 5m

- **数据来源**: Base timeframe OHLCV

- **直觉**: 26周期EMA识别中期趋势方向，当价格在EMA_26上方时表示中期上升趋势

- **适用场景**: 中期趋势, 趋势确认, 持仓管理

- **生效条件**: 适用于中期趋势，需要识别中期趋势方向

- **计算方式**: `import pandas_ta as pta
df["EMA_26"] = pta.ema(df["close"], length=26)...`


### EMA_3

- **频率**: 5m

- **数据来源**: Base timeframe OHLCV

- **直觉**: 3周期EMA对价格变化非常敏感，能够快速捕捉短期趋势方向，当价格突破EMA_3时，可能预示着短期趋势的开始

- **适用场景**: 短期趋势跟踪, 快速入场信号, 高频交易

- **生效条件**: 适用于短期趋势，需要快速响应价格变化

- **计算方式**: `import pandas_ta as pta
df["EMA_3"] = pta.ema(df["close"], length=3)...`


### EMA_50

- **频率**: 5m

- **数据来源**: Base timeframe OHLCV

- **直觉**: 50周期EMA识别中长期趋势方向，当EMA_50上升且价格在其上方时，表示中长期上升趋势，常用于趋势过滤

- **适用场景**: 中长期趋势, 趋势过滤, 大周期确认

- **生效条件**: 适用于中长期趋势，需要过滤短期噪音

- **计算方式**: `import pandas_ta as pta
df["EMA_50"] = pta.ema(df["close"], length=50)...`


### EMA_9

- **频率**: 5m

- **数据来源**: Base timeframe OHLCV

- **直觉**: 9周期EMA平衡了敏感性和稳定性，常用于短期趋势确认，当价格在EMA_9上方时表示短期上升趋势

- **适用场景**: 短期趋势确认, 趋势过滤, 入场时机选择

- **生效条件**: 适用于短期趋势，波动率中等

- **计算方式**: `import pandas_ta as pta
df["EMA_9"] = pta.ema(df["close"], length=9)...`


### KST_10_15_20_30_10_10_10_15

- **频率**: 5m

- **数据来源**: Base timeframe OHLCV

- **直觉**: KST指标结合多个周期的ROC，提供综合的趋势强度信号，当KST上升且为正时表示上升趋势加强，下降且为负时表示下降趋势加强

- **适用场景**: 趋势识别, 趋势强度, 综合趋势信号

- **生效条件**: 适用于趋势市场，KST > 0表示上升趋势，KST < 0表示下降趋势

- **计算方式**: `import pandas_ta as pta
import pandas as pd
import numpy as np
# 计算KST指标
kst = pta.kst(df["close"])
...`


### KSTs_9

- **频率**: 5m

- **数据来源**: Base timeframe OHLCV

- **直觉**: KST信号线是KST的平滑版本，当KST上穿KSTs时表示趋势转强，下穿时表示趋势转弱

- **适用场景**: 趋势变化, 趋势确认, 交叉信号

- **生效条件**: 适用于趋势市场，KST与KSTs的金叉死叉提供趋势变化信号

- **计算方式**: `import pandas_ta as pta
import pandas as pd
import numpy as np
# 计算KST指标
kst = pta.kst(df["close"])
...`


### MFI_14

- **频率**: 5m

- **数据来源**: Base timeframe OHLCV

- **直觉**: MFI结合价格和成交量，识别资金流入流出，当MFI处于极端值时，可能预示着价格反转，因为资金流入或流出已经达到极限

- **适用场景**: 资金流向, 超买超卖, 成交量确认

- **生效条件**: 适用于趋势市场，MFI > 80表示超买，MFI < 20表示超卖

- **计算方式**: `import pandas_ta as pta
df["MFI_14"] = pta.mfi(df["high"], df["low"], df["close"], df["volume"], len...`


### OBV

- **频率**: 5m

- **数据来源**: Base timeframe OHLCV

- **直觉**: OBV通过累加成交量来反映资金流向，当OBV上升时表示资金流入（上涨时成交量大于下跌时），下降时表示资金流出，可用于确认价格趋势

- **适用场景**: 资金流向, 趋势确认, 成交量分析

- **生效条件**: 适用于趋势市场，OBV上升表示资金流入，OBV下降表示资金流出

- **计算方式**: `import pandas_ta as pta
df["OBV"] = pta.obv(df["close"], df["volume"])...`


### OBV_change_pct

- **频率**: 5m

- **数据来源**: Base timeframe OHLCV

- **直觉**: OBV变化率捕捉资金流向的变化速度，当OBV_change_pct突然增大时，可能预示着资金流入加速，趋势可能加强

- **适用场景**: 资金流向速度, 趋势加速, 动量分析

- **生效条件**: 适用于趋势市场，OBV变化率反映资金流入流出的速度

- **计算方式**: `import pandas_ta as pta
# 先计算OBV
df["OBV"] = pta.obv(df["close"], df["volume"])
# 计算OBV变化率
df["OBV_c...`


### ROC_2

- **频率**: 5m

- **数据来源**: Base timeframe OHLCV

- **直觉**: 2周期ROC捕捉极短期的价格变化率，对价格变化非常敏感，可用于识别短期动量的快速变化

- **适用场景**: 短期动量, 快速变化, 高频信号

- **生效条件**: 适用于短期动量，需要快速捕捉价格变化

- **计算方式**: `import pandas_ta as pta
df["ROC_2"] = pta.roc(df["close"], length=2)...`


### ROC_9

- **频率**: 5m

- **数据来源**: Base timeframe OHLCV

- **直觉**: 9周期ROC识别中期价格变化率，当ROC_9为正时表示上升趋势，为负时表示下降趋势

- **适用场景**: 中期动量, 趋势识别, 动量分析

- **生效条件**: 适用于中期动量，需要识别价格变化率

- **计算方式**: `import pandas_ta as pta
df["ROC_9"] = pta.roc(df["close"], length=9)...`


### ROC_9_1d

- **频率**: 1d

- **数据来源**: Informative timeframe

- **直觉**: 日线级别ROC识别长期价格变化率和趋势强度

- **适用场景**: 长期趋势, 趋势确认, 长期动量

- **生效条件**: 适用于长期趋势，ROC > -15 表示长期上升趋势

- **计算方式**: `import pandas_ta as pta
from freqtrade.strategy import merge_informative_pair
# 在informative_1d_indi...`


### ROC_9_1h

- **频率**: 1h

- **数据来源**: Informative timeframe

- **直觉**: ROC指标衡量价格变化率，用于识别趋势强度和动量

- **适用场景**: 趋势识别, 动量分析, 趋势强度

- **生效条件**: 适用于趋势市场，ROC > -10 表示上升趋势

- **计算方式**: `import pandas_ta as pta
from freqtrade.strategy import merge_informative_pair
# 在informative_1h_indi...`


### ROC_9_4h

- **频率**: 4h

- **数据来源**: Informative timeframe

- **直觉**: 4小时级别ROC识别长期价格变化率和趋势强度

- **适用场景**: 长期趋势, 动量分析, 趋势确认

- **生效条件**: 适用于长期趋势，ROC < 80 表示上升趋势减弱

- **计算方式**: `import pandas_ta as pta
from freqtrade.strategy import merge_informative_pair
# 在informative_4h_indi...`


### SMA_16

- **频率**: 5m

- **数据来源**: Base timeframe OHLCV

- **直觉**: 16周期SMA提供简单的短期趋势参考，当价格突破SMA_16时可能预示着短期趋势变化

- **适用场景**: 短期趋势, 简单趋势指标, 入场信号

- **生效条件**: 适用于短期趋势，需要简单稳定的趋势指标

- **计算方式**: `import pandas_ta as pta
df["SMA_16"] = pta.sma(df["close"], length=16)...`


### SMA_200

- **频率**: 5m

- **数据来源**: Base timeframe OHLCV

- **直觉**: 200周期SMA是经典的长期趋势指标，当价格在SMA_200上方时表示长期上升趋势，是判断牛熊市的重要参考

- **适用场景**: 长期趋势, 市场方向, 牛熊判断

- **生效条件**: 适用于长期趋势，需要识别大周期方向

- **计算方式**: `import pandas_ta as pta
df["SMA_200"] = pta.sma(df["close"], length=200)...`


### SMA_21

- **频率**: 5m

- **数据来源**: Base timeframe OHLCV

- **直觉**: 21周期SMA提供短期趋势参考，当价格在SMA_21上方时表示短期上升趋势

- **适用场景**: 短期趋势, 趋势确认, 入场时机

- **生效条件**: 适用于短期趋势，需要稳定的趋势信号

- **计算方式**: `import pandas_ta as pta
df["SMA_21"] = pta.sma(df["close"], length=21)...`


### SMA_30

- **频率**: 5m

- **数据来源**: Base timeframe OHLCV

- **直觉**: 30周期SMA识别中期趋势方向，当价格在SMA_30上方时表示中期上升趋势

- **适用场景**: 中期趋势, 趋势确认, 持仓管理

- **生效条件**: 适用于中期趋势，需要识别中期趋势方向

- **计算方式**: `import pandas_ta as pta
df["SMA_30"] = pta.sma(df["close"], length=30)...`


### SMA_9

- **频率**: 5m

- **数据来源**: Base timeframe OHLCV

- **直觉**: 9周期SMA提供简单的短期趋势参考，当价格突破SMA_9时可能预示着短期趋势变化

- **适用场景**: 短期趋势, 简单趋势指标, 入场信号

- **生效条件**: 适用于短期趋势，需要简单稳定的趋势指标

- **计算方式**: `import pandas_ta as pta
df["SMA_9"] = pta.sma(df["close"], length=9)...`


### change_pct

- **频率**: 5m

- **数据来源**: Base timeframe OHLCV

- **直觉**: 蜡烛变化率衡量单根K线的涨跌幅度，当change_pct较大时表示该K线涨幅或跌幅较大，可能预示着短期动量的强弱

- **适用场景**: K线分析, 短期动量, 涨跌幅度

- **生效条件**: 适用于所有市场状态，反映单根蜡烛的涨跌幅度

- **计算方式**: `df["change_pct"] = (df["close"] - df["open"]) / df["open"] * 100.0...`


### close_delta

- **频率**: 5m

- **数据来源**: Base timeframe OHLCV

- **直觉**: 收盘价变化绝对值反映价格的波动幅度，当close_delta增大时表示价格波动增大，可能预示着趋势的开始或加速

- **适用场景**: 波动率分析, 价格波动, 趋势开始

- **生效条件**: 适用于波动率分析，close_delta增大表示价格波动增大

- **计算方式**: `import numpy as np
df["close_delta"] = (df["close"] - df["close"].shift()).abs()...`


### close_max_12

- **频率**: 5m

- **数据来源**: Base timeframe OHLCV

- **直觉**: 12周期最高价识别短期阻力位，当价格接近close_max_12时可能遇到阻力，当价格突破close_max_12时可能预示着上升趋势的延续

- **适用场景**: 阻力位识别, 突破交易, 趋势延续

- **生效条件**: 适用于趋势市场，当价格接近close_max时表示接近短期高点

- **计算方式**: `df["close_max_12"] = df["close"].rolling(12).max()...`


### close_max_48

- **频率**: 5m

- **数据来源**: Base timeframe OHLCV

- **直觉**: 48周期最高价识别中期阻力位，当价格接近close_max_48时可能遇到阻力，当价格突破close_max_48时可能预示着上升趋势的延续

- **适用场景**: 中期阻力, 突破交易, 趋势延续

- **生效条件**: 适用于中期趋势，当价格接近close_max_48时表示接近中期高点

- **计算方式**: `df["close_max_48"] = df["close"].rolling(48).max()...`


### close_max_6

- **频率**: 5m

- **数据来源**: Base timeframe OHLCV

- **直觉**: 6周期最高价识别极短期阻力位，当价格接近close_max_6时可能遇到阻力

- **适用场景**: 极短期阻力, 突破交易, 短期趋势

- **生效条件**: 适用于短期趋势，当价格接近close_max_6时表示接近极短期高点

- **计算方式**: `df["close_max_6"] = df["close"].rolling(6).max()...`


### close_min_12

- **频率**: 5m

- **数据来源**: Base timeframe OHLCV

- **直觉**: 12周期最低价识别短期支撑位，当价格接近close_min_12时可能遇到支撑，当价格跌破close_min_12时可能预示着下降趋势的延续

- **适用场景**: 支撑位识别, 跌破交易, 趋势延续

- **生效条件**: 适用于趋势市场，当价格接近close_min时表示接近短期低点

- **计算方式**: `df["close_min_12"] = df["close"].rolling(12).min()...`


### close_min_48

- **频率**: 5m

- **数据来源**: Base timeframe OHLCV

- **直觉**: 48周期最低价识别中期支撑位，当价格接近close_min_48时可能遇到支撑，当价格跌破close_min_48时可能预示着下降趋势的延续

- **适用场景**: 中期支撑, 跌破交易, 趋势延续

- **生效条件**: 适用于中期趋势，当价格接近close_min_48时表示接近中期低点

- **计算方式**: `df["close_min_48"] = df["close"].rolling(48).min()...`


### close_min_6

- **频率**: 5m

- **数据来源**: Base timeframe OHLCV

- **直觉**: 6周期最低价识别极短期支撑位，当价格接近close_min_6时可能遇到支撑

- **适用场景**: 极短期支撑, 跌破交易, 短期趋势

- **生效条件**: 适用于短期趋势，当价格接近close_min_6时表示接近极短期低点

- **计算方式**: `df["close_min_6"] = df["close"].rolling(6).min()...`


## Volatility 类型因子 (3个)

### BBB_20_2.0

- **频率**: 5m

- **数据来源**: Base timeframe OHLCV

- **直觉**: 布林带带宽指标衡量布林带的宽度，反映市场波动率水平，当BBB增大时表示波动率上升，可能预示着趋势的开始或加速

- **适用场景**: 波动率分析, 趋势开始识别, 市场状态判断

- **生效条件**: 适用于波动率分析，BBB增大表示波动率上升

- **计算方式**: `import pandas_ta as pta
import pandas as pd
import numpy as np
# 计算布林带
bbands_20_2 = pta.bbands(df["...`


### BBB_40_2.0

- **频率**: 5m

- **数据来源**: Base timeframe OHLCV

- **直觉**: 40周期布林带带宽指标衡量布林带的宽度，反映市场波动率水平，当BBB增大时表示波动率上升

- **适用场景**: 波动率分析, 趋势开始识别, 市场状态判断

- **生效条件**: 适用于波动率分析，BBB增大表示波动率上升

- **计算方式**: `import talib.abstract as ta
import numpy as np
# 使用talib计算40周期布林带
upper, middle, lower = ta.BBANDS(d...`


### BBD_40_2.0

- **频率**: 5m

- **数据来源**: Base timeframe OHLCV

- **直觉**: 布林带下轨到中轨的距离反映市场波动幅度，当BBD增大时表示波动增大

- **适用场景**: 波动率分析, 波动幅度, 市场状态

- **生效条件**: 适用于波动率分析，BBD反映布林带下轨到中轨的距离

- **计算方式**: `import talib.abstract as ta
import numpy as np
# 使用talib计算40周期布林带
upper, middle, lower = ta.BBANDS(d...`

