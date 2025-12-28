import subprocess
import sys
import time
import os
import socket
from pathlib import Path

# 设置环境变量，跳过本地地址的代理（解决本地服务访问问题）
os.environ["NO_PROXY"] = "localhost,127.0.0.1"
os.environ["no_proxy"] = "localhost,127.0.0.1"

def is_port_in_use(host, port):
    """检查端口是否被占用"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((host, port))
            return False
        except OSError:
            return True

def kill_process_on_port(port):
    """在 Windows 上关闭占用指定端口的进程"""
    try:
        # 查找占用端口的进程
        result = subprocess.run(
            ["netstat", "-ano"],
            capture_output=True,
            text=True,
            check=False
        )
        
        for line in result.stdout.split('\n'):
            if f':{port}' in line and 'LISTENING' in line:
                parts = line.split()
                if len(parts) >= 5:
                    pid = parts[-1]
                    try:
                        # 终止进程
                        subprocess.run(["taskkill", "/F", "/PID", pid], check=False)
                        print(f"已关闭占用端口 {port} 的进程 (PID: {pid})")
                        time.sleep(1)  # 等待进程关闭
                        return True
                    except Exception as e:
                        print(f"关闭进程失败: {e}")
        return False
    except Exception as e:
        print(f"查找占用端口的进程时出错: {e}")
        return False

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
        # 检查端口 8000 是否被占用
        backend_port = 8000
        if is_port_in_use("127.0.0.1", backend_port):
            print(f"⚠️  端口 {backend_port} 已被占用，尝试关闭占用该端口的进程...")
            if kill_process_on_port(backend_port):
                print("等待端口释放...")
                time.sleep(2)
                # 再次检查
                if is_port_in_use("127.0.0.1", backend_port):
                    print(f"❌ 端口 {backend_port} 仍被占用，请手动关闭占用该端口的进程")
                    print(f"   运行命令: netstat -ano | findstr :{backend_port}")
                    return
            else:
                print(f"❌ 无法自动关闭占用端口 {backend_port} 的进程")
                print(f"   请手动运行: netstat -ano | findstr :{backend_port}")
                print(f"   然后使用 taskkill /F /PID <进程ID> 关闭进程")
                return
        
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
        # 使用 taskkill /F /T 强制杀死进程树
        if backend_process:
            try:
                if os.name == 'nt':
                    subprocess.run(["taskkill", "/F", "/T", "/PID", str(backend_process.pid)], 
                                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                else:
                    backend_process.terminate()
            except Exception as e:
                print(f"Error killing backend process: {e}")
                
        if frontend_process:
            try:
                if os.name == 'nt':
                    subprocess.run(["taskkill", "/F", "/T", "/PID", str(frontend_process.pid)],
                                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                else:
                    frontend_process.terminate()
            except Exception as e:
                print(f"Error killing frontend process: {e}")
                
        print("Services stopped.")

if __name__ == "__main__":
    main()

