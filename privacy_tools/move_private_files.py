#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
移动私人文件工具
将包含个人隐私信息的文件移动到private_data目录
并更新相关代码中的文件引用
"""

import os
import shutil
import json
from pathlib import Path

def create_private_data_structure():
    """创建私人数据目录结构"""
    private_dir = Path("private_data")
    
    # 创建主目录
    private_dir.mkdir(exist_ok=True)
    
    # 创建子目录结构
    subdirs = [
        "data",
        "configs", 
        "logs",
        "backups"
    ]
    
    for subdir in subdirs:
        (private_dir / subdir).mkdir(exist_ok=True)
    
    print(f"[创建] 私人数据目录结构: {private_dir}/")
    for subdir in subdirs:
        print(f"  - {private_dir}/{subdir}/")
    
    return private_dir

def identify_private_files():
    """识别包含私人信息的文件"""
    private_files = []
    
    # 数据文件（包含个人会议安排、任务历史等）
    data_files = [
        "chat_memory_data.json",
        "daily_todos.json", 
        "technical_events.json",
        "weekly_meeting_data.json",
        "daily_plan_2026-03-13.json",
        "robot_tasks_simple.json",
        "memory_data.json",
        "simple_memory_data.json"
    ]
    
    # 批处理文件（包含本地路径）
    batch_files = [
        "morning_todo.bat",
        "start_memory_system.bat"
    ]
    
    # 配置文件（可能包含个人设置）
    config_files = [
        "config.json"  # 检查是否需要处理
    ]
    
    all_files = data_files + batch_files
    
    for filename in all_files:
        if Path(filename).exists():
            private_files.append(filename)
            print(f"[发现] 私人文件: {filename}")
        else:
            print(f"[跳过] 文件不存在: {filename}")
    
    return private_files

def move_files_to_private_dir(files_to_move, private_dir):
    """移动文件到私人数据目录"""
    moved_files = []
    
    for filename in files_to_move:
        source = Path(filename)
        destination = private_dir / "data" / filename
        
        if source.exists():
            # 备份原文件
            backup_path = private_dir / "backups" / f"{filename}.backup"
            shutil.copy2(source, backup_path)
            
            # 移动文件
            shutil.move(str(source), str(destination))
            moved_files.append(filename)
            print(f"[移动] {filename} -> {destination}")
            
            # 创建占位符文件（说明文件已移动）
            placeholder = source.with_name(f"{source.stem}_EXAMPLE{source.suffix}")
            create_example_file(placeholder, filename)
        else:
            print(f"[警告] 源文件不存在: {filename}")
    
    return moved_files

def create_example_file(filepath, original_filename):
    """创建示例文件，说明原始文件已移动到private_data目录"""
    
    examples = {
        "chat_memory_data.json": {
            "description": "对话记忆数据文件（示例）",
            "content": [
                {
                    "timestamp": "2026-03-12T10:00:00",
                    "user_message": "用户消息示例",
                    "ai_response": "AI回复示例",
                    "summary": "对话摘要示例"
                }
            ]
        },
        "daily_todos.json": {
            "description": "每日待办事项数据文件（示例）",
            "content": {
                "daily_todos": [
                    {
                        "date": "2026-03-12",
                        "day": "周四",
                        "available_hours": 6.8,
                        "tasks": [
                            {
                                "id": "task_001",
                                "description": "示例任务",
                                "priority": 0.8,
                                "estimated_hours": 1.0
                            }
                        ]
                    }
                ]
            }
        },
        "technical_events.json": {
            "description": "技术事件记录文件（示例）",
            "content": [
                {
                    "id": "EVENT_EXAMPLE_001",
                    "date": "2026-03-12",
                    "title": "技术问题解决方案示例",
                    "description": "这是一个示例技术事件记录",
                    "tags": ["示例", "技术"],
                    "importance": "medium"
                }
            ]
        },
        "weekly_meeting_data.json": {
            "description": "每周会议数据文件（示例）",
            "content": {
                "meetings": [
                    {
                        "day": "周一",
                        "name": "项目站会示例",
                        "time": "09:30-10:00",
                        "duration": "0.5小时",
                        "priority": "中"
                    }
                ]
            }
        },
        "config.json": {
            "description": "配置文件（示例）",
            "content": {
                "framework": {
                    "name": "示例框架",
                    "version": "1.0.0"
                },
                "user_preferences": {
                    "language": "zh-CN",
                    "theme": "default"
                }
            }
        }
    }
    
    if original_filename in examples:
        example = examples[original_filename]
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(example["content"], f, ensure_ascii=False, indent=2)
        
        # 添加注释
        with open(filepath, 'r+', encoding='utf-8') as f:
            content = f.read()
            f.seek(0, 0)
            comment = f"// {example['description']}\n// 原始文件已移动到 private_data/data/{original_filename}\n// 请根据需要复制此文件并修改内容\n\n"
            f.write(comment + content)
        
        print(f"[创建] 示例文件: {filepath}")
    else:
        # 创建通用示例文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# {original_filename} 示例文件\n")
            f.write(f"# 原始文件已移动到 private_data/data/{original_filename}\n")
            f.write(f"# 请根据需要创建实际数据\n\n")
            f.write("{\n")
            f.write('  "note": "这是一个示例文件，实际数据已移动到private_data目录"\n')
            f.write("}\n")
        
        print(f"[创建] 通用示例文件: {filepath}")

def update_code_references(private_dir):
    """更新代码中对私人文件的引用"""
    
    # 需要更新的文件列表
    files_to_update = [
        "daily_todo_system.py",
        "weekly_meeting_system.py",
        "technical_events_recorder.py",
        "view_technical_events.py",
        "record_today_event.py",
        "chat_memory_system.py",
        "memory_system.py",
        "simple_memory_system.py"
    ]
    
    updates_made = []
    
    for filename in files_to_update:
        if not Path(filename).exists():
            continue
        
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 更新文件路径引用
        replacements = [
            ('"chat_memory_data.json"', f'"{private_dir}/data/chat_memory_data.json"'),
            ('"daily_todos.json"', f'"{private_dir}/data/daily_todos.json"'),
            ('"technical_events.json"', f'"{private_dir}/data/technical_events.json"'),
            ('"weekly_meeting_data.json"', f'"{private_dir}/data/weekly_meeting_data.json"'),
            ('"robot_tasks_simple.json"', f'"{private_dir}/data/robot_tasks_simple.json"'),
            ('"memory_data.json"', f'"{private_dir}/data/memory_data.json"'),
            ('"simple_memory_data.json"', f'"{private_dir}/data/simple_memory_data.json"'),
            ('weekly_meeting_data.json', f'{private_dir}/data/weekly_meeting_data.json'),
            ('technical_events.json', f'{private_dir}/data/technical_events.json'),
        ]
        
        for old, new in replacements:
            if old in content:
                content = content.replace(old, new)
        
        if content != original_content:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            updates_made.append(filename)
            print(f"[更新] 代码引用: {filename}")
    
    return updates_made

def create_usage_guide(private_dir):
    """创建使用指南"""
    guide_path = Path("PRIVACY_SETUP_GUIDE.md")
    
    guide_content = f"""# 隐私保护配置指南

