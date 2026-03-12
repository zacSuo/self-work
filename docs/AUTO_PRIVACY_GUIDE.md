# 🔒 自动隐私保护系统使用指南

## 概述

自动隐私保护系统确保您在项目中创建的任何包含个人信息的文件都会被自动移动到 `private_data/` 目录，同时创建示例文件供Git提交。系统强制执行隐私保护规则，确保您的个人数据不会被提交到公开Git仓库。

## 核心组件

### 1. 隐私规则定义文件 (`docs/PRIVATE_DATA_RULE.md`)
- **定义什么是私人信息**：姓名、工作内容、会议时间、具体任务等
- **规定存储位置**：所有私人数据必须存储在 `private_data/` 目录
- **提供操作指南**：创建、修改、验证文件的方法

### 2. 自动隐私保护强制执行器 (`auto_privacy_enforcer.py`)
- **实时监控新文件**：检查每个新创建的文件
- **自动移动私人文件**：将私人数据移动到 `private_data/`
- **创建示例文件**：创建不含私人信息的示例文件
- **更新.gitignore**：自动添加排除规则

### 3. 目录组织器 (`directory_organizer.py`)
- **结构化项目布局**：按功能和模块分类文件
- **统一文件管理**：确保文件存放在正确的目录
- **创建目录指南**：提供完整的项目结构说明

### 4. 隐私检查工具 (`privacy_tools/`)
- `private_data_rule_checker.py` - 检查隐私规则完整性
- `check_privacy.py` - 验证隐私配置
- `check_file_refs.py` - 检查文件引用
- `final_git_check.py` - 最终Git检查
- `test_privacy_config.py` - 测试配置

## 使用流程

### 1. 创建新文件时的自动化流程
```python
# 当您创建新文件时，自动隐私保护系统会执行以下步骤：

1. **检查文件内容**
   - 检查文件名后缀（如.personal.json, .work.json）
   - 检查内容中的私人信息关键词
   - 检查JSON字段中的个人信息

2. **自动分类和处理**
   - 如果是私人文件 → 移动到 private_data/ 目录
   - 如果是配置文件 → 移动到 private_data/configs/
   - 如果是日志文件 → 移动到 private_data/logs/

3. **创建示例文件**
   - 创建不含私人信息的示例文件
   - 放在 examples/ 目录中
   - 示例文件可提交到Git仓库

4. **更新.gitignore**
   - 添加对应文件的排除规则
   - 确保私人文件不会被Git跟踪

5. **更新规则文档**
   - 记录文件处理过程
   - 更新 PRIVATE_DATA_RULE.md
```

### 2. 如何手动运行隐私检查
```bash
# 检查所有已存在的文件
python auto_privacy_enforcer.py

# 监控新创建的文件
python auto_privacy_enforcer.py

# 运行目录组织器
python directory_organizer.py

# 运行隐私检查器
python privacy_tools/private_data_rule_checker.py
```

### 3. 在代码中集成自动隐私保护
```python
# 在您的代码中添加以下功能：

import auto_privacy_enforcer
from auto_privacy_enforcer import AutoPrivacyEnforcer

def create_file_with_privacy_check(file_path, content):
    """
    创建文件时自动检查隐私信息
    
    Args:
        file_path: 文件路径
        content: 文件内容
        
    Returns:
        str: 实际的文件路径（可能是移动到private_data后的路径）
    """
    enforcer = AutoPrivacyEnforcer()
    result = enforcer.enforce_privacy(file_path)
    
    if result["action"] == "moved":
        # 文件已被移动到private_data目录
        return result["new_path"]
    else:
        # 文件不含私人信息，保持在原位置
        return file_path

# 使用示例
data = {
    "name": "张三",  # 私人信息
    "tasks": ["优化算法", "参加会议"],  # 个人任务
    "schedule": {"time": "9:00", "location": "办公室"}  # 个人日程
}

# 创建文件时自动隐私保护
actual_path = create_file_with_privacy_check("my_schedule.json", json.dumps(data))
print(f"文件实际保存位置: {actual_path}")
```

## 目录结构

