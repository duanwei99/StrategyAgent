import React, { useContext } from 'react';
import { Typography, Card, Empty, Tabs, Button } from 'antd';
import { DownloadOutlined, CodeOutlined, FileTextOutlined } from '@ant-design/icons';
import ReactMarkdown from 'react-markdown';
import { AppContext } from '../App';

const { Title, Paragraph, Text } = Typography;

const Home = () => {
  const { strategyData } = useContext(AppContext);

  if (!strategyData) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
        <Empty
          image={Empty.PRESENTED_IMAGE_SIMPLE}
          description="暂无策略数据，请在右侧输入想法生成策略"
        />
      </div>
    );
  }

  const downloadCode = () => {
    if (!strategyData.final_code) return;
    const blob = new Blob([strategyData.final_code], { type: 'text/x-python' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'strategy.py';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const items = [
    {
      key: 'report',
      label: <span><FileTextOutlined />策略分析报告</span>,
      children: (
        <Card bordered={false}>
          {strategyData.strategy_report ? (
            <ReactMarkdown>{strategyData.strategy_report}</ReactMarkdown>
          ) : (
            <Empty description="未生成报告" />
          )}
        </Card>
      ),
    },
    {
      key: 'code',
      label: <span><CodeOutlined />策略代码</span>,
      children: (
        <Card 
          bordered={false} 
          extra={
            <Button type="primary" icon={<DownloadOutlined />} onClick={downloadCode}>
              下载代码
            </Button>
          }
        >
          {strategyData.final_code ? (
            <pre style={{ 
              backgroundColor: '#f6f8fa', 
              padding: '16px', 
              borderRadius: '8px', 
              overflowX: 'auto',
              maxHeight: '600px' 
            }}>
              <code>{strategyData.final_code}</code>
            </pre>
          ) : (
            <Empty description="未生成代码" />
          )}
        </Card>
      ),
    },
    {
      key: 'logic',
      label: '核心逻辑',
      children: (
        <Card bordered={false}>
          <Title level={4}>设计思路</Title>
          <Paragraph>
            本策略基于以下核心逻辑构建：
          </Paragraph>
           {/* 如果后端返回了专门的逻辑描述字段最好，否则尝试解析报告 */}
           <ReactMarkdown>{strategyData.strategy_report || "暂无详细逻辑描述"}</ReactMarkdown>
        </Card>
      )
    }
  ];

  return (
    <div>
      <Title level={2}>策略概览</Title>
      <Tabs defaultActiveKey="report" items={items} />
    </div>
  );
};

export default Home;

