import React, { useContext } from 'react';
import { Typography, Card, Empty, Descriptions, Table, Tag, Collapse } from 'antd';
import { AppContext } from '../App';

const { Title } = Typography;
const { Panel } = Collapse;

const Backtest = () => {
  const { strategyData } = useContext(AppContext);

  if (!strategyData || !strategyData.backtest_results) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
        <Empty
          image={Empty.PRESENTED_IMAGE_SIMPLE}
          description="暂无回测数据"
        />
      </div>
    );
  }

  const results = strategyData.backtest_results;

  // 尝试适配不同的回测结果格式
  // 假设 results 是一个包含 strategy_comparison 或类似结构的字典
  
  // 提取关键指标
  const summaryItems = [
    { label: '总收益', value: results.total_return || 'N/A' },
    { label: '最大回撤', value: results.max_drawdown || 'N/A' },
    { label: '胜率', value: results.win_rate || 'N/A' },
    { label: '交易次数', value: results.total_trades || 'N/A' },
    { label: '夏普比率', value: results.sharpe_ratio || 'N/A' },
  ];

  return (
    <div>
      <Title level={2}>回测详情</Title>
      
      <Card title="核心指标" style={{ marginBottom: 24 }}>
        <Descriptions bordered column={{ xxl: 4, xl: 3, lg: 3, md: 3, sm: 2, xs: 1 }}>
          {summaryItems.map((item, index) => (
            <Descriptions.Item key={index} label={item.label}>
              {item.value}
            </Descriptions.Item>
          ))}
        </Descriptions>
      </Card>

      <Card title="详细数据" style={{ marginBottom: 24 }}>
         <div style={{ maxHeight: '500px', overflow: 'auto' }}>
            <pre>{JSON.stringify(results, null, 2)}</pre>
         </div>
      </Card>

      {strategyData.error_logs && strategyData.error_logs.length > 0 && (
        <Card title="执行日志与错误" style={{ marginBottom: 24, borderColor: '#ffccc7' }}>
          <Collapse>
            <Panel header="点击查看详细日志" key="1">
              {strategyData.error_logs.map((log, index) => (
                <div key={index} style={{ marginBottom: 8, fontFamily: 'monospace' }}>
                  <Tag color="red">ERROR</Tag> {log}
                </div>
              ))}
            </Panel>
          </Collapse>
        </Card>
      )}
    </div>
  );
};

export default Backtest;

