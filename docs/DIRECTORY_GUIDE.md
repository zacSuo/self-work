# 📁 目录结构指南

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
python -c "import os; print('\n目录结构:'); for d in os.listdir('.'): if os.path.isdir(d): print(f'{d}: {len([f for f in os.listdir(d)])} 个文件')"
```
