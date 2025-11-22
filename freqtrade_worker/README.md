# Freqtrade Worker 目录

这个目录用于运行 Freqtrade 回测。

## 设置步骤

### 1. 安装 Freqtrade

确保你已经安装了 Freqtrade。如果还没有安装，请参考 [Freqtrade 官方文档](https://www.freqtrade.io/en/stable/installation/)。

```bash
# 使用 pip 安装
pip install freqtrade
```

### 2. 下载历史数据

在运行回测之前，你需要下载交易对的历史数据：

```bash
# 进入 freqtrade_worker 目录
cd freqtrade_worker

# 下载数据（示例：下载 BTC/USDT 和 ETH/USDT 的 1小时 K线数据）
freqtrade download-data \
  --config user_data/config.json \
  --timerange 20230101-20231231 \
  --timeframe 1h \
  --pairs BTC/USDT ETH/USDT BNB/USDT SOL/USDT ADA/USDT
```

### 3. 验证数据

检查数据是否下载成功：

```bash
freqtrade list-data --config user_data/config.json
```

### 4. 测试回测

你可以手动测试回测功能：

```bash
# 使用示例策略进行回测
freqtrade backtesting \
  --config user_data/config.json \
  --strategy SampleStrategy \
  --timerange 20230101-20230201
```

## 目录结构

```
freqtrade_worker/
├── user_data/
│   ├── strategies/          # AI 生成的策略将保存在这里
│   ├── data/                # 历史行情数据
│   ├── backtest_results/    # 回测结果
│   └── config.json          # Freqtrade 配置文件
└── README.md                # 本文件
```

## 注意事项

1. 确保在运行 StrategyAgent 之前已经下载了足够的历史数据。
2. `config.json` 中的交易对列表应该与下载的数据一致。
3. 回测时间范围应该在已下载数据的范围内。
4. 默认配置使用的是 Binance 交易所，可以根据需要修改。

