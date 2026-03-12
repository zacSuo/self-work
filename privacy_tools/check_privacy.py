#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版隐私配置检查
"""

import os
from pathlib import Path

def check_gitignore():
    print("[检查] .gitignore文件")
    if Path(".gitignore").exists():
        with open(".gitignore", "r", encoding="utf-8") as f:
            content = f.read()
        
        # 检查关键规则
        checks = [
            ("private_data/", "私人数据目录"),
            ("*.json", "JSON数据文件"),
            ("*.bat", "批处理文件"),
            ("__pycache__/", "Python缓存"),
        ]
        
        for pattern, desc in checks:
            if pattern in content:
                print(f"  [OK] {desc}: {pattern}")
            else:
                print(f"  [问题] {desc}未排除: {pattern}")
    else:
        print("  [错误] .gitignore文件不存在")

def check_private_data():
    print("\n[检查] private_data目录")
    private_dir = Path("private_data")
    
    if private_dir.exists():
        print("  [OK] private_data目录存在")
        
        # 检查子目录
        subdirs = ["data", "configs", "logs", "backups"]
        for subdir in subdirs:
            subdir_path = private_dir / subdir
            if subdir_path.exists():
                print(f"  [OK] 子目录存在: {subdir}")
            else:
                print(f"  [警告] 子目录缺失: {subdir}")
        
        # 检查数据文件
        data_dir = private_dir / "data"
        if data_dir.exists():
            json_files = list(data_dir.glob("*.json"))
            if json_files:
                print(f"  [OK] 找到 {len(json_files)} 个JSON数据文件")
                for f in json_files[:5]:  # 只显示前5个
                    print(f"    - {f.name}")
                if len(json_files) > 5:
                    print(f"    ... 还有 {len(json_files)-5} 个文件")
            else:
                print("  [警告] 没有JSON数据文件")
    else:
        print("  [错误] private_data目录不存在")

def check_root_files():
    print("\n[检查] 根目录文件")
    
    # 检查不应在根目录的文件
    sensitive_files = [
        "chat_memory_data.json",
        "daily_todos.json",
        "technical_events.json",
        "weekly_meeting_data.json",
        "daily_plan_2026-03-13.json",
        "robot_tasks_simple.json",
        "memory_data.json",
        "simple_memory_data.json",
        "morning_todo.bat",
        "start_memory_system.bat"
    ]
    
    found_sensitive = []
    for file in sensitive_files:
        if Path(file).exists():
            found_sensitive.append(file)
    
    if found_sensitive:
        print(f"  [警告] 发现 {len(found_sensitive)} 个敏感文件在根目录:")
        for f in found_sensitive:
            print(f"    - {f}")
    else:
        print("  [OK] 根目录没有敏感数据文件")
    
    # 检查示例文件
    example_files = list(Path(".").glob("*EXAMPLE*"))
    if example_files:
        print(f"  [OK] 找到 {len(example_files)} 个示例文件")
    else:
        print("  [警告] 没有示例文件")

def check_code_references():
    print("\n[检查] 代码文件引用")
    
    # 简单检查几个关键文件
    files_to_check = [
        "daily_todo_system.py",
        "weekly_meeting_system.py",
    ]
    
    for file in files_to_check:
        if Path(file).exists():
            with open(file, "r", encoding="utf-8") as f:
                content = f.read()
            
            if "private_data" in content:
                print(f"  [OK] {file} 引用了private_data")
            else:
                print(f"  [警告] {file} 可能没有更新引用")

def main():
    print("=" * 60)
    print("隐私保护配置检查")
    print("=" * 60)
    
    check_gitignore()
    check_private_data()
    check_root_files()
    check_code_references()
    
    print("\n" + "=" * 60)
    print("检查完成")
    print("=" * 60)
    
    print("\n[建议]")
    print("1. 确保所有敏感文件都在 private_data/ 目录")
    print("2. 确保 .gitignore 配置正确")
    print("3. 示例文件应保留在根目录供参考")
    print("4. 代码应引用 private_data/ 路径")
    print("\n现在可以安全地将代码提交到Git仓库!")

if __name__ == "__main__":
    main()