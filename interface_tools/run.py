#!/usr/bin/env python3
"""
记忆系统启动脚本
"""

import os
import sys
from memory_system import MemorySystem
from web_interface import app

def main():
    """主启动函数"""
    print("=== 记忆系统启动 ===")
    
    # 检查依赖
    try:
        import flask
        print("✓ Flask 依赖检查通过")
    except ImportError:
        print("✗ 缺少Flask依赖，请运行: pip install -r requirements.txt")
        return
    
    # 初始化记忆系统
    memory = MemorySystem()
    print("✓ 记忆系统初始化完成")
    
    # 显示系统信息
    summary = memory.generate_summary()
    print(f"\n系统状态:")
    print(f"  习惯记录: {summary['total_habits']} 个")
    print(f"  工作方式: {summary['total_work_styles']} 个")
    print(f"  决策记录: {summary['total_decisions']} 个")
    print(f"  任务安排: {summary['total_tasks']} 个")
    print(f"  任务完成率: {summary['task_completion_rate']:.1%}")
    
    print(f"\nWeb界面将在 http://localhost:5000 启动...")
    print("按 Ctrl+C 停止服务")
    
    # 启动Web服务
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == "__main__":
    main()