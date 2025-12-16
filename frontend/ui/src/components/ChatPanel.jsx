import React, { useState, useContext, useRef, useEffect } from 'react';
import { Input, Button, List, Avatar, Spin, message, Select, DatePicker, Space, Collapse } from 'antd';
import { SendOutlined, UserOutlined, RobotOutlined, SettingOutlined, PlusOutlined } from '@ant-design/icons';
import ReactMarkdown from 'react-markdown';
import { generateStrategy, generateStrategyWithWebSocket } from '../api';
import { AppContext } from '../App';
import dayjs from 'dayjs';

const { TextArea } = Input;
const { Option } = Select;
const { Panel } = Collapse;
const { RangePicker } = DatePicker;

// 常用交易对列表
const COMMON_PAIRS = [
  'BTC/USDT',
  'ETH/USDT',
  'BNB/USDT',
  'SOL/USDT',
  'ADA/USDT',
  'XRP/USDT',
  'DOGE/USDT',
  'DOT/USDT',
  'MATIC/USDT',
  'AVAX/USDT',
  'LINK/USDT',
  'UNI/USDT',
  'LTC/USDT',
  'ATOM/USDT',
  'ETC/USDT'
];

// 常用时间周期
const TIMEFRAMES = [
  { value: '1m', label: '1分钟' },
  { value: '5m', label: '5分钟' },
  { value: '15m', label: '15分钟' },
  { value: '30m', label: '30分钟' },
  { value: '1h', label: '1小时' },
  { value: '4h', label: '4小时' },
  { value: '1d', label: '1天' }
];

