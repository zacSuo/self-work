#!/usr/bin/env python3
"""
目录结构组织器

将代码按功能和模块分类到不同的目录下，创建清晰的项目结构
"""

import os
import shutil
import json
from pathlib import Path

class DirectoryOrganizer:
    """目录结构组织器"""
    
    def __init__(self):
        self.project_root = os.path.dirname(os.path.abspath(__file__))
        
        # 功能模块分类
        self.module_categories = {
            "core_system": [
                "framework_ui.py",
                "skills_framework.py",
                "start_framework.py",
                "instant_memory_system.py",
                "memory_system.py",
                "simple_memory_system.py"
            ],
            
            "todo_planning": [
                "daily_todo_system.py",
                "integrated_daily_plan.py",
                "quick_daily_plan.py",
                "robot_team_priority_system.py",
                "simple_robot_planner.py",
                "start_robot_planner.py",
                "today_simple_analysis.py",
                "today_tasks_analyzer.py",
                "tomorrow_meeting_plan.py"
            ],
            
            "meeting_management": [
                "daily_meeting_viewer.py",
                "weekly_meeting_overview.py",
                "weekly_meeting_system.py"
            ],
            
            "technical_records": [
                "record_today_event.py",
                "technical_events_recorder.py",
                "view_technical_events.py"
            ],
            
            "chat_memory": [
                "chat_based_processor.py",
                "chat_memory_system.py"
            ],
            
            "privacy_tools": [
                "check_file_refs.py",
                "check_privacy.py",
                "move_private_files.py",
                "private_data_rule_checker.py",
                "test_privacy_config.py",
                "final_git_check.py"
            ],
            
            "interface_tools": [
                "web_interface.py",
                "run.py"
            ]
        }
        
        # 目录映射
        self.directories = [
            "core_system",     # 核心系统
            "todo_planning",   # 待办事项规划
            "meeting_management",  # 会议管理
            "technical_records",    # 技术记录
            "chat_memory",          # 对话记忆
            "privacy_tools",   # 隐私工具
            "interface_tools",  # 界面工具
            "templates",       # HTML模板（保持不变）
            "skills",          # 技能模块（保持不变）
            "private_data",    # 私人数据（保持不变）
            "docs",            # 文档文件
            "examples"         # 示例文件
        ]
    
    def organize_directories(self):
        """组织目录结构"""
        print("=" * 60)
        print("[系统] 目录结构重组器")
        print("=" * 60)
        
        # 创建所有目录
        for dir_name in self.directories:
            dir_path = os.path.join(self.project_root, dir_name)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
                print(f"[创建] 创建目录: {dir_name}")
        
        # 移动文件到对应的目录
        moved_files = []
        
        # 首先移动示例文件和文档文件
        print("\n[移动] 移动示例文件和文档文件...")
        
        # 示例文件移动到 examples 目录
        example_files = [
            "chat_memory_data_EXAMPLE.json",
            "daily_plan_2026-03-13_EXAMPLE.json",
            "daily_todos_EXAMPLE.json",
            "memory_data_EXAMPLE.json",
            "robot_tasks_simple_EXAMPLE.json",
            "simple_memory_data_EXAMPLE.json",
            "technical_events_EXAMPLE.json",
            "weekly_meeting_data_EXAMPLE.json",
            "morning_todo_EXAMPLE.bat",
            "start_memory_system_EXAMPLE.bat"
        ]
        
        for file_name in example_files:
            source_path = os.path.join(self.project_root, file_name)
            if os.path.exists(source_path):
                target_path = os.path.join(self.project_root, "examples", file_name)
                shutil.move(source_path, target_path)
                moved_files.append((file_name, "examples"))
                print(f"[移动] {file_name} → examples")
        
        # 文档文件移动到 docs 目录
        doc_files = [
            "README.md",
            "README_GIT.md",
            "PRIVACY_SETUP_GUIDE.md",
            "PRIVATE_DATA_RULE.md"
        ]
        
        for file_name in doc_files:
            source_path = os.path.join(self.project_root, file_name)
            if os.path.exists(source_path):
                target_path = os.path.join(self.project_root, "docs", file_name)
                shutil.move(source_path, target_path)
                moved_files.append((file_name, "docs"))
                print(f"[移动] {file_name} → docs")
        
        # 移动功能模块文件
        print("\n[移动] 移动功能模块文件...")
        
        for module_name, file_list in self.module_categories.items():
            for file_name in file_list:
                source_path = os.path.join(self.project_root, file_name)
                if os.path.exists(source_path):
                    target_path = os.path.join(self.project_root, module_name, file_name)
                    shutil.move(source_path, target_path)
                    moved_files.append((file_name, module_name))
                    print(f"[移动] {file_name} → {module_name}")
        
        # 配置文件处理
        print("\n[处理] 配置文件处理...")
        
        # config.json 移动到 core_system 目录
        config_file = "config.json"
        source_path = os.path.join(self.project_root, config_file)
        if os.path.exists(source_path):
            target_path = os.path.join(self.project_root, "core_system", config_file)
            shutil.move(source_path, target_path)
            moved_files.append((config_file, "core_system"))
            print(f"[移动] {config_file} → core_system")
        
        # requirements.txt 移动到 docs 目录
        req_file = "requirements.txt"
        source_path = os.path.join(self.project_root, req_file)
        if os.path.exists(source_path):
            target_path = os.path.join(self.project_root, "docs", req_file)
            shutil.move(source_path, target_path)
            moved_files.append((req_file, "docs"))
            print(f"[移动] {req_file} → docs")
        
        # .gitignore 保持不变在根目录
        
        # 更新文件引用
        print("\n[更新] 更新文件引用...")
        self.update_file_references(moved_files)
        
        # 更新概述文档
        print("\n[更新] 更新概述文档...")
        self.update_overview_document(moved_files)
        
        # 总结
        print("\n" + "=" * 60)
        print("[完成] 目录结构重组完成")
        print("=" * 60)
        
        print(f"[统计] 移动了 {len(moved_files)} 个文件")
        for file_name, target_dir in moved_files:
            print(f"  - {file_name} → {target_dir}")
        
        print("\n[结构] 新目录结构:")
        for dir_name in self.directories:
            dir_path = os.path.join(self.project_root, dir_name)
            files_count = len([f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))])
            print(f"  {dir_name}: {files_count} 个文件")
    
    def update_file_references(self, moved_files):
        """更新文件引用路径"""
        # 创建文件映射关系
        file_map = {}
        for file_name, target_dir in moved_files:
            if file_name.endswith(".py"):
                old_path = os.path.join(self.project_root, file_name)
                new_path = os.path.join(self.project_root, target_dir, file_name)
                file_map[file_name] = (old_path, new_path)
        
        # 检查Python文件中的引用
        for module_name, file_list in self.module_categories.items():
            for file_name in file_list:
                file_path = os.path.join(self.project_root, module_name, file_name)
                if os.path.exists(file_path):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        # 检查是否有对其他文件的引用
                        updated_content = content
                        
                        # 更新 import 语句
                        for referenced_file, (old_path, new_path) in file_map.items():
                            # 检查是否有直接引用该文件的代码
                            if referenced_file in content:
                                # 如果是 import 语句
                                if f"import {referenced_file.replace('.py', '')}" in content:
                                    # 更新 import 路径
                                    old_import = f"import {referenced_file.replace('.py', '')}"
                                    new_import = f"from {file_map[referenced_file][1].replace('.py', '')} import {referenced_file.replace('.py', '')}"
                                    updated_content = updated_content.replace(old_import, new_import)
                                
                                # 如果是相对路径引用
                                if f"{referenced_file}" in content and not f"{module_name}/{referenced_file}" in content:
                                    # 需要检查具体情况
                                    pass
                        
                        # 如果有修改，写入文件
                        if updated_content != content:
                            with open(file_path, 'w', encoding='utf-8') as f:
                                f.write(updated_content)
                            print(f"[更新] 更新了 {file_name} 中的引用")
                    except Exception as e:
                        print(f"[警告] 更新 {file_name} 时出错: {e}")
    
    def update_overview_document(self, moved_files):
        """更新概述文档"""
        overview_path = "c:\\Users\\IWITH\\AppData\\Roaming\\WorkBuddy\\User\\globalStorage\\tencent-cloud.coding-copilot\\brain\\628c6c1bca454da4bc4be3fe74d88496\\overview.md"
        
        try:
            # 读取现有概述文档
            if os.path.exists(overview_path):
                with open(overview_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 添加目录结构信息
                new_content = content + "\n\n## 📁 目录结构重组完成\n\n"
                
                # 新目录结构
                new_content += "### 功能模块分类\n"
                
                for module_name, file_list in self.module_categories.items():
                    dir_path = os.path.join(self.project_root, module_name)
                    if os.path.exists(dir_path):
                        files_in_dir = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
                        new_content += f"\n**{module_name}** (`{module_name}/`):\n"
                        new_content += f"- 文件数量: {len(files_in_dir)}\n"
                        new_content += f"- 主要功能: "
                        if module_name == "core_system":
                            new_content += "核心系统框架和技能管理\n"
                        elif module_name == "todo_planning":
                            new_content += "待办事项规划和管理\n"
                        elif module_name == "meeting_management":
                            new36:"技术事件记录和管理\n"
                        elif module_name == "chat_memory":
                            new_content += "对话记忆系统\n"
                        elif module_name == "privacy_tools":
                            new_content += "隐私保护和文件管理工具\n"
                        elif module_name == "interface_tools":
                            new_content += "Web界面和运行脚本\n"
                
                # 其他目录
                new_content += "\n### 其他目录\n"
                for dir_name in ["docs", "examples", "templates", "skills", "private_data"]:
                    dir_path = os.path.join(self.project_root, dir_name)
                    if os.path.exists(dir_path):
                        files_in_dir = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
                        new_content += f"\n**{dir_name}** (`{dir_name}/`):\n"
                        new_content += f"- 文件数量: {len(files_in_dir)}\n"
                        new_content += f"- 用途: "
                        if dir_name == "docs":
                            new_content += "文档和README文件\n"
                        elif dir_name == "examples":
                            new_content += "示例文件和配置\n"
                        elif dir_name == "templates":
                            new_content += "HTML模板文件\n"
                        elif dir_name == "skills":
                            new_content += "技能模块代码\n"
                        elif dir_name == "private_data":
                            new_content += "私人数据和配置文件\n"
                
                # 移动文件统计
                new_content += "\n### 文件移动统计\n"
                new_content += f"- 总共移动了 {len(moved_files)} 个文件\n"
                
                # 按目录统计
                dir_stats = {}
                for file_name, target_dir in moved_files:
                    if target_dir not in dir_stats:
                        dir_stats[target_dir] = []
                    dir_stats[target_dir].append(file_name)
                
                for target_dir, files in dir_stats.items():
                    new_content += f"\n**{target_dir}**:\n"
                    for file_name in files:
                        new_content += f"- {file_name}\n"
                
                # 写入更新后的概述文档
                with open(overview_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print(f"[更新] 概述文档已更新: {overview_path}")
            
        except Exception as e:
            print(f"[错误] 更新概述文档时出错: {e}")
    
    def create_directory_guide(self):
        """创建目录结构指南"""
        guide_path = os.path.join(self.project_root, "docs", "DIRECTORY_GUIDE.md")
        
        guide_content = """# 📁 目录结构指南

## 项目结构

```
workbuddy/
├── core_system/           # 核心系统框架
├── todo_planning/         # 待办事项规划系统
├── meeting_management/    # 会议管理系统
├── technical_records/     # 技术记录系统
├── chat_memory/           # 对话记忆系统
├── privacy_tools/         # 隐私保护工具
├── interface_tools/       # Web界面和运行脚本
├── docs/                  # 文档文件
├── examples/              # 示例文件
├── templates/             # HTML模板
├── skills/                # 技能模块
├── private_data/          # 私人数据目录
├── .gitignore             # Git排除规则
└── directory_organizer.py # 目录组织工具
```

## 各目录说明

### core_system/
核心系统框架和技能管理模块
```
├── framework_ui.py        # 框架UI界面
├── skills_framework.py    # 技能框架系统
├── start_framework.py     # 框架启动脚本
├── instant_memory_system.py # 即时记忆系统
├── memory_system.py       # 记忆系统
├── simple_memory_system.py # 简单记忆系统
├── config.json           # 系统配置文件
```

### todo_planning/
待办事项规划和管理系统
```
├── daily_todo_system.py       # 每日待办事项系统
├── integrated_daily_plan.py    # 集成每日计划
├── quick_daily_plan.py         # 快速每日计划
├── robot_team_priority_system.py # 机器人团队优先级系统
├── simple_robot_planner.py     # 简单机器人规划器
├── start_robot_planner.py       # 机器人规划器启动脚本
├── today_simple_analysis.py    # 今日简单分析
├── today_tasks_analyzer.py     # 今日任务分析器
├── tomorrow_meeting_plan.py    # 明日会议计划
```

### meeting_management/
会议管理系统
```
├── daily_meeting_viewer.py    # 每日会议查看器
├── weekly_meeting_overview.py  # 每周会议概览
├── weekly_meeting_system.py    # 每周会议系统
```

### technical_records/
技术记录系统
```
├── record_today_event.py      # 记录今日事件
├── technical_events_recorder.py # 技术事件记录器
├── view_technical_events.py   # 查看技术事件
```

### chat_memory/
对话记忆系统
```
├── chat_based_processor.py    # 基于对话的处理器
├── chat_memory_system.py      # 对话记忆系统
```

### privacy_tools/
隐私保护工具
```
├── check_file_refs.py         # 检查文件引用
├── check_privacy.py           # 检查隐私配置
├── move_private_files.py      # 移动私人文件
├── private_data_rule_checker.py # 私人数据规则检查器
├── test_privacy_config.py     # 测试隐私配置
├── final_git_check.py         # 最终Git检查
```

### interface_tools/
Web界面和运行脚本
```
├── web_interface.py           # Web界面
├── run.py                     # 运行脚本
```

### docs/
文档文件
```
├── README.md                  # 项目README
├── README_GIT.md             # Git上传指南
├── PRIVACY_SETUP_GUIDE.md    # 隐私配置指南
├── PRIVATE_DATA_RULE.md      # 私人数据规则
├── DIRECTORY_GUIDE.md        # 目录结构指南
├── requirements.txt          # 依赖文件
```

### examples/
示例文件和配置
```
├── chat_memory_data_EXAMPLE.json       # 对话记忆示例数据
├── daily_plan_2026-03-13_EXAMPLE.json   # 每日计划示例
├── daily_todos_EXAMPLE.json            # 每日待办事项示例
├── memory_data_EXAMPLE.json            # 记忆数据示例
├── robot_tasks_simple_EXAMPLE.json     # 机器人任务示例
├── simple_memory_data_EXAMPLE.json     # 简单记忆数据示例
├── technical_events_EXAMPLE.json       # 技术事件示例
├── weekly_meeting_data_EXAMPLE.json   # 每周会议数据示例
├── morning_todo_EXAMPLE.bat            # 早上待办示例脚本
├── start_memory_system_EXAMPLE.bat     # 启动记忆系统示例脚本
```

### templates/
HTML模板
```
├── template.html             # HTML模板文件
```

### skills/
技能模块
```
├── ...                       # 技能模块代码
```

### private_data/
私人数据目录（不会被Git跟踪）
```
├── data/                     # 个人数据文件
├── configs/                  # 个人配置文件
├── logs/                     # 个人日志文件
├── backups/                  # 备份文件
├── notes/                    # 个人笔记
├── README_PRIVATE.md         # 私人数据说明
```

## 使用规则

### 1. 新文件创建规则
- **核心系统代码** → 放在 `core_system/` 目录
- **待办事项代码** → 放在 `todo_planning/` 目录
- **会议管理代码** → 放在 `meeting_management/` 目录
- **技术记录代码** → 放在 `technical_records/` 目录
- **隐私保护代码** → 放在 `privacy_tools/` 目录
- **界面工具代码** → 放在 `interface_tools/` 目录
- **文档文件** → 放在 `docs/` 目录
- **示例文件** → 放在 `examples/` 目录

### 2. 私人数据规则
- **所有个人数据** → 放在 `private_data/data/` 目录
- **所有配置文件** → 放在 `private_data/configs/` 目录
- **所有日志文件** → 放在 `private_data/logs/` 目录
- **所有备份文件** → 放在 `private_data/backups/` 目录

### 3. Git提交规则
- 不要提交 `private_data/` 目录下的任何文件
- 提交示例文件和文档文件
- 使用示例文件展示数据结构
- 使用个人数据文件存储实际信息

## 维护指南

### 添加新模块
1. 首先确定模块类型
2. 将文件放在对应的目录中
3. 更新 `directory_organizer.py` 中的分类
4. 更新 `DIRECTORY_GUIDE.md` 文档

### 更新目录结构
运行目录组织工具：
```bash
python directory_organizer.py
```

### 检查目录结构
查看当前目录结构：
```bash
python -c "import os; print('\\n目录结构:'); for d in os.listdir('.'): if os.path.isdir(d): print(f'{d}: {len([f for f in os.listdir(d)])} 个文件')"
```
"""
        
        with open(guide_path, 'w', encoding='utf-8') as f:
            f.write(guide_content)
        
        print(f"[创建] 目录结构指南已创建: {guide_path}")
    
    def main(self):
        """主函数"""
        print("=" * 60)
        print("[系统] 目录结构重组开始")
        print("=" * 60)
        
        # 1. 组织目录结构
        self.organize_directories()
        
        # 2. 创建目录指南
        self.create_directory_guide()
        
        # 3. 更新.gitignore添加新目录
        self.update_gitignore_for_new_dirs()
        
        print("\n[完成] 目录重组完成")
        print("\n[下一步] 建议操作:")
        print("1. 检查新目录结构")
        print("2. 运行程序验证功能")
        print("3. 使用目录结构指南维护项目")
    
    def update_gitignore_for_new_dirs(self):
        """更新.gitignore添加新目录的排除规则"""
        gitignore_path = os.path.join(self.project_root, ".gitignore")
        
        try:
            with open(gitignore_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 添加新目录的排除规则
            new_dirs_to_exclude = [
                "private_data/",
                "__pycache__/"
            ]
            
            # 确保这些目录已被排除
            for dir_to_exclude in new_dirs_to_exclude:
                if dir_to_exclude not in content:
                    # 找到合适的位置添加
                    if "# 操作系统文件" in content:
                        lines = content.split('\n')
                        for i, line in enumerate(lines):
                            if line.startswith("# 操作系统文件"):
                                lines.insert(i + 2, dir_to_exclude)
                                content = '\n'.join(lines)
                                break
            
            # 写入更新后的.gitignore
            with open(gitignore_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("[更新] .gitignore已更新，添加了新目录排除规则")
        
        except Exception as e:
            print(f"[错误] 更新.gitignore时出错: {e}")

if __name__ == "__main__":
    organizer = DirectoryOrganizer()
    organizer.main()