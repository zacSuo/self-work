# 隐私保护配置指南

## 📋 概述

为了保护您的个人隐私信息，所有包含私人数据的文件都已移动到 `private_data/` 目录。这些文件不会被提交到Git仓库。

## 📁 目录结构

```
private_data/
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

### 已移动到 private_data/data/ 的文件：
- `chat_memory_data.json` - 对话记忆数据
- `daily_todos.json` - 个人待办事项历史
- `technical_events.json` - 技术事件记录
- `weekly_meeting_data.json` - 个人会议安排
- `robot_tasks_simple.json` - 机器人任务数据
- `memory_data.json` - 记忆系统数据
- `simple_memory_data.json` - 简单记忆数据

### 已移动到 private_data/configs/ 的文件：
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

以下代码文件已更新，现在引用 `private_data/data/` 目录中的文件：
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
1. 检查 `private_data/data/` 目录中的文件是否包含您的实际数据
2. 如果需要，从示例文件复制结构并填入您的数据
3. 运行程序测试是否正常工作

### 开发新功能
1. 如果需要访问私人数据，请使用 `private_data/data/` 路径
2. 在 `.gitignore` 中确保新文件被正确排除
3. 创建示例文件供其他开发者参考

### 备份和恢复
1. 定期备份 `private_data/` 目录
2. `private_data/backups/` 包含原始文件的备份
3. 迁移到新环境时，复制整个 `private_data/` 目录

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
**解决方案**：检查 `private_data/data/` 目录中是否有对应的文件，如果没有，从示例文件复制

### 问题：批处理文件路径错误
**解决方案**：更新批处理文件中的路径指向您本地的项目目录

### 问题：想要共享配置但不共享数据
**解决方案**：只提交示例文件，让他人基于示例创建自己的配置文件

## 📞 支持

如有问题，请检查：
1. `private_data/` 目录结构是否完整
2. 代码中的文件路径是否正确
3. 示例文件是否可用作参考

---

**重要提示**：`private_data/` 目录中的文件包含您的个人隐私信息，请勿提交到公开仓库或与他人共享。
