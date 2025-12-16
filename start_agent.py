import subprocess
import sys
import time
import os
from pathlib import Path

# 设置环境变量，跳过本地地址的代理（解决本地服务访问问题）
os.environ["NO_PROXY"] = "localhost,127.0.0.1"
os.environ["no_proxy"] = "localhost,127.0.0.1"

def main():
    # Get the root directory
    root_dir = Path(__file__).parent.absolute()
    
    print(f"Starting StrategyAgent from {root_dir}...")

    # Add root directory to PYTHONPATH
    env = os.environ.copy()
    python_path = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = str(root_dir) + os.pathsep + python_path
    
    # 设置环境变量，跳过本地地址的代理（解决本地服务访问问题）
    env["NO_PROXY"] = "localhost,127.0.0.1"
    env["no_proxy"] = "localhost,127.0.0.1"
    
    # Backend command (FastAPI)
    # Using uvicorn directly as a module
    backend_cmd = [
        sys.executable, "-m", "uvicorn", 
        "backend.app.app:app", 
        "--host", "127.0.0.1", 
        "--port", "8000",
    ]
    
    # Frontend command (React/Vite)
    frontend_dir = root_dir / "frontend" / "ui"
    # Check if node_modules exists, if not, install dependencies first
    node_modules_path = frontend_dir / "node_modules"
    if not node_modules_path.exists():
        print("Installing frontend dependencies...")
        import subprocess as sp
        # Use npm.cmd on Windows, npm on Unix
        npm_cmd = "npm.cmd" if os.name == "nt" else "npm"
        install_result = sp.run(
            [npm_cmd, "install", "--registry=https://registry.npmmirror.com", "--prefer-offline", "--no-audit"],
            cwd=frontend_dir,
            env=env
        )
        if install_result.returncode != 0:
            print("Failed to install frontend dependencies")
            return
    
    # Use npm.cmd on Windows, npm on Unix
    npm_cmd = "npm.cmd" if os.name == "nt" else "npm"
    frontend_cmd = [
        npm_cmd, "run", "dev"
    ]

    backend_process = None
    frontend_process = None

    try:
        print("Starting Backend Server (FastAPI)...")
        # Start backend in a new process
        backend_process = subprocess.Popen(backend_cmd, cwd=root_dir, env=env)
        
        # Wait a bit for backend to initialize
        time.sleep(3)
        
        print("Starting Frontend Interface (React/Vite)...")
        # Start frontend in a new process
        frontend_process = subprocess.Popen(frontend_cmd, cwd=frontend_dir, env=env, shell=True)
        
        # 等待 React/Vite 启动
        time.sleep(3)
        
        # 检查进程是否还在运行
        if frontend_process.poll() is not None:
            print(f"\n⚠️  警告: React 前端启动失败！退出代码: {frontend_process.returncode}")
            print("请手动启动 React 前端测试：")
            print(f"  cd frontend/ui && npm run dev")
            backend_process.terminate()
            return
        
        print("\nStrategyAgent is running!")
        print(f"   Backend API: http://127.0.0.1:8000")
        print(f"   Frontend UI: http://localhost:3000")
        print("\nPress Ctrl+C to stop all services.")
        
        # Keep the script running to monitor processes
        while True:
            # 检查进程状态
            if backend_process.poll() is not None:
                print(f"\n⚠️  后端进程已停止！退出代码: {backend_process.returncode}")
                break
            if frontend_process.poll() is not None:
                print(f"\n⚠️  前端进程已停止！退出代码: {frontend_process.returncode}")
                break
            time.sleep(1)
        
    except KeyboardInterrupt:
        print("\n\nStopping services...")
    finally:
        if backend_process:
            backend_process.terminate()
        if frontend_process:
            frontend_process.terminate()
        print("Services stopped.")

if __name__ == "__main__":
    main()

