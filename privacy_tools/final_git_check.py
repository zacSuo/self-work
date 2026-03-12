#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终Git仓库提交检查
验证项目已准备好上传到公开Git仓库
"""

import os
import glob
from pathlib import Path

def check_git_ready():
    print("=" * 60)
    print("Git仓库提交准备检查")
    print("=" * 60)
    
    # 1. 检查.gitignore配置
    print("\n[1] 检查.gitignore配置")
    gitignore_path = Path(".gitignore")
    if gitignore_path.exists():
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        required_patterns = [
            "private_data/",
            "*.json",
            "*.bat",
            "__pycache__/",
            "*.log",
            ".vscode/",
            ".idea/",
            ".env",
            "venv/"
        ]
        
        missing_patterns = []
        for pattern in required_patterns:
            if pattern not in content:
                missing_patterns.append(pattern)
        
        if missing_patterns:
            print(f"  [警告] .gitignore缺少以下模式:")
            for pattern in missing_patterns:
                print(f"    - {pattern}")
        else:
            print("  [OK] .gitignore配置完整")
    else:
        print("  [错误] .gitignore文件不存在")
    
    # 2. 检查private_data目录
    print("\n[2] 检查private_data目录")
    private_dir = Path("private_data")
    if private_dir.exists():
        print("  [OK] private_data目录存在")
        
        # 检查子目录
        subdirs = ["data", "configs", "logs", "backups"]
        for subdir in subdirs:
            subdir_path = private_dir / subdir
            if subdir_path.exists():
                print(f"  [OK] {subdir}目录存在")
            else:
                print(f"  [警告] {subdir}目录缺失")
        
        # 检查数据文件
        data_dir = private_dir / "data"
        if data_dir.exists():
            json_files = list(data_dir.glob("*.json"))
            if json_files:
                print(f"  [OK] data目录中有{len(json_files)}个JSON文件")
            else:
                print("  [警告] data目录中没有JSON文件")
        else:
            print("  [错误] data目录不存在")
    else:
        print("  [错误] private_data目录不存在")
    
    # 3. 检查根目录的敏感文件
    print("\n[3] 检查根目录的敏感文件")
    
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
        print(f"  [警告] 根目录中发现{len(found_sensitive)}个敏感文件:")
        for file in found_sensitive:
            print(f"    - {file}")
        print("  [建议] 将这些文件移动到private_data目录")
    else:
        print("  [OK] 根目录中没有敏感文件")
    
    # 4. 检查示例文件
    print("\n[4] 检查示例文件")
    example_files = list(Path(".").glob("*EXAMPLE*"))
    if example_files:
        print(f"  [OK] 有{len(example_files)}个示例文件:")
        for file in example_files:
            print(f"    - {file.name}")
    else:
        print("  [警告] 没有示例文件")
    
    # 5. 检查Python源代码
    print("\n[5] 检查Python源代码")
    py_files = glob.glob("*.py")
    if py_files:
        print(f"  [OK] 有{len(py_files)}个Python源代码文件")
        
        # 检查关键文件是否存在
        key_files = [
            "daily_todo_system.py",
            "weekly_meeting_system.py",
            "technical_events_recorder.py",
            "view_technical_events.py",
            "record_today_event.py",
            "chat_memory_system.py",
            "memory_system.py",
            "simple_memory_system.py",
            "run.py",
            "framework_ui.py"
        ]
        
        missing_key_files = []
        for file in key_files:
            if not Path(file).exists():
                missing_key_files.append(file)
        
        if missing_key_files:
            print(f"  [警告] 缺少{len(missing_key_files)}个关键文件:")
            for file in missing_key_files:
                print(f"    - {file}")
        else:
            print("  [OK] 所有关键文件都存在")
    else:
        print("  [错误] 没有Python源代码文件")
    
    # 6. 检查文档文件
    print("\n[6] 检查文档文件")
    doc_files = [
        "README.md",
        "README_GIT.md",
        "PRIVACY_SETUP_GUIDE.md",
        "requirements.txt"
    ]
    
    missing_doc_files = []
    for file in doc_files:
        if not Path(file).exists():
            missing_doc_files.append(file)
    
    if missing_doc_files:
        print(f"  [警告] 缺少{len(missing_doc_files)}个文档文件:")
        for file in missing_doc_files:
            print(f"    - {file}")
    else:
        print("  [OK] 所有文档文件都存在")
    
    # 7. 模拟git status检查
    print("\n[7] 模拟git status检查")
    print("  [信息] 运行以下命令检查实际git状态:")
    print("    git status")
    print("    git status --ignored")
    
    print("\n" + "=" * 60)
    print("检查总结")
    print("=" * 60)
    
    # 总结建议
    print("\n[建议] 下一步操作:")
    
    if found_sensitive:
        print("  1. 将敏感文件移动到private_data目录")
        print("     python move_private_files.py")
    
    print("  2. 验证.gitignore配置")
    print("     cat .gitignore")
    
    print("  3. 检查哪些文件将被提交")
    print("     git status")
    
    print("  4. 提交到Git仓库")
    print("     git add .")
    print("     git commit -m \"初始化工作管理系统\"")
    print("     git push")
    
    print("\n[注意事项]")
    print("  - private_data/目录不会被提交")
    print("  - 示例文件将被提交供参考")
    print("  - 所有Python源代码将被提交")
    print("  - 文档和配置文件将被提交")
    
    print("\n[完成] 项目已准备好上传到公开Git仓库!")

if __name__ == "__main__":
    check_git_ready()