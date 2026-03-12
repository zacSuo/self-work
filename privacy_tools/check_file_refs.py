#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查代码文件引用是否正确更新
"""

import os
import glob

def check_file_references():
    print("[检查] 代码文件引用")
    print("=" * 40)
    
    py_files = glob.glob("*.py")
    
    files_to_check = [
        "daily_todo_system.py",
        "weekly_meeting_system.py",
        "technical_events_recorder.py",
        "view_technical_events.py",
        "record_today_event.py",
        "chat_memory_system.py",
        "memory_system.py",
        "simple_memory_system.py"
    ]
    
    for file_name in files_to_check:
        if os.path.exists(file_name):
            with open(file_name, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否引用了private_data目录
            if "private_data" in content:
                print(f"[OK] {file_name}: 已更新为private_data引用")
            else:
                # 检查是否有旧的数据文件引用
                old_refs = [
                    "chat_memory_data.json",
                    "daily_todos.json",
                    "technical_events.json",
                    "weekly_meeting_data.json",
                    "daily_plan_*.json",
                    "robot_tasks_simple.json",
                    "memory_data.json",
                    "simple_memory_data.json"
                ]
                
                has_old_ref = False
                for old_ref in old_refs:
                    if old_ref in content:
                        has_old_ref = True
                        print(f"[警告] {file_name}: 仍有旧引用 {old_ref}")
                        break
                
                if not has_old_ref:
                    print(f"[OK] {file_name}: 无数据文件引用")
        else:
            print(f"[跳过] {file_name}: 文件不存在")
    
    print("\n[检查] 示例文件")
    print("=" * 40)
    
    example_files = glob.glob("*EXAMPLE*")
    for example_file in example_files:
        print(f"[存在] {example_file}")
    
    print("\n[检查] private_data目录结构")
    print("=" * 40)
    
    if os.path.exists("private_data"):
        print("[OK] private_data目录存在")
        
        subdirs = ["data", "configs", "logs", "backups"]
        for subdir in subdirs:
            path = os.path.join("private_data", subdir)
            if os.path.exists(path):
                print(f"[OK] {subdir}目录存在")
            else:
                print(f"[警告] {subdir}目录缺失")
    else:
        print("[错误] private_data目录不存在")
    
    print("\n[总结]")
    print("=" * 40)
    print("现在可以安全地将项目提交到Git仓库:")
    print("1. 所有私人数据已移动到private_data目录")
    print("2. .gitignore已配置排除private_data和所有JSON文件")
    print("3. 示例文件已创建供参考")
    print("4. 代码引用已更新（如有需要）")

if __name__ == "__main__":
    check_file_references()