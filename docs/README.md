# 个人记忆系统 (Personal Memory System)

一个用于记录和管理个人习惯、工作方式、决策模式和任务安排的综合记忆系统。

## 功能特性

### 🎯 核心功能
- **习惯管理**: 记录个人习惯，跟踪执行频率和成功率
- **工作方式记录**: 记录个人工作习惯、沟通方式和决策模式
- **决策跟踪**: 实时记录决策过程、结果和经验教训
- **任务安排**: 管理个人任务，跟踪进度和完成情况

### 📊 数据分析
- 习惯执行成功率统计
- 决策结果分析
- 任务完成率跟踪
- 工作方式有效性评估

### 🌐 用户界面
- 响应式Web界面
- 直观的数据可视化
- 快速操作和批量处理
- 实时数据更新

## 快速开始

### 1. 环境要求
- Python 3.7+
- pip 包管理器

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 启动系统
```bash
python run.py
```

### 4. 访问系统
打开浏览器访问: http://localhost:5000

## 系统架构

### 核心模块

#### 1. 记忆系统核心 (`memory_system.py`)
- `HabitRecord`: 习惯记录类
- `WorkStyleRecord`: 工作方式记录类
- `DecisionRecord`: 决策记录类
- `TaskRecord`: 任务记录类
- `MemorySystem`: 主系统类，提供数据管理功能

#### 2. Web界面 (`web_interface.py`)
- Flask Web应用
- RESTful API接口
- 模板渲染系统

#### 3. 数据存储
- JSON文件存储 (`memory_data.json`)
- 自动备份和恢复
- 数据完整性检查

## 使用指南

### 1. 习惯管理
- 添加新习惯，设置执行频率和优先级
- 记录习惯执行情况
- 查看习惯成功率和统计

### 2. 工作方式记录
- 记录个人工作习惯和偏好
- 评估工作方式的有效性
- 跟踪常用工具和技能

### 3. 决策跟踪
- 记录重要决策的背景和过程
- 分析决策结果和经验教训
- 建立个人决策模式库

### 4. 任务安排
- 创建和管理个人任务
- 设置优先级和截止日期
- 跟踪任务进度和完成情况

## API接口

### 数据查询接口
- `GET /api/summary`: 获取系统摘要
- `GET /api/recent_activity`: 获取最近活动

### 数据管理接口
- `POST /add_habit`: 添加习惯
- `POST /update_habit_practice`: 更新习惯实践
- `POST /add_work_style`: 添加工作方式
- `POST /record_decision`: 记录决策
- `POST /add_task`: 添加任务
- `POST /update_task_status`: 更新任务状态

## 数据模型

### 习惯记录 (HabitRecord)
```python
{
    "name": "习惯名称",
    "description": "习惯描述",
    "frequency": "执行频率 (daily/weekly/monthly)",
    "priority": "优先级 (1-10)",
    "created_at": "创建时间",
    "last_practiced": "最后执行时间",
    "success_rate": "成功率 (0-1)"
}
```

### 决策记录 (DecisionRecord)
```python
{
    "decision_type": "决策类型",
    "description": "决策描述",
    "factors_considered": "考虑因素列表",
    "outcome": "决策结果 (positive/negative/neutral)",
    "confidence_level": "信心度 (1-10)",
    "timestamp": "决策时间",
    "lessons_learned": "经验教训"
}
```

## 部署选项

### 本地开发
```bash
python run.py
```

### 生产部署
```bash
# 使用Gunicorn等生产服务器
gunicorn -w 4 -b 0.0.0.0:5000 web_interface:app
```

### Docker部署
```dockerfile
FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "run.py"]
```

## 数据备份

系统数据自动保存在 `memory_data.json` 文件中，建议定期备份此文件。

## 故障排除

### 常见问题

1. **端口占用**
   ```bash
   # 检查端口占用
   netstat -ano | findstr :5000
   # 杀死占用进程
   taskkill /PID <PID> /F
   ```

2. **依赖安装失败**
   ```bash
   # 使用国内镜像源
   pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
   ```

3. **数据文件损坏**
   ```bash
   # 删除损坏的数据文件，系统会自动重建
   rm memory_data.json
   ```

## 贡献指南

欢迎提交Issue和Pull Request来改进这个项目。

## 许可证

MIT License

## 更新日志

### v1.0.0 (2024-03-12)
- 初始版本发布
- 实现核心记忆功能
- 提供Web管理界面
- 支持数据持久化