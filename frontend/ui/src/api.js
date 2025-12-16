import axios from 'axios';

// Vite 代理配置了 /api -> http://localhost:8000
const API_BASE_URL = '/api';

// WebSocket URL (需要根据实际部署情况调整)
const getWebSocketUrl = () => {
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  const host = window.location.hostname;
  const port = window.location.port || (protocol === 'wss:' ? '443' : '8000');
  // 如果使用Vite代理，可能需要直接连接到后端
  if (host === 'localhost' || host === '127.0.0.1') {
    return `${protocol === 'wss:' ? 'ws:' : 'ws:'}//${host}:8000/ws/generate_strategy`;
  }
  return `${protocol}//${host}:${port}/api/ws/generate_strategy`;
};

export const generateStrategy = async (idea, maxIterations = 3, pairs = ["BTC/USDT", "ETH/USDT"], timeframe = "5m", timerange = "20230101-20231231") => {
  try {
    const response = await axios.post(`${API_BASE_URL}/generate_strategy`, {
      strategy_idea: idea,
      max_iterations: maxIterations,
      pairs: pairs,
      timeframe: timeframe,
      timerange: timerange
    });
    return response.data;
  } catch (error) {
    console.error("Error generating strategy:", error);
    throw error;
  }
};

/**
 * 通过WebSocket实时生成策略
 * @param {Object} params - 策略生成参数
 * @param {string} params.idea - 策略想法
 * @param {number} params.maxIterations - 最大迭代次数
 * @param {string[]} params.pairs - 交易对列表
 * @param {string} params.timeframe - 时间周期
 * @param {string} params.timerange - 时间范围
 * @param {string} params.threadId - 会话ID（可选）
 * @param {boolean} params.isNewConversation - 是否开始新对话
 * @param {Function} params.onStep - 步骤回调函数 (stepInfo) => void
 * @param {Function} params.onComplete - 完成回调函数 (result) => void
 * @param {Function} params.onError - 错误回调函数 (error) => void
 * @returns {Promise} WebSocket连接Promise
 */
export const generateStrategyWithWebSocket = ({ idea, maxIterations = 3, pairs, timeframe, timerange, threadId, isNewConversation = false, onStep, onComplete, onError }) => {
  return new Promise((resolve, reject) => {
    const ws = new WebSocket(getWebSocketUrl());
    
    ws.onopen = () => {
      console.log('WebSocket connected');
      // 发送请求
      ws.send(JSON.stringify({
        strategy_idea: idea,
        max_iterations: maxIterations,
        pairs: pairs,
        timeframe: timeframe,
        timerange: timerange,
        thread_id: threadId || null,
        is_new_conversation: isNewConversation
      }));
    };
    
    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        
        if (data.type === 'step') {
          // 步骤信息
          if (onStep) {
            onStep(data);
          }
        } else if (data.type === 'complete') {
          // 完成
          if (onComplete) {
            onComplete(data);
          }
          ws.close();
          resolve(data);
        } else if (data.type === 'error') {
          // 错误
          const error = new Error(data.message || 'Unknown error');
          if (onError) {
            onError(error);
          }
          ws.close();
          reject(error);
        }
      } catch (error) {
        console.error('Error parsing WebSocket message:', error);
        if (onError) {
          onError(error);
        }
      }
    };
    
    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      if (onError) {
        onError(new Error('WebSocket connection error'));
      }
      reject(error);
    };
    
    ws.onclose = () => {
      console.log('WebSocket closed');
    };
  });
};