## 📋 概述

为了保护您的个人隐私信息，所有包含私人数据的文件都已移动到 `{private_dir}/` 目录。这些文件不会被提交到Git仓库。

## 📁 目录结构

```
{private_dir}/
├── data/                    # 私人数据文件
│   ├── chat_memory_data.json
│   ├── daily_todos.json
│   ├── technical_events.json
│   ├── weekly_meeting_data.json
│   └── ...
├── configs/                # 私人配置文件
├── logs/                   # 日志文件
├── backups/                # 备份文件
└── README_PRIVATE.md      # 私人目录说明
```

## 🔒 已保护的文件

### 已移动到 {private_dir}/data/ 的文件：
- `chat_memory_data.json` - 对话记忆数据
- `daily_todos.json` - 个人待办事项历史
- `technical_events.json` - 技术事件记录
- `weekly_meeting_data.json` - 个人会议安排
- `robot_tasks_simple.json` - 机器人任务数据
- `memory_data.json` - 记忆系统数据
- `simple_memory_data.json` - 简单记忆数据

### 已移动到 {private_dir}/configs/ 的文件：
- `morning_todo.bat` - 包含本地路径的批处理文件
- `start_memory_system.bat` - 包含本地路径的批处理文件

## 📝 示例文件

在项目根目录中，我们创建了以下示例文件：
- `chat_memory_data_EXAMPLE.json` - 对话记忆数据示例
- `daily_todos_EXAMPLE.json` - 待办事项数据示例
- `technical_events_EXAMPLE.json` - 技术事件示例
- `weekly_meeting_data_EXAMPLE.json` - 会议数据示例
- `config_EXAMPLE.json` - 配置文件示例

