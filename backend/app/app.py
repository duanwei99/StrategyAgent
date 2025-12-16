from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import json
import asyncio
import queue
import threading

# 加载环境变量（支持不同编码）
def load_env_with_fallback():
    """尝试使用不同编码加载 .env 文件"""
    encodings = ['utf-8', 'utf-8-sig', 'gbk', 'gb2312', 'latin-1']
    
    for encoding in encodings:
        try:
            load_dotenv(encoding=encoding)
            return True
        except (UnicodeDecodeError, Exception):
            continue
    
    try:
        load_dotenv()
        return True
    except:
        return False

load_env_with_fallback()

from ..agent.graph import create_graph
from ..agent.state import AgentState
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Freqtrade Strategy Agent")

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该限制为前端的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化 Graph
agent_graph = create_graph()

class StrategyRequest(BaseModel):
    strategy_idea: str
    max_iterations: int = 3
    pairs: list[str] = ["BTC/USDT", "ETH/USDT"]  # 交易对列表
    timeframe: str = "5m"  # 时间周期，例如 "5m", "15m", "1h", "4h", "1d"
    timerange: str = "20230101-20231231"  # 回测时间范围
    thread_id: str | None = None  # 会话ID，用于记忆管理
    is_new_conversation: bool = False  # 是否开始新对话

@app.get("/")
async def root():
    return {"message": "Strategy Agent API is running"}