const ChatPanel = () => {
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState([
    { role: 'assistant', content: '你好！我是你的量化策略助手。请告诉我你的策略想法，我会为你生成代码并进行回测。' }
  ]);
  const { setStrategyData } = useContext(AppContext);
  const messagesEndRef = useRef(null);
  const [currentSteps, setCurrentSteps] = useState([]); // 实时步骤列表
  const loadingMessageIdRef = useRef(null); // 当前loading消息的ID
  const [threadId, setThreadId] = useState(null); // 会话ID，用于记忆管理
  const [isNewConversation, setIsNewConversation] = useState(false); // 是否开始新对话
  
  // 回测参数状态
  const [selectedPairs, setSelectedPairs] = useState(['BTC/USDT', 'ETH/USDT']);
  const [selectedTimeframe, setSelectedTimeframe] = useState('5m');
  const [dateRange, setDateRange] = useState([dayjs('2023-01-01'), dayjs('2023-12-31')]);
  const [showSettings, setShowSettings] = useState(false);
  
  // 开始新对话
  const handleNewConversation = () => {
    setMessages([
      { role: 'assistant', content: '你好！我是你的量化策略助手。请告诉我你的策略想法，我会为你生成代码并进行回测。' }
    ]);
    setThreadId(null);
    setIsNewConversation(true);
    message.info('已开始新对话');
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      // 格式化时间范围
      const timerange = dateRange && dateRange[0] && dateRange[1]
        ? `${dateRange[0].format('YYYYMMDD')}-${dateRange[1].format('YYYYMMDD')}`
        : '20230101-20231231';

      // 添加一个临时的"处理中"消息，用于实时更新
      const loadingMessageId = Date.now();
      setMessages(prev => [...prev, { 
        id: loadingMessageId,
        role: 'assistant', 
        content: `**开始处理策略生成...**\n\n**交易对**: ${selectedPairs.join(', ')}\n**时间周期**: ${TIMEFRAMES.find(t => t.value === selectedTimeframe)?.label || selectedTimeframe}\n**时间范围**: ${dateRange[0]?.format('YYYY-MM-DD')} 至 ${dateRange[1]?.format('YYYY-MM-DD')}\n\n---\n\n*等待后端响应...*`, 
        type: 'loading',
        steps: []
      }]);
      loadingMessageIdRef.current = loadingMessageId;

      // 使用WebSocket实时接收处理步骤
      const result = await generateStrategyWithWebSocket({
        idea: userMessage.content,
        maxIterations: 3,
        pairs: selectedPairs,
        timeframe: selectedTimeframe,
        timerange: timerange,
        threadId: threadId,
        isNewConversation: isNewConversation,
        onStep: (stepData) => {
          // 实时更新处理步骤
          setMessages(prev => {
            return prev.map(msg => {
              if (msg.id === loadingMessageId) {
                const steps = [...(msg.steps || []), stepData];
                let content = `**正在处理策略生成...**\n\n**交易对**: ${selectedPairs.join(', ')}\n**时间周期**: ${TIMEFRAMES.find(t => t.value === selectedTimeframe)?.label || selectedTimeframe}\n**时间范围**: ${dateRange[0]?.format('YYYY-MM-DD')} 至 ${dateRange[1]?.format('YYYY-MM-DD')}\n\n---\n\n`;
                
                // 添加步骤信息
                steps.forEach((step, index) => {
                  const stepEmoji = step.step === 'start' ? '🚀' :
                                   step.step === 'downloading_data' ? '📥' :
                                   step.step === 'data_downloaded' ? '✅' :
                                   step.step === 'data_skipped' ? '⏭️' :
                                   step.step === 'code_generated' ? '💻' :
                                   step.step === 'syntax_checked' ? '🔍' :
                                   step.step === 'backtest_running' ? '📊' :
                                   step.step === 'evaluation' ? '📈' :
                                   step.step === 'report_generated' ? '📝' :
                                   step.step === 'web_searching' ? '🔎' :
                                   '⚙️';
                  
                  content += `${stepEmoji} ${step.message}`;
                  if (step.node) {
                    content += ` (${step.node})`;
                  }
                  if (step.iteration) {
                    content += ` [迭代 ${step.iteration}]`;
                  }
                  content += '\n';
                });
                
                return {
                  ...msg,
                  content: content,
                  steps: steps
                };
              }
              return msg;
            });
          });
        },
        onComplete: (result) => {
          // 更新全局策略数据
          setStrategyData(result);
          
          // 保存会话ID
          if (result.thread_id) {
            setThreadId(result.thread_id);
            setIsNewConversation(false);
          }
          
          // 判断是优化还是生成新策略
          const actionType = result.has_strategy ? '优化' : '生成';
          
          // 移除 loading 消息并添加结果消息
          setMessages(prev => {
            const newMessages = prev.filter(m => m.id !== loadingMessageId);
            return [...newMessages, { 
              role: 'assistant', 
              content: `**策略${actionType}完成！**\n\n**迭代次数**: ${result.iteration_count}\n**满意度**: ${result.is_satisfactory ? '✅ 满意' : '❌ 未达标'}\n\n详细信息请查看左侧面板。` 
            }];
          });
          
          message.success(`策略${actionType}成功！`);
          setLoading(false);
        },
        onError: (error) => {
          setMessages(prev => {
            const newMessages = prev.filter(m => m.id !== loadingMessageId);
            return [...newMessages, { role: 'assistant', content: `**发生错误**: ${error.message || '未知错误'}` }];
          });
          message.error('生成失败');
          setLoading(false);
        }
      });
      
    } catch (error) {
      setMessages(prev => {
        const newMessages = prev.filter(m => m.id !== loadingMessageIdRef.current);
        return [...newMessages, { role: 'assistant', content: `**发生错误**: ${error.message || '未知错误'}` }];
      });
      message.error('生成失败');
      setLoading(false);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      <div style={{ padding: '16px', borderBottom: '1px solid #f0f0f0', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <span style={{ fontWeight: 'bold' }}>交互助手</span>
        <Button 
          type="primary" 
          icon={<PlusOutlined />} 
          size="small"
          onClick={handleNewConversation}
          disabled={loading}
        >
          开始新对话
        </Button>
      </div>
      
      <div style={{ flex: 1, overflowY: 'auto', padding: '16px' }}>
        <List
          itemLayout="horizontal"
          dataSource={messages}
          renderItem={(item) => (
            <List.Item style={{ border: 'none', padding: '8px 0' }}>
              <List.Item.Meta
                avatar={<Avatar icon={item.role === 'user' ? <UserOutlined /> : <RobotOutlined />} style={{ backgroundColor: item.role === 'user' ? '#1890ff' : '#52c41a' }} />}
                title={item.role === 'user' ? '你' : 'AI 助手'}
                description={
                  <div style={{ 
                    backgroundColor: item.role === 'user' ? '#e6f7ff' : '#f6ffed', 
                    padding: '8px 12px', 
                    borderRadius: '8px',
                    marginTop: '4px',
                    display: 'inline-block',
                    maxWidth: '100%'
                  }}>
                    {item.type === 'loading' ? <Spin size="small" /> : <ReactMarkdown>{item.content}</ReactMarkdown>}
                  </div>
                }
              />
            </List.Item>
          )}
        />
        <div ref={messagesEndRef} />
      </div>

      <div style={{ padding: '16px', borderTop: '1px solid #f0f0f0' }}>
        <Collapse 
          activeKey={showSettings ? ['settings'] : []}
          onChange={(keys) => setShowSettings(keys.includes('settings'))}
          style={{ marginBottom: '12px' }}
        >
          <Panel 
            header={
              <span>
                <SettingOutlined style={{ marginRight: '8px' }} />
                回测参数设置
              </span>
            } 
            key="settings"
          >
            <Space direction="vertical" style={{ width: '100%' }} size="middle">
              <div>
                <div style={{ marginBottom: '8px', fontWeight: 500 }}>交易对（可多选）:</div>
                <Select
                  mode="multiple"
                  style={{ width: '100%' }}
                  placeholder="选择交易对"
                  value={selectedPairs}
                  onChange={setSelectedPairs}
                  disabled={loading}
                >
                  {COMMON_PAIRS.map(pair => (
                    <Option key={pair} value={pair}>{pair}</Option>
                  ))}
                </Select>
              </div>
              
              <div>
                <div style={{ marginBottom: '8px', fontWeight: 500 }}>时间周期:</div>
                <Select
                  style={{ width: '100%' }}
                  value={selectedTimeframe}
                  onChange={setSelectedTimeframe}
                  disabled={loading}
                >
                  {TIMEFRAMES.map(tf => (
                    <Option key={tf.value} value={tf.value}>{tf.label}</Option>
                  ))}
                </Select>
              </div>
              
              <div>
                <div style={{ marginBottom: '8px', fontWeight: 500 }}>回测时间范围:</div>
                <RangePicker
                  style={{ width: '100%' }}
                  value={dateRange}
                  onChange={setDateRange}
                  format="YYYY-MM-DD"
                  disabled={loading}
                />
              </div>
            </Space>
          </Panel>
        </Collapse>
        
        <TextArea
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="输入你的策略想法..."
          autoSize={{ minRows: 2, maxRows: 6 }}
          onPressEnter={(e) => {
            if (!e.shiftKey) {
              e.preventDefault();
              handleSend();
            }
          }}
          disabled={loading}
        />
        <Button 
          type="primary" 
          icon={<SendOutlined />} 
          onClick={handleSend} 
          loading={loading}
          style={{ marginTop: '8px', width: '100%' }}
        >
          发送
        </Button>
      </div>
    </div>
  );
};

export default ChatPanel;

