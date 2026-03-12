# 私人数据存储规则

## 规则定义

### 1. 什么是私人信息？

私人信息包括**所有与我个人工作和生活有关的具体信息**，不仅仅是账号密码等敏感信息，还包括：

1. **个人信息**
   - 姓名、联系方式、地址
   - 个人习惯、偏好、日程安排
   - 个人笔记、思考记录

2. **工作信息**
   - 具体的工作内容、项目细节
   - 会议时间、会议内容、参会人员
   - 任务安排、工作计划、进度跟踪
   - 团队信息、同事信息

3. **系统配置信息**
   - 本地路径信息（C:\Users\IWITH\...等）
   - 本地配置信息
   - 本地环境信息

4. **历史记录信息**
   - 工作历史记录
   - 学习历史记录
   - 项目历史记录

### 2. 存储规则

**所有包含私人信息的文件和数据必须存储在 `private_data/` 目录下。**

#### 目录结构
```
private_data/
├── data/           # 个人数据文件（JSON格式）
├── configs/        # 个人配置文件（.json, .bat, .py等）
├── logs/           # 个人日志文件
├── backups/        # 备份文件
├── notes/          # 个人笔记
└── README_PRIVATE.md # 私人数据说明
```

#### 文件命名约定
1. **个人数据文件**：使用 `.personal.json`、`.work.json`、`.meeting.json`、`.todo.json` 后缀
2. **配置文件**：使用 `.local.json`、`.user.json` 后缀
3. **批处理文件**：所有包含本地路径的批处理文件

### 3. 操作规则

#### 创建新文件时
1. **检查文件内容**：判断是否包含私人信息
2. **判断文件类型**：
   - 如果包含个人数据 → 保存到 `private_data/data/`
   - 如果是个人配置 → 保存到 `private_data/configs/`
   - 如果是个人日志 → 保存到 `private_data/logs/`
3. **记录操作**：在 `private_data/README_PRIVATE.md` 中记录新增文件

#### 修改现有文件时
1. **检查文件位置**：如果文件在根目录但包含私人信息 → 移动到 `private_data/`
2. **更新代码引用**：更新Python代码中的文件路径引用
3. **更新.gitignore**：确保新类型的私人文件被排除

### 4. 代码引用规则

#### Python代码中引用私人数据
```python
# 正确的方式：引用 private_data 目录下的文件
PRIVATE_DATA_DIR = "private_data/data/"
daily_todos_path = f"{PRIVATE_DATA_DIR}daily_todos.json"
weekly_meeting_path = f"{PRIVATE_DATA_DIR}weekly_meeting_data.json"

# 错误的方式：直接引用根目录的文件（会导致隐私泄露）
daily_todos_path = "daily_todos.json"  # ❌ 错误
weekly_meeting_path = "weekly_meeting_data.json"  # ❌ 错误
```

#### 示例文件模式
1. 创建 `example_todos.json` 在根目录（用于展示数据结构）
2. 创建 `daily_todos.json` 在 `private_data/data/`（实际的个人数据）
3. 代码使用示例文件路径作为默认值，但可以切换到私人数据路径

### 5. 验证规则

每次任务完成后，必须执行以下验证：

1. **检查.gitignore**：确保所有私人文件类型已被排除
2. **检查private_data目录**：确保所有私人数据文件已正确存放
3. **检查代码引用**：确保代码引用正确的路径
4. **运行验证脚本**：运行 `check_privacy.py` 验证隐私保护完整性

### 6. 紧急情况处理

#### 如果误提交了私人文件
1. **立即删除提交**：`git rm --cached <file>`
2. **移动文件到private_data**：`mv <file> private_data/data/`
3. **更新.gitignore**：添加对应的文件类型规则
4. **重新提交**：确保.gitignore生效

#### 如果私人数据泄露
1. **立即停止推送**：暂停所有Git操作
2. **删除远程文件**：从远程仓库删除泄露的文件
3. **更新本地配置**：确保.gitignore包含泄露的文件类型
4. **重建信任**：创建新的私人数据目录，重新组织数据

## 强制执行机制

### 1. 代码检查脚本
- 每次任务后运行 `check_file_refs.py`
- 检查是否有直接引用私人文件的代码
- 自动修复发现的隐私风险

### 2. Git提交前检查
- 运行 `final_git_check.py` 在提交前
- 确保没有私人文件被添加到git
- 确保.gitignore配置完整

### 3. 自动化规则执行
- 创建新文件时自动检查内容
- 如果包含私人信息，自动保存到 `private_data/`
- 自动更新代码引用和.gitignore

## 示例

### 示例1：创建新的个人任务记录
```python
# 创建文件时
def create_personal_task_record():
    # 数据包含个人任务安排和完成情况
    personal_data = {
        "name": "张三",  # 私人信息
        "tasks": ["完成项目A", "参加会议B"],  # 工作信息
        "schedule": {"time": "09:00", "location": "办公室"}  # 个人安排
    }
    
    # 正确：保存到 private_data/data/
    save_path = "private_data/data/personal_tasks.json"
    with open(save_path, 'w') as f:
        json.dump(personal_data, f)
    
    # 同时创建示例文件（不含私人信息）
    example_data = {
        "name": "示例用户",
        "tasks": ["示例任务1", "示例任务2"],
        "schedule": {"time": "示例时间", "location": "示例地点"}
    }
    with open("personal_tasks_EXAMPLE.json", 'w') as f:
        json.dump(example_data, f)
```

### 示例2：修改现有代码引用
```python
# 原代码
def load_daily_todos():
    with open("daily_todos.json", 'r') as f:
        return json.load(f)

# 修改后
def load_daily_todos():
    # 检查是否存在私人数据版本
    private_path = "private_data/data/daily_todos.json"
    example_path = "daily_todos_EXAMPLE.json"
    
    if os.path.exists(private_path):
        with open(private_path, 'r') as f:
            return json.load(f)
    else:
        # 使用示例数据（默认情况）
        with open(example_path, 'r') as f:
            return json.load(f)
```

## 总结

**核心原则：**
- 所有私人信息 → `private_data/`
- 所有示例信息 → 根目录
- 所有代码引用 → 动态检查路径
- 所有Git提交 → 排除私人文件

**检查清单：**
1. 创建文件时检查内容
2. 修改文件时检查位置
3. 提交代码时检查.gitignore
4. 任务完成后验证隐私保护