@app.post("/generate_strategy")
async def generate_strategy(request: StrategyRequest):
    """
    触发策略生成流程
    注意：由于包含回测，此接口响应时间可能较长
    """
    print(f"Received request: {request.strategy_idea}")
    print(f"Pairs: {request.pairs}, Timeframe: {request.timeframe}, Timerange: {request.timerange}")
    
    # 在回测前下载数据
    from ..tools.data_downloader import download_data_if_needed
    download_result = download_data_if_needed(
        pairs=request.pairs,
        timeframe=request.timeframe,
        timerange=request.timerange,
        force_download=False  # 如果数据已存在则跳过下载
    )
    
    if not download_result.get("success") and not download_result.get("skipped"):
        print(f"警告: 数据下载失败，但继续执行回测: {download_result.get('message')}")
        # 不阻止流程，因为可能使用模拟模式或已有部分数据
    
    # 处理会话ID和记忆
    import uuid
    thread_id = request.thread_id
    if not thread_id or request.is_new_conversation:
        thread_id = str(uuid.uuid4())
        print(f"创建新会话: {thread_id}")
    
    # 检查会话中是否已有策略
    has_strategy = False
    if thread_id and not request.is_new_conversation:
        try:
            config = {"configurable": {"thread_id": thread_id}}
            checkpoint = agent_graph.get_state(config)
            if checkpoint and checkpoint.values:
                previous_state = checkpoint.values
                has_strategy = previous_state.get("has_strategy", False)
        except Exception as e:
            print(f"获取会话状态失败: {e}")
    
    # 初始化状态
    initial_state = {
        "user_requirement": request.strategy_idea,
        "current_code": None,
        "iteration_count": 0,
        "backtest_results": None,
        "error_logs": [],
        "is_satisfactory": False,
        "search_results": None,
        "strategy_report": None,
        "pairs": request.pairs,
        "timeframe": request.timeframe,
        "timerange": request.timerange,
        "has_strategy": has_strategy
    }
    
    # 如果会话中已有策略，恢复状态
    if has_strategy and thread_id and not request.is_new_conversation:
        try:
            config = {"configurable": {"thread_id": thread_id}}
            checkpoint = agent_graph.get_state(config)
            if checkpoint and checkpoint.values:
                previous_state = checkpoint.values
                if previous_state.get("current_code"):
                    initial_state["current_code"] = previous_state["current_code"]
                initial_state["iteration_count"] = previous_state.get("iteration_count", 0)
        except Exception as e:
            print(f"恢复会话状态失败: {e}")
    
    try:
        # 运行图，传入 thread_id
        import asyncio
        config = {"configurable": {"thread_id": thread_id}}
        final_state = await asyncio.get_event_loop().run_in_executor(
            None, lambda: agent_graph.invoke(initial_state, config)
        )
        
        return {
            "status": "completed",
            "thread_id": thread_id,
            "final_code": final_state.get("current_code"),
            "is_satisfactory": final_state.get("is_satisfactory"),
            "iteration_count": final_state.get("iteration_count"),
            "backtest_results": final_state.get("backtest_results"),
            "error_logs": final_state.get("error_logs"),
            "strategy_report": final_state.get("strategy_report"),
            "search_results": final_state.get("search_results"),
            "has_strategy": final_state.get("has_strategy", False)
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.websocket("/ws/generate_strategy")
async def websocket_generate_strategy(websocket: WebSocket):
    """
    WebSocket端点：实时推送策略生成步骤
    """
    await websocket.accept()
    
    try:
        # 接收初始请求
        data = await websocket.receive_json()
        request = StrategyRequest(**data)
        
        print(f"WebSocket: Received request: {request.strategy_idea}")
        
        # 发送开始消息
        await websocket.send_json({
            "type": "step",
            "step": "start",
            "message": "开始策略生成流程",
            "node": None
        })
        
        # 在回测前下载数据
        await websocket.send_json({
            "type": "step",
            "step": "downloading_data",
            "message": f"正在下载数据: {', '.join(request.pairs)}",
            "node": None
        })
        
        from ..tools.data_downloader import download_data_if_needed
        download_result = download_data_if_needed(
            pairs=request.pairs,
            timeframe=request.timeframe,
            timerange=request.timerange,
            force_download=False
        )
        
        if download_result.get("success"):
            await websocket.send_json({
                "type": "step",
                "step": "data_downloaded",
                "message": "数据下载完成",
                "node": None
            })
        elif download_result.get("skipped"):
            await websocket.send_json({
                "type": "step",
                "step": "data_skipped",
                "message": "数据已存在，跳过下载",
                "node": None
            })
        else:
            await websocket.send_json({
                "type": "step",
                "step": "data_warning",
                "message": f"数据下载警告: {download_result.get('message', '未知错误')}",
                "node": None
            })
        
        # 处理会话ID和记忆
        import uuid
        thread_id = request.thread_id
        if not thread_id or request.is_new_conversation:
            # 创建新的会话ID
            thread_id = str(uuid.uuid4())
            print(f"创建新会话: {thread_id}")
        else:
            print(f"使用现有会话: {thread_id}")
        
        # 检查会话中是否已有策略
        has_strategy = False
        if thread_id and not request.is_new_conversation:
            try:
                # 尝试从 checkpointer 获取之前的会话状态
                config = {"configurable": {"thread_id": thread_id}}
                # 获取最新的检查点
                checkpoint = agent_graph.get_state(config)
                if checkpoint and checkpoint.values:
                    previous_state = checkpoint.values
                    has_strategy = previous_state.get("has_strategy", False)
                    if has_strategy:
                        print(f"会话 {thread_id} 中已有策略，将进行优化")
            except Exception as e:
                print(f"获取会话状态失败: {e}，将作为新会话处理")
        
        # 初始化状态
        initial_state = {
            "user_requirement": request.strategy_idea,
            "current_code": None,
            "iteration_count": 0,
            "backtest_results": None,
            "error_logs": [],
            "is_satisfactory": False,
            "search_results": None,
            "strategy_report": None,
            "pairs": request.pairs,
            "timeframe": request.timeframe,
            "timerange": request.timerange,
            "has_strategy": has_strategy  # 设置会话记忆标志
        }
        
        # 如果会话中已有策略，从之前的检查点恢复状态
        if has_strategy and thread_id and not request.is_new_conversation:
            try:
                config = {"configurable": {"thread_id": thread_id}}
                checkpoint = agent_graph.get_state(config)
                if checkpoint and checkpoint.values:
                    previous_state = checkpoint.values
                    # 保留之前的策略代码和迭代次数
                    if previous_state.get("current_code"):
                        initial_state["current_code"] = previous_state["current_code"]
                    initial_state["iteration_count"] = previous_state.get("iteration_count", 0)
                    print(f"从会话 {thread_id} 恢复状态，当前代码长度: {len(initial_state['current_code'] or '')}")
            except Exception as e:
                print(f"恢复会话状态失败: {e}")
        
        # 创建队列用于线程间通信
        step_queue = queue.Queue()
        final_state_container = {"state": None, "error": None}
        
        def run_graph_with_stream():
            """在后台线程中运行图，将步骤信息放入队列"""
            try:
                final_state = None
                
                # 配置 thread_id 用于会话记忆
                config = {"configurable": {"thread_id": thread_id}}
                
                # 使用stream模式获取每个节点的执行信息，传入 thread_id
                for event in agent_graph.stream(initial_state, config):
                    # event格式: {node_name: state_update}
                    for node_name, state_update in event.items():
                        # 将步骤信息放入队列
                        step_info = {
                            "type": "step",
                            "step": "node_execution",
                            "node": node_name,
                            "message": f"正在执行: {node_name}",
                            "iteration": state_update.get("iteration_count", 0)
                        }
                        
                        # 根据节点类型添加详细信息
                        if node_name == "strategy_generator":
                            step_info.update({
                                "step": "code_generated",
                                "message": "策略代码已生成",
                                "has_code": bool(state_update.get("current_code"))
                            })
                        elif node_name == "syntax_checker":
                            has_errors = bool(state_update.get("error_logs"))
                            step_info.update({
                                "step": "syntax_checked",
                                "message": "语法检查完成" if not has_errors else "发现语法错误，需要修复",
                                "has_errors": has_errors
                            })
                        elif node_name == "backtest_executor":
                            step_info.update({
                                "step": "backtest_running",
                                "message": "正在执行回测...",
                            })
                        elif node_name == "evaluator":
                            is_satisfactory = state_update.get("is_satisfactory", False)
                            step_info.update({
                                "step": "evaluation",
                                "message": f"评估结果: {'满意' if is_satisfactory else '需要优化'}",
                                "is_satisfactory": is_satisfactory
                            })
                        elif node_name == "report_generator":
                            step_info.update({
                                "step": "report_generated",
                                "message": "策略报告已生成",
                            })
                        elif node_name == "web_search":
                            step_info.update({
                                "step": "web_searching",
                                "message": "正在搜索相关信息...",
                            })
                        
                        step_queue.put(step_info)
                        
                        # 保存最终状态
                        if state_update:
                            final_state = state_update
                
                final_state_container["state"] = final_state or initial_state
            except Exception as e:
                final_state_container["error"] = str(e)
                import traceback
                final_state_container["error"] = traceback.format_exc()
        
        # 在executor中运行图
        loop = asyncio.get_event_loop()
        executor_task = loop.run_in_executor(None, run_graph_with_stream)
        
        # 同时监听队列并发送步骤信息
        async def send_steps():
            """从队列读取步骤信息并发送"""
            while True:
                try:
                    # 非阻塞获取队列项
                    try:
                        step_info = step_queue.get_nowait()
                        await websocket.send_json(step_info)
                    except queue.Empty:
                        # 检查executor是否完成
                        if executor_task.done():
                            # 处理剩余的队列项
                            while not step_queue.empty():
                                try:
                                    step_info = step_queue.get_nowait()
                                    await websocket.send_json(step_info)
                                except queue.Empty:
                                    break
                            break
                        # 等待一小段时间
                        await asyncio.sleep(0.1)
                except Exception as e:
                    print(f"Error sending step: {e}")
                    break
        
        # 等待executor完成并发送步骤
        await asyncio.gather(executor_task, send_steps())
        
        # 获取最终状态
        if final_state_container["error"]:
            raise Exception(final_state_container["error"])
        
        final_state = final_state_container["state"]
        
        # 发送完成消息和最终结果
        await websocket.send_json({
            "type": "complete",
            "status": "completed",
            "thread_id": thread_id,  # 返回会话ID
            "final_code": final_state.get("current_code"),
            "is_satisfactory": final_state.get("is_satisfactory"),
            "iteration_count": final_state.get("iteration_count"),
            "backtest_results": final_state.get("backtest_results"),
            "error_logs": final_state.get("error_logs"),
            "strategy_report": final_state.get("strategy_report"),
            "search_results": final_state.get("search_results"),
            "has_strategy": final_state.get("has_strategy", False)
        })
        
    except WebSocketDisconnect:
        print("WebSocket disconnected")
    except Exception as e:
        import traceback
        traceback.print_exc()
        await websocket.send_json({
            "type": "error",
            "message": str(e),
            "detail": traceback.format_exc()
        })