### 项目根目录结构
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
├── private_data/          # 🔒 私人数据目录（Git排除）
├── auto_privacy_enforcer.py  # 自动隐私保护器
├── directory_organizer.py     # 目录组织器
├── .gitignore             # Git排除规则
└── README.md              # 项目说明
```

### 私人数据目录结构
```
private_data/              # 🔒 不会被Git跟踪
├── data/                  # 个人数据文件
│   ├── chat_memory_data.json      # 对话记忆数据
│   ├── daily_todos.json            # 每日待办事项
│   ├── technical_events.json       # 技术事件记录
│   ├── weekly_meeting_data.json    # 每周会议数据
│   └── ...                         # 其他个人数据
├── configs/               # 个人配置文件
│   ├── morning_todo.bat           # 早上待办批处理
│   ├── start_memory_system.bat    # 启动记忆系统批处理
│   └── ...                         # 其他配置文件
├── logs/                  # 个人日志文件
│   ├── privacy_check.json         # 隐私检查记录
│   ├── enforcement_results.json   # 强制执行记录
│   └── ...                         # 其他日志
├── backups/              # 备份文件
├── notes/               # 个人笔记
└── README_PRIVATE.md    # 私人数据说明
```

### 示例文件目录结构
```
examples/                 # 示例文件（可提交到Git）
├── chat_memory_data_EXAMPLE.json      # 对话记忆示例
├── daily_todos_EXAMPLE.json           # 每日待办示例
├── technical_events_EXAMPLE.json      # 技术事件示例
├── weekly_meeting_data_EXAMPLE.json   # 每周会议示例
├── morning_todo_EXAMPLE.bat           # 批处理示例
├── start_memory_system_EXAMPLE.bat    # 启动脚本示例
└── ...                                # 其他示例文件
```

## 代码集成示例

### 1. 智能文件创建函数
```python
def smart_file_create(file_name, content):
    """
    智能创建文件，自动处理隐私保护
    
    Args:
        file_name: 文件名
        content: 文件内容
        
    Returns:
        dict: 创建结果信息
    """
    # 创建原始文件
    original_path = os.path.join(os.getcwd(), file_name)
    with open(original_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # 自动隐私保护检查
    enforcer = AutoPrivacyEnforcer()
    result = enforcer.enforce_privacy(original_path)
    
    return result

# 使用示例
result = smart_file_create("my_personal_data.json", json.dumps({
    "name": "张三",
    "work_schedule": "9:00-12:00, 13:30-18:00"
}))

if result["action"] == "moved":
    print(f"私人文件已自动移动到: {result['new_path']}")
    print(f"示例文件已创建在: {result['example_path']}")
```

### 2. 智能文件读取函数
```python
def smart_file_read(file_name):
    """
    智能读取文件，优先读取私人数据，否则读取示例数据
    
    Args:
        file_name: 文件名
        
    Returns:
        dict: 文件数据
    """
    # 检查私人数据目录
    private_path = os.path.join("private_data", "data", file_name)
    example_path = os.path.join("examples", f"{file_name}_EXAMPLE")
    
    if os.path.exists(private_path):
        # 读取私人数据
        with open(private_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    elif os.path.exists(example_path):
        # 读取示例数据
        with open(example_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        # 返回默认数据
        return {"error": "文件不存在"}
```

### 3. 代码模板生成函数
```python
def generate_code_template(file_name, data_type):
    """
    生成代码模板，包含智能隐私保护
    
    Args:
        file_name: 文件名
        data_type: 数据类型
        
    Returns:
        str: Python代码模板
    """
    templates = {
        "personal_data": """
# 创建个人数据文件
data = {
    "name": "张三",  # 姓名信息
    "work_info": "具体工作内容",  # 工作信息
    "schedule": "工作时间安排"  # 日程信息
}

# 使用智能文件创建函数
result = smart_file_create("{file_name}", json.dumps(data))

# 检查结果
if result["action"] == "moved":
    print("文件已自动保护")
else:
    print("文件无需特殊保护")
""",
        
        "work_data": """
# 创建工作数据文件
work_data = {
    "project_name": "项目名称",
    "tasks": ["任务1", "任务2"],
    "meetings": ["会议1", "会议2"]
}

# 使用智能文件创建
result = smart_file_create("{file_name}", json.dumps(work_data))

# 文件将被自动检查和处理
""",
        
        "config_file": """
# 创建配置文件
config = {
    "local_path": "C:/Users/IWITH/...",
    "workspace": "D:/code/workbuddy",
    "settings": {"option1": "value1"}
}

# 配置文件会自动移动到private_data/configs/
result = smart_file_create("{file_name}", json.dumps(config))

# 示例文件将保留在原目录
"""
    }
    
    template = templates.get(data_type, templates["personal_data"])
    return template.replace("{file_name}", file_name)
```

## 最佳实践

### 1. 文件命名规范
- **个人数据文件**：使用 `.personal.json` 后缀
- **工作数据文件**：使用 `.work.json` 后缀
- **配置文件**：使用 `.local.json` 或 `.config.json` 后缀
- **示例文件**：使用 `.json_EXAMPLE` 后缀

### 2. 文件内容规范
- **示例文件**：使用"示例_"前缀替换个人信息
- **个人数据**：保存在 `private_data/data/` 目录
- **配置文件**：保存在 `private_data/configs/` 目录
- **日志文件**：保存在 `private_data/logs/` 目录

### 3. Git提交规范
- **提交示例文件**：所有示例文件可提交
- **排除私人数据**：所有 `private_data/` 目录下的文件不提交
- **检查.gitignore**：每次提交前检查.gitignore是否完整

### 4. 开发流程规范
- **创建文件** → 使用智能文件创建函数
- **读取文件** → 使用智能文件读取函数
- **移动文件** → 使用自动隐私保护器
- **提交代码** → 运行最终Git检查

## 集成到现有系统

### 1. 每日待办事项系统集成
```python
# 修改 daily_todo_system.py 中的文件读取部分

def load_daily_todos():
    """
    智能加载每日待办事项
    """
    # 优先读取私人数据
    private_path = "private_data/data/daily_todos.json"
    example_path = "examples/daily_todos_EXAMPLE.json"
    
    if os.path.exists(private_path):
        with open(private_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        # 使用示例数据
        with open(example_path, 'r', encoding='utf-8') as f:
            return json.load(f)
```

### 2. 会议管理系统集成
```python
# 修改 weekly_meeting_system.py 中的文件读取部分

def load_weekly_meetings():
    """
    智能加载每周会议数据
    """
    # 优先读取私人数据
    private_path = "private_data/data/weekly_meeting_data.json"
    example_path = "examples/weekly_meeting_data_EXAMPLE.json"
    
    if os.path.exists(private_path):
        with open(private_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        # 使用示例数据
        with open(example_path, 'r', encoding='utf-8') as f:
            return json.load(f)
```

### 3. 技术事件记录器集成
```python
# 修改 technical_events_recorder.py 中的文件写入部分

def save_technical_event(event_data):
    """
    智能保存技术事件
    """
    file_name = f"technical_event_{datetime.now().strftime('%Y-%m-%d')}.json"
    
    # 使用智能文件创建
    result = smart_file_create(file_name, json.dumps(event_data))
    
    if result["action"] == "moved":
        print(f"技术事件已保存到: {result['new_path']}")
    else:
        print(f"技术事件已保存到: {result['original_path']}")
```

## 验证和测试

### 1. 运行隐私检查器
```bash
# 全面检查隐私保护配置
python privacy_tools/private_data_rule_checker.py

# 验证目录结构
python auto_privacy_enforcer.py 1

# 最终Git检查
python privacy_tools/final_git_check.py
```

### 2. 测试新文件创建
```bash
# 创建测试文件
python -c "
import json
data = {'name': '张三', 'work': '工程师'}
with open('test_personal.json', 'w') as f:
    json.dump(data, f)
"

# 运行隐私保护器
python auto_privacy_enforcer.py 3 test_personal.json
```

### 3. 验证Git排除规则
```bash
# 检查.gitignore配置
python -c "
with open('.gitignore', 'r') as f:
    rules = f.readlines()
    
print('已排除的文件类型:')
for rule in rules:
    if rule.strip() and not rule.startswith('#'):
        print(f'  - {rule.strip()}')
"
```

## 故障排除

### 问题1：文件未被自动移动
**原因**：文件内容不包含定义的私人信息关键词
**解决方法**：
- 检查文件内容是否包含个人信息
- 更新 `auto_privacy_enforcer.py` 中的关键词列表
- 运行 `python auto_privacy_enforcer.py 1` 检查所有文件

### 问题2：示例文件未创建
**原因**：`examples/` 目录不存在或权限不足
**解决方法**：
- 创建 `examples/` 目录：`mkdir examples`
- 检查目录权限
- 运行目录组织器：`python directory_organizer.py`

### 问题3：.gitignore未更新
**原因**：.gitignore文件格式错误或关键词未匹配
**解决方法**：
- 检查.gitignore文件格式
- 手动添加排除规则
- 运行隐私检查器验证配置

### 问题4：代码引用错误
**原因**：文件移动后代码引用未更新
**解决方法**：
- 使用智能文件读取函数
- 更新代码引用路径
- 运行 `python privacy_tools/check_file_refs.py` 检查引用

## 总结

自动隐私保护系统确保：
- **所有个人数据**自动保存到 `private_data/` 目录
- **所有示例文件**自动创建在 `examples/` 目录
- **所有Git提交**自动排除私人数据
- **所有代码引用**自动适应路径变化

### 关键优势
1. **自动化**：无需手动处理隐私保护
2. **统一性**：统一的目录结构和命名规范
3. **安全性**：确保个人数据不被泄露
4. **可维护性**：清晰的目录结构和文档

### 使用方法
- 创建新文件 → 自动隐私保护
- 读取文件 → 智能路径检测
- 提交代码 → 隐私配置验证
- 维护项目 → 目录结构组织

现在您的项目已经具备了完整的自动隐私保护能力，可以安全地提交到公开Git仓库！