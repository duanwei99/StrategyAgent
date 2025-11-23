import os
# 设置环境变量，跳过本地地址的代理（必须在导入 requests 之前）
os.environ["NO_PROXY"] = "localhost,127.0.0.1,::1"
os.environ["no_proxy"] = "localhost,127.0.0.1,::1"

import streamlit as st
import requests
import json

# ------------------------------------------------------------------------------
# File: StrategyAgent/frontend/app.py
# Purpose: StrategyAgent 的前端界面，基于 Streamlit 实现。
# Function:
#   1. 提供用户输入界面 (策略想法, 迭代次数)。
#   2. 调用后端 FastAPI 接口 (/generate_strategy) 生成策略。
#   3. 展示生成的代码、回测结果和日志。
# Usage:
#   运行命令: streamlit run StrategyAgent/frontend/app.py
# ------------------------------------------------------------------------------

# 设置页面配置
# 页面标题和布局设置
st.set_page_config(
    page_title="Freqtrade Strategy Agent",
    page_icon="🤖",
    layout="wide"
)

# 侧边栏配置
with st.sidebar:
    st.header("配置 / Configuration")
    api_url = st.text_input("Backend API URL", value="http://localhost:8000")
    st.markdown("---")
    st.markdown("""
    ### 说明 / Instructions
    1. 确保后端 API 已启动。
    2. 输入您的策略想法。
    3. 点击生成按钮。
    
    ### 关于 / About
    这是一个基于 AI 的 Freqtrade 策略生成器。
    """)

# 主界面
st.title("🤖 Freqtrade Strategy Agent")
st.markdown("### AI 驱动的量化策略生成与优化系统")

# 输入区域
with st.container():
    col1, col2 = st.columns([3, 1])
    with col1:
        strategy_idea = st.text_area(
            "策略想法 / Strategy Idea",
            height=150,
            placeholder="例如：基于 RSI 和 MACD 金叉的策略，当 RSI < 30 且 MACD 金叉时买入..."
        )
    with col2:
        max_iterations = st.number_input(
            "最大迭代次数 / Max Iterations",
            min_value=1,
            max_value=10,
            value=3,
            help="AI 尝试优化策略的最大次数"
        )
    
    generate_btn = st.button("生成策略 / Generate Strategy", type="primary")

# 处理生成逻辑
if generate_btn:
    if not strategy_idea:
        st.warning("请输入策略想法！")
    else:
        try:
            # 准备请求数据
            payload = {
                "strategy_idea": strategy_idea,
                "max_iterations": max_iterations
            }
            
            # 显示加载状态
            with st.spinner("AI 正在思考、生成代码并进行回测，请耐心等待... (可能需要几分钟)"):
                # 调用后端 API
                response = requests.post(f"{api_url}/generate_strategy", json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # 成功获取结果，展示内容
                    st.success("策略生成完成！")
                    
                    # 创建标签页展示不同内容
                    tab1, tab2, tab3, tab4 = st.tabs(["📋 策略报告", "📝 策略代码", "📊 回测结果", "🐛 调试日志"])
                    
                    with tab1:
                        st.subheader("策略分析报告")
                        strategy_report = data.get("strategy_report")
                        if strategy_report:
                            st.markdown(strategy_report)
                        else:
                            st.info("未生成策略报告")
                    
                    with tab2:
                        st.subheader("生成的 Python 代码")
                        if data.get("final_code"):
                            st.code(data["final_code"], language="python")
                            st.download_button(
                                label="下载策略文件",
                                data=data["final_code"],
                                file_name="strategy.py",
                                mime="text/x-python"
                            )
                        else:
                            st.info("未生成有效代码")

                    with tab3:
                        st.subheader("回测指标")
                        results = data.get("backtest_results")
                        if results:
                            # 尝试美化展示回测结果
                            # 假设 results 是字典结构，可以直接展示 json 或尝试解析关键指标
                            st.json(results)
                            
                            # 如果有特定字段（如收益率等），可以用 metrics 展示
                            # metrics_cols = st.columns(3)
                            # with metrics_cols[0]:
                            #     st.metric("Total Return", results.get('total_return', 'N/A'))
                        else:
                            st.info("暂无回测数据")
                            
                    with tab4:
                        st.subheader("执行日志与错误")
                        logs = data.get("error_logs")
                        if logs:
                            for log in logs:
                                st.text(log)
                        else:
                            st.success("无错误日志")
                            
                    # 状态信息
                    st.markdown("---")
                    st.caption(f"迭代次数: {data.get('iteration_count')} | 结果满意度: {'✅ 满意' if data.get('is_satisfactory') else '❌ 未达标'}")
                    
                else:
                    st.error(f"请求失败: {response.status_code} - {response.text}")
                    
        except requests.exceptions.ConnectionError:
            st.error("无法连接到后端服务器。请确认后端服务已在 http://localhost:8000 启动。")
        except Exception as e:
            st.error(f"发生错误: {str(e)}")