这些文件展示了数据结构，您可以基于这些示例创建自己的配置文件。

## ⚙️ 代码更新

以下代码文件已更新，现在引用 `{private_dir}/data/` 目录中的文件：
- `daily_todo_system.py`
- `weekly_meeting_system.py`
- `technical_events_recorder.py`
- `view_technical_events.py`
- `record_today_event.py`
- `chat_memory_system.py`
- `memory_system.py`
- `simple_memory_system.py`

## 🚀 使用说明

### 首次使用
1. 检查 `{private_dir}/data/` 目录中的文件是否包含您的实际数据
2. 如果需要，从示例文件复制结构并填入您的数据
3. 运行程序测试是否正常工作

### 开发新功能
1. 如果需要访问私人数据，请使用 `{private_dir}/data/` 路径
2. 在 `.gitignore` 中确保新文件被正确排除
3. 创建示例文件供其他开发者参考

### 备份和恢复
1. 定期备份 `{private_dir}/` 目录
2. `{private_dir}/backups/` 包含原始文件的备份
3. 迁移到新环境时，复制整个 `{private_dir}/` 目录

## 📋 .gitignore 配置

`.gitignore` 文件已配置为排除以下内容：
- 所有私人数据文件
- 批处理文件（包含本地路径）
- 日志文件
- 临时文件
- IDE配置文件
- 虚拟环境

## 🔧 故障排除

### 问题：程序找不到数据文件
**解决方案**：检查 `{private_dir}/data/` 目录中是否有对应的文件，如果没有，从示例文件复制

### 问题：批处理文件路径错误
**解决方案**：更新批处理文件中的路径指向您本地的项目目录

### 问题：想要共享配置但不共享数据
**解决方案**：只提交示例文件，让他人基于示例创建自己的配置文件

## 📞 支持

如有问题，请检查：
1. `{private_dir}/` 目录结构是否完整
2. 代码中的文件路径是否正确
3. 示例文件是否可用作参考

---

**重要提示**：`{private_dir}/` 目录中的文件包含您的个人隐私信息，请勿提交到公开仓库或与他人共享。
"""

    with open(guide_path, 'w', encoding='utf-8') as f:
        f.write(guide_content)
    
    print(f"[创建] 使用指南: {guide_path}")
    
    # 创建私人目录说明
    private_readme = private_dir / "README_PRIVATE.md"
    with open(private_readme, 'w', encoding='utf-8') as f:
        f.write(f"""# 私人数据目录

此目录包含个人隐私信息，请勿提交到Git仓库。

## 文件说明

### data/ 目录
- 包含所有个人数据文件
- 这些文件包含您的会议安排、任务历史、技术记录等

### configs/ 目录
- 包含个人配置文件
- 批处理文件包含本地系统路径

### backups/ 目录
- 包含原始文件的备份
- 用于恢复或迁移

### logs/ 目录
- 程序日志文件

## 安全建议

1. **定期备份**：备份整个 `{private_dir}/` 目录
2. **环境迁移**：复制此目录到新环境
3. **隐私保护**：不要将此目录的内容分享给他人
4. **版本控制**：此目录不受Git管理，请自行管理版本

## 恢复步骤

