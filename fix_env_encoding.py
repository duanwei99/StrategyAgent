"""
修复 .env 文件编码问题的工具
将 .env 文件转换为 UTF-8 编码，避免 UnicodeDecodeError
"""
import os
from pathlib import Path


def detect_and_convert_encoding(file_path):
    """
    检测文件编码并转换为 UTF-8
    
    Args:
        file_path: 文件路径
        
    Returns:
        bool: 是否成功转换
    """
    # 尝试的编码列表（从最可能到最不可能）
    encodings = ['utf-8', 'utf-8-sig', 'gbk', 'gb2312', 'gb18030', 'latin-1', 'cp1252']
    
    content = None
    detected_encoding = None
    
    # 尝试读取文件
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
                detected_encoding = encoding
                break
        except (UnicodeDecodeError, UnicodeError):
            continue
        except Exception as e:
            print(f"读取文件时出错 ({encoding}): {e}")
            continue
    
    if content is None:
        print("❌ 无法读取文件，尝试了所有常见编码")
        return False
    
    print(f"✓ 检测到文件编码: {detected_encoding}")
    
    # 如果已经是 UTF-8（不带 BOM），则无需转换
    if detected_encoding == 'utf-8':
        print("✓ 文件已经是 UTF-8 编码，无需转换")
        return True
    
    # 备份原文件
    backup_path = str(file_path) + '.backup'
    try:
        with open(file_path, 'rb') as src:
            with open(backup_path, 'wb') as dst:
                dst.write(src.read())
        print(f"✓ 已创建备份: {backup_path}")
    except Exception as e:
        print(f"⚠️  创建备份失败: {e}")
    
    # 写入 UTF-8 编码
    try:
        with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(content)
        print(f"✓ 已转换为 UTF-8 编码")
        return True
    except Exception as e:
        print(f"❌ 转换失败: {e}")
        # 恢复备份
        if os.path.exists(backup_path):
            try:
                with open(backup_path, 'rb') as src:
                    with open(file_path, 'wb') as dst:
                        dst.write(src.read())
                print("已恢复原文件")
            except:
                pass
        return False


def main():
    print("=" * 70)
    print(".env 文件编码修复工具")
    print("=" * 70)
    print()
    
    env_file = Path(".env")
    
    # 检查文件是否存在
    if not env_file.exists():
        print("❌ 错误: .env 文件不存在")
        print()
        print("请先创建 .env 文件：")
        print("  方法 1: 运行 setup_doubao.bat")
        print("  方法 2: 手动复制 env.example 为 .env")
        print()
        return
    
    print(f"找到文件: {env_file.absolute()}")
    print()
    
    # 显示文件信息
    file_size = env_file.stat().st_size
    print(f"文件大小: {file_size} 字节")
    print()
    
    # 检测并转换编码
    print("正在检测和转换编码...")
    print()
    
    success = detect_and_convert_encoding(env_file)
    
    print()
    print("=" * 70)
    
    if success:
        print("✅ 处理完成！")
        print()
        print("现在可以正常运行：")
        print("  python test_llm_config.py")
        print("  python start_agent.py")
    else:
        print("❌ 处理失败")
        print()
        print("建议手动操作：")
        print("  1. 用文本编辑器（如 VS Code、Notepad++）打开 .env 文件")
        print("  2. 选择 '另存为'")
        print("  3. 编码选择 'UTF-8' 或 'UTF-8 without BOM'")
        print("  4. 保存文件")
    
    print("=" * 70)
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n操作已取消")
    except Exception as e:
        print(f"\n\n发生错误: {e}")
        import traceback
        traceback.print_exc()
    
    input("\n按回车键退出...")

