import React, { useState, createContext, useContext } from 'react';
import { Layout, Menu, theme } from 'antd';
import { RobotOutlined, LineChartOutlined, DashboardOutlined } from '@ant-design/icons';
import { Routes, Route, useNavigate, useLocation } from 'react-router-dom';
import ChatPanel from './components/ChatPanel';
import Home from './pages/Home';
import Backtest from './pages/Backtest';

const { Header, Content, Sider } = Layout;

// 创建全局 Context 用于在 Chat 和其他页面间共享数据
export const AppContext = createContext();

const App = () => {
  const [collapsed, setCollapsed] = useState(false);
  const [strategyData, setStrategyData] = useState(null); // 存储生成的策略数据
  const navigate = useNavigate();
  const location = useLocation();
  const {
    token: { colorBgContainer, borderRadiusLG },
  } = theme.useToken();

  const menuItems = [
    {
      key: '/',
      icon: <DashboardOutlined />,
      label: '策略概览',
    },
    {
      key: '/backtest',
      icon: <LineChartOutlined />,
      label: '回测详情',
    },
  ];

  return (
    <AppContext.Provider value={{ strategyData, setStrategyData }}>
      <Layout style={{ minHeight: '100vh' }}>
        <Sider collapsible collapsed={collapsed} onCollapse={(value) => setCollapsed(value)}>
          <div className="demo-logo-vertical" style={{ height: 32, margin: 16, background: 'rgba(255, 255, 255, 0.2)', borderRadius: 6 }} />
          <Menu 
            theme="dark" 
            defaultSelectedKeys={['/']} 
            selectedKeys={[location.pathname]}
            mode="inline" 
            items={menuItems} 
            onClick={({ key }) => navigate(key)}
          />
        </Sider>
        <Layout>
          {/* 这里是主内容区域，我们将 Chat 放在最右边作为固定侧边栏，或者作为一个 Split View */}
          <Layout style={{ flexDirection: 'row' }}>
            <Content style={{ margin: '16px', flex: 1, overflow: 'hidden', display: 'flex', flexDirection: 'column' }}>
              <div
                style={{
                  padding: 24,
                  background: colorBgContainer,
                  borderRadius: borderRadiusLG,
                  flex: 1,
                  overflowY: 'auto'
                }}
              >
                <Routes>
                  <Route path="/" element={<Home />} />
                  <Route path="/backtest" element={<Backtest />} />
                </Routes>
              </div>
            </Content>
            
            {/* 右侧聊天栏 */}
            <div style={{ 
              width: '400px', 
              borderLeft: '1px solid #f0f0f0', 
              background: '#fff',
              display: 'flex',
              flexDirection: 'column'
            }}>
              <ChatPanel />
            </div>
          </Layout>
        </Layout>
      </Layout>
    </AppContext.Provider>
  );
};

export default App;