如果意外删除了文件：
1. 检查 `backups/` 目录
2. 从备份恢复文件
3. 或从示例文件重新创建
""")
    
    print(f"[创建] 私人目录说明: {private_readme}")

def main():
    """主函数"""
    print("=" * 60)
    print("[工具] 隐私保护文件迁移工具")
    print("=" * 60)
    
    # 1. 创建私人数据目录结构
    private_dir = create_private_data_structure()
    
    # 2. 识别私人文件
    print("\n[步骤1] 识别私人文件")
    private_files = identify_private_files()
    
    if not private_files:
        print("[信息] 未找到需要移动的私人文件")
        return
    
    # 3. 移动文件到私人目录
    print(f"\n[步骤2] 移动文件到 {private_dir}/data/")
    moved_files = move_files_to_private_dir(private_files, private_dir)
    
    # 4. 更新代码引用
    print(f"\n[步骤3] 更新代码中的文件引用")
    updated_files = update_code_references(private_dir)
    
    # 5. 创建使用指南
    print(f"\n[步骤4] 创建文档和指南")
    create_usage_guide(private_dir)
    
    # 6. 移动批处理文件到configs目录
    print(f"\n[步骤5] 移动批处理文件")
    batch_files = ["morning_todo.bat", "start_memory_system.bat"]
    for batch_file in batch_files:
        source = Path(batch_file)
        if source.exists():
            dest = private_dir / "configs" / batch_file
            shutil.move(str(source), str(dest))
            
            # 创建示例批处理文件
            example_batch = source.with_name(f"{source.stem}_EXAMPLE{source.suffix}")
            with open(example_batch, 'w', encoding='utf-8') as f:
                f.write(f"""@echo off
chcp 65001 > nul
echo 这是一个示例批处理文件
echo 原始文件已移动到 {private_dir}/configs/{batch_file}
echo.
echo 请修改以下路径为您的实际项目路径:
echo cd /d "您的项目路径"
echo python 您的脚本.py
echo.
pause
""")
            print(f"[移动] {batch_file} -> {dest}")
            print(f"[创建] 示例文件: {example_batch}")
    
    # 7. 总结
    print("\n" + "=" * 60)
    print("[完成] 迁移完成!")
    print("=" * 60)
    
    print(f"\n[目录] 已创建的目录:")
    print(f"  - {private_dir}/")
    print(f"  - {private_dir}/data/")
    print(f"  - {private_dir}/configs/")
    print(f"  - {private_dir}/logs/")
    print(f"  - {private_dir}/backups/")
    
    print(f"\n[文件] 已移动的文件 ({len(moved_files)}个):")
    for file in moved_files:
        print(f"  - {file}")
    
    print(f"\n[代码] 已更新的代码文件 ({len(updated_files)}个):")
    for file in updated_files:
        print(f"  - {file}")
    
    print(f"\n[文档] 创建的文档:")
    print(f"  - PRIVACY_SETUP_GUIDE.md")
    print(f"  - {private_dir}/README_PRIVATE.md")
    
    print(f"\n[示例] 创建的示例文件:")
    print(f"  - chat_memory_data_EXAMPLE.json")
    print(f"  - daily_todos_EXAMPLE.json")
    print(f"  - technical_events_EXAMPLE.json")
    print(f"  - weekly_meeting_data_EXAMPLE.json")
    print(f"  - config_EXAMPLE.json")
    print(f"  - morning_todo_EXAMPLE.bat")
    print(f"  - start_memory_system_EXAMPLE.bat")
    
    print(f"\n[安全] .gitignore 已配置:")
    print(f"  - 已排除所有私人数据文件")
    print(f"  - 已排除批处理文件")
    print(f"  - 已配置其他隐私保护规则")
    
    print(f"\n[下一步] 下一步操作:")
    print(f"  1. 检查 {private_dir}/data/ 目录中的文件")
    print(f"  2. 阅读 PRIVACY_SETUP_GUIDE.md 了解详情")
    print(f"  3. 运行程序测试功能是否正常")
    print(f"  4. 现在可以安全地将代码提交到Git仓库")
    
    print(f"\n[提示] 提示:")
    print(f"  - {private_dir}/ 目录不会被Git跟踪")
    print(f"  - 示例文件展示了数据结构")
    print(f"  - 批处理文件需要根据您的环境修改路径")
    print(f"  - 定期备份 {private_dir}/ 目录")

if __name__ == "__main__":
    main()