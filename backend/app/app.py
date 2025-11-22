from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os

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

app = FastAPI(title="Freqtrade Strategy Agent")

# 初始化 Graph
agent_graph = create_graph()

class StrategyRequest(BaseModel):
    strategy_idea: str
    max_iterations: int = 3

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
    
    # 初始化状态
    initial_state = {
        "user_requirement": request.strategy_idea,
        "current_code": None,
        "iteration_count": 0,
        "backtest_results": None,
        "error_logs": [],
        "is_satisfactory": False
    }
    
    try:
        # 运行图
        # LangGraph 的节点是同步的，但是我们可以在 executor 中运行
        import asyncio
        final_state = await asyncio.get_event_loop().run_in_executor(
            None, agent_graph.invoke, initial_state
        )
        
        return {
            "status": "completed",
            "final_code": final_state.get("current_code"),
            "is_satisfactory": final_state.get("is_satisfactory"),
            "iteration_count": final_state.get("iteration_count"),
            "backtest_results": final_state.get("backtest_results"),
            "error_logs": final_state.get("error_logs")
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
