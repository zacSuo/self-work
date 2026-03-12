#!/usr/bin/env python3
"""
机器人研发团队负责人每日任务优先级安排系统
专门为20+人机器人研发团队负责人设计的任务管理工具
结合技术攻关（软硬件/算法/结构）与项目管理双重职责
"""

import json
import os
import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import re

# ==================== 数据模型 ====================

class TaskType(Enum):
    """任务类型枚举"""
    HARDWARE = "硬件技术攻关"           # 硬件相关技术问题
    SOFTWARE = "软件技术攻关"           # 软件架构和开发
    ALGORITHM = "算法研发攻关"          # 算法研究和优化
    STRUCTURE = "结构设计攻关"          # 机械结构设计
    PROJECT_MILESTONE = "项目关键节点"  # 项目里程碑监控
    TEAM_MANAGEMENT = "团队管理"        # 人员、资源、协调
    DECISION_MAKING = "关键决策"        # 重要技术/管理决策
    EXTERNAL_COMM = "外部沟通"          # 客户、供应商、合作方
    RISK_MANAGEMENT = "风险管控"        # 技术风险、进度风险
    INNOVATION = "技术创新探索"         # 新技术调研和预研

class PriorityLevel(Enum):
    """优先级级别"""
    CRITICAL = "关键紧急"      # 必须立即处理，影响全局
    HIGH = "高优先级"         # 当天需要完成
    MEDIUM = "中等优先级"     # 近期需要完成
    LOW = "低优先级"         # 可以安排较晚时间
    BACKLOG = "待办事项"     # 后续安排

@dataclass
class Task:
    """任务数据类"""
    id: str
    title: str
    task_type: TaskType
    priority: PriorityLevel
    description: str
    assigned_to: Optional[str] = None  # 负责的子团队或个人
    estimated_hours: float = 2.0
    deadline: Optional[str] = None
    dependencies: List[str] = None  # 依赖的其他任务ID
    status: str = "pending"  # pending, in_progress, completed, blocked
    created_at: str = None
    completed_at: Optional[str] = None
    progress_percent: int = 0
    difficulty_level: int = 3  # 1-5，难度等级
    impact_level: int = 3      # 1-5，影响范围等级
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []
        if self.created_at is None:
            self.created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def to_dict(self):
        return {
            **asdict(self),
            "task_type": self.task_type.value,
            "priority": self.priority.value
        }

@dataclass
class DailyPlan:
    """每日计划"""
    date: str
    focus_areas: List[str]  # 重点关注领域
    critical_tasks: List[Task]
    daily_tasks: List[Task]
    review_notes: List[str]
    completion_rate: float = 0.0

# ==================== 智能优先级算法 ====================

class RobotTeamPriorityEngine:
    """机器人团队专用优先级引擎"""
    
    def __init__(self):
        # 权重配置：根据团队负责人双重职责调整
        self.weights = {
            "impact_on_project": 0.25,      # 对项目进度的影响
            "technical_risk": 0.20,         # 技术风险程度
            "team_blockers": 0.15,          # 是否阻塞团队
            "external_dependency": 0.10,    # 外部依赖程度
            "innovation_value": 0.10,       # 创新价值
            "stakeholder_concern": 0.10,    # 干系人关注度
            "resource_availability": 0.05,  # 资源可用性
            "time_sensitivity": 0.05        # 时间敏感性
        }
        
        # 任务类型基准分
        self.type_base_scores = {
            TaskType.PROJECT_MILESTONE: 90,
            TaskType.RISK_MANAGEMENT: 85,
            TaskType.TEAM_MANAGEMENT: 80,
            TaskType.HARDWARE: 75,
            TaskType.ALGORITHM: 75,
            TaskType.SOFTWARE: 70,
            TaskType.DECISION_MAKING: 70,
            TaskType.STRUCTURE: 65,
            TaskType.EXTERNAL_COMM: 60,
            TaskType.INNOVATION: 55,
        }
    
    def calculate_priority_score(self, task: Task) -> float:
        """计算任务优先级综合得分"""
        base_score = self.type_base_scores.get(task.task_type, 50)
        
        # 难度调整
        difficulty_adj = task.difficulty_level * 5
        
        # 影响范围调整
        impact_adj = task.impact_level * 8
        
        # 截止日期调整（如果有）
        deadline_adj = 0
        if task.deadline:
            deadline_adj = self._calculate_deadline_urgency(task.deadline)
        
        # 状态调整
        status_adj = 0
        if task.status == "blocked":
            status_adj = 20
        elif task.status == "in_progress":
            status_adj = 10
        
        total_score = base_score + difficulty_adj + impact_adj + deadline_adj + status_adj
        
        # 根据任务类型应用权重
        if task.task_type in [TaskType.PROJECT_MILESTONE, TaskType.RISK_MANAGEMENT]:
            total_score *= 1.2
        elif task.task_type in [TaskType.HARDWARE, TaskType.ALGORITHM]:
            total_score *= 1.1
        
        return min(100, total_score)
    
    def _calculate_deadline_urgency(self, deadline_str: str) -> int:
        """计算截止日期紧急度"""
        try:
            deadline = datetime.datetime.strptime(deadline_str, "%Y-%m-%d")
            today = datetime.datetime.now()
            days_left = (deadline - today).days
            
            if days_left < 0:
                return 30  # 已过期
            elif days_left <= 1:
                return 25  # 今天或明天
            elif days_left <= 3:
                return 20  # 3天内
            elif days_left <= 7:
                return 15  # 一周内
            elif days_left <= 14:
                return 10  # 两周内
            else:
                return 5   # 两周以上
        except:
            return 0
    
    def generate_daily_focus(self, tasks: List[Task]) -> Dict:
        """生成每日重点关注领域"""
        # 按任务类型分组
        type_groups = {}
        for task in tasks:
            task_type = task.task_type.value
            if task_type not in type_groups:
                type_groups[task_type] = []
            type_groups[task_type].append(task)
        
        # 计算每个类型的总分
        type_scores = {}
        for task_type, task_list in type_groups.items():
            total_score = sum(self.calculate_priority_score(task) for task in task_list)
            type_scores[task_type] = total_score / len(task_list)
        
        # 按分数排序
        sorted_types = sorted(type_scores.items(), key=lambda x: x[1], reverse=True)
        
        # 确定今日重点关注领域（前3个）
        daily_focus = []
        for i, (task_type, score) in enumerate(sorted_types[:3]):
            focus_level = "🔴" if i == 0 else "🟡" if i == 1 else "🟢"
            daily_focus.append(f"{focus_level} {task_type} (优先级分: {score:.1f})")
        
        return {
            "daily_focus": daily_focus,
            "type_distribution": type_scores,
            "recommended_focus_ratio": self._recommend_focus_ratio(type_scores)
        }
    
    def _recommend_focus_ratio(self, type_scores: Dict[str, float]) -> Dict[str, float]:
        """推荐每日时间分配比例"""
        total_score = sum(type_scores.values())
        if total_score == 0:
            return {"项目管理": 0.4, "技术攻关": 0.4, "团队管理": 0.2}
        
        # 分类聚合
        project_score = type_scores.get(TaskType.PROJECT_MILESTONE.value, 0) + \
                       type_scores.get(TaskType.RISK_MANAGEMENT.value, 0)
        
        tech_score = type_scores.get(TaskType.HARDWARE.value, 0) + \
                    type_scores.get(TaskType.SOFTWARE.value, 0) + \
                    type_scores.get(TaskType.ALGORITHM.value, 0) + \
                    type_scores.get(TaskType.STRUCTURE.value, 0)
        
        team_score = type_scores.get(TaskType.TEAM_MANAGEMENT.value, 0) + \
                    type_scores.get(TaskType.DECISION_MAKING.value, 0) + \
                    type_scores.get(TaskType.EXTERNAL_COMM.value, 0)
        
        total_categorized = project_score + tech_score + team_score
        
        if total_categorized == 0:
            return {"项目管理": 0.4, "技术攻关": 0.4, "团队管理": 0.2}
        
        return {
            "项目管理": round(project_score / total_categorized, 2),
            "技术攻关": round(tech_score / total_categorized, 2),
            "团队管理": round(team_score / total_categorized, 2)
        }

# ==================== 每日规划生成器 ====================

class DailyPlanner:
    """每日规划生成器"""
    
    def __init__(self, data_file="robot_team_tasks.json"):
        self.data_file = data_file
        self.priority_engine = RobotTeamPriorityEngine()
        self.tasks = self._load_tasks()
    
    def _load_tasks(self) -> List[Task]:
        """加载任务数据"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                tasks = []
                for task_data in data.get("tasks", []):
                    try:
                        task = Task(
                            id=task_data["id"],
                            title=task_data["title"],
                            task_type=TaskType(task_data["task_type"]),
                            priority=PriorityLevel(task_data["priority"]),
                            description=task_data["description"],
                            assigned_to=task_data.get("assigned_to"),
                            estimated_hours=task_data.get("estimated_hours", 2.0),
                            deadline=task_data.get("deadline"),
                            dependencies=task_data.get("dependencies", []),
                            status=task_data.get("status", "pending"),
                            created_at=task_data.get("created_at"),
                            completed_at=task_data.get("completed_at"),
                            progress_percent=task_data.get("progress_percent", 0),
                            difficulty_level=task_data.get("difficulty_level", 3),
                            impact_level=task_data.get("impact_level", 3)
                        )
                        tasks.append(task)
                    except Exception as e:
                        print(f"加载任务时出错: {e}")
                return tasks
        return []
    
    def _save_tasks(self):
        """保存任务数据"""
        data = {
            "tasks": [task.to_dict() for task in self.tasks],
            "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def add_task(self, task: Task):
        """添加新任务"""
        self.tasks.append(task)
        self._save_tasks()
    
    def generate_daily_plan(self, date_str: Optional[str] = None) -> Dict[str, Any]:
        """生成今日规划"""
        if date_str is None:
            date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        
        # 筛选待处理任务
        pending_tasks = [task for task in self.tasks if task.status in ["pending", "in_progress", "blocked"]]
        
        # 计算每个任务的优先级分数
        for task in pending_tasks:
            task.priority_score = self.priority_engine.calculate_priority_score(task)
        
        # 按优先级排序
        sorted_tasks = sorted(pending_tasks, key=lambda x: x.priority_score, reverse=True)
        
        # 生成重点关注领域
        focus_analysis = self.priority_engine.generate_daily_focus(sorted_tasks)
        
        # 确定关键任务（前20%）
        critical_count = max(1, len(sorted_tasks) // 5)
        critical_tasks = sorted_tasks[:critical_count]
        
        # 确定今日可完成的任务（基于8小时工作日）
        daily_capacity = 8  # 小时
        daily_tasks = []
        time_used = 0
        
        for task in sorted_tasks:
            if time_used + task.estimated_hours <= daily_capacity:
                daily_tasks.append(task)
                time_used += task.estimated_hours
            else:
                break
        
        # 生成规划报告
        plan = {
            "date": date_str,
            "total_tasks": len(pending_tasks),
            "critical_tasks_count": len(critical_tasks),
            "daily_tasks_count": len(daily_tasks),
            "estimated_daily_hours": time_used,
            "daily_focus_areas": focus_analysis["daily_focus"],
            "recommended_time_allocation": focus_analysis["recommended_focus_ratio"],
            "critical_tasks": [
                {
                    "id": task.id,
                    "title": task.title,
                    "task_type": task.task_type.value,
                    "priority_score": task.priority_score,
                    "estimated_hours": task.estimated_hours,
                    "status": task.status
                }
                for task in critical_tasks
            ],
            "recommended_daily_tasks": [
                {
                    "id": task.id,
                    "title": task.title,
                    "task_type": task.task_type.value,
                    "priority_score": task.priority_score,
                    "estimated_hours": task.estimated_hours,
                    "time_slot": self._assign_time_slot(task, daily_tasks.index(task))
                }
                for task in daily_tasks
            ],
            "team_considerations": self._generate_team_considerations(sorted_tasks),
            "risk_warnings": self._identify_risks(sorted_tasks)
        }
        
        return plan
    
    def _assign_time_slot(self, task: Task, index: int) -> str:
        """分配时间段"""
        time_slots = [
            "09:00-10:30",  # 上午第一段
            "10:30-12:00",  # 上午第二段
            "13:30-15:00",  # 下午第一段
            "15:00-16:30",  # 下午第二段
            "16:30-18:00",  # 下午第三段
        ]
        
        if index < len(time_slots):
            return time_slots[index]
        return "灵活安排"
    
    def _generate_team_considerations(self, tasks: List[Task]) -> List[str]:
        """生成团队考虑事项"""
        considerations = []
        
        # 检查是否有需要协调的任务
        coordination_tasks = [t for t in tasks if t.assigned_to and "团队" in t.assigned_to]
        if coordination_tasks:
            considerations.append(f"今日有{len(coordination_tasks)}个需要跨团队协调的任务")
        
        # 检查阻塞任务
        blocked_tasks = [t for t in tasks if t.status == "blocked"]
        if blocked_tasks:
            considerations.append(f"有{len(blocked_tasks)}个任务被阻塞，需要优先处理")
        
        # 检查高难度任务
        hard_tasks = [t for t in tasks if t.difficulty_level >= 4]
        if hard_tasks:
            considerations.append(f"有{len(hard_tasks)}个高难度任务，可能需要技术支持")
        
        return considerations
    
    def _identify_risks(self, tasks: List[Task]) -> List[str]:
        """识别风险"""
        risks = []
        
        # 截止日期风险
        today = datetime.datetime.now()
        for task in tasks:
            if task.deadline:
                try:
                    deadline = datetime.datetime.strptime(task.deadline, "%Y-%m-%d")
                    days_left = (deadline - today).days
                    if 0 <= days_left <= 2 and task.progress_percent < 80:
                        risks.append(f"任务'{task.title}'截止日期临近（{days_left}天），进度{task.progress_percent}%")
                except:
                    pass
        
        # 依赖风险
        for task in tasks:
            if task.dependencies:
                deps_status = []
                for dep_id in task.dependencies:
                    dep_task = next((t for t in tasks if t.id == dep_id), None)
                    if dep_task and dep_task.status != "completed":
                        deps_status.append(f"{dep_task.title}({dep_task.status})")
                
                if deps_status:
                    risks.append(f"任务'{task.title}'依赖未完成: {', '.join(deps_status)}")
        
        return risks
    
    def generate_summary_report(self) -> str:
        """生成摘要报告"""
        plan = self.generate_daily_plan()
        
        report = f"""
{'='*60}
🤖 机器人研发团队负责人每日规划 - {plan['date']}
{'='*60}

📊 总体概况:
• 待处理任务总数: {plan['total_tasks']} 个
• 关键任务数量: {plan['critical_tasks_count']} 个
• 今日推荐任务: {plan['daily_tasks_count']} 个
• 预计工作时间: {plan['estimated_daily_hours']} 小时

🎯 今日重点关注领域:
"""
        
        for focus in plan['daily_focus_areas']:
            report += f"  {focus}\n"
        
        report += f"""
⏰ 推荐时间分配比例:
• 项目管理: {plan['recommended_time_allocation']['项目管理']*100:.0f}%
• 技术攻关: {plan['recommended_time_allocation']['技术攻关']*100:.0f}%  
• 团队管理: {plan['recommended_time_allocation']['团队管理']*100:.0f}%

🔴 关键任务 (必须优先处理):
"""
        
        for i, task in enumerate(plan['critical_tasks'], 1):
            report += f"{i}. [{task['task_type']}] {task['title']}\n"
            report += f"   优先级分: {task['priority_score']:.1f} | 预估: {task['estimated_hours']}小时 | 状态: {task['status']}\n"
        
        report += f"""
📋 今日推荐任务安排:
"""
        
        for i, task in enumerate(plan['recommended_daily_tasks'], 1):
            report += f"{i}. [{task['time_slot']}] {task['title']}\n"
            report += f"   类型: {task['task_type']} | 优先级分: {task['priority_score']:.1f}\n"
        
        if plan['team_considerations']:
            report += f"""
👥 团队考虑事项:
"""
            for consideration in plan['team_considerations']:
                report += f"• {consideration}\n"
        
        if plan['risk_warnings']:
            report += f"""
⚠️ 风险提醒:
"""
            for risk in plan['risk_warnings']:
                report += f"• {risk}\n"
        
        report += f"""
{'='*60}
💡 今日建议:
1. 上午专注技术攻关任务
2. 下午安排会议和团队协调
3. 留出时间处理突发问题
4. 每日下班前花15分钟更新任务状态
{'='*60}
"""
        
        return report

# ==================== 快速任务录入工具 ====================

class QuickTaskInput:
    """快速任务录入工具"""
    
    @staticmethod
    def parse_natural_language(text: str) -> Optional[Task]:
        """解析自然语言输入，生成任务"""
        import uuid
        
        # 默认值
        task_type = TaskType.TEAM_MANAGEMENT
        priority = PriorityLevel.MEDIUM
        difficulty = 3
        impact = 3
        
        # 检测任务类型关键词
        text_lower = text.lower()
        
        type_keywords = {
            TaskType.HARDWARE: ["硬件", "电路", "传感器", "电机", "控制器", "pcb", "嵌入式"],
            TaskType.SOFTWARE: ["软件", "代码", "架构", "接口", "api", "调试", "测试"],
            TaskType.ALGORITHM: ["算法", "模型", "ai", "机器学习", "视觉", "导航", "路径规划"],
            TaskType.STRUCTURE: ["结构", "机械", "设计", "cad", "3d打印", "装配"],
            TaskType.PROJECT_MILESTONE: ["里程碑", "节点", "交付", "验收", "阶段"],
            TaskType.TEAM_MANAGEMENT: ["团队", "人员", "协调", "分配", "培训"],
            TaskType.DECISION_MAKING: ["决策", "选择", "确定", "方案", "评审"],
            TaskType.EXTERNAL_COMM: ["客户", "供应商", "合作", "沟通", "会议"],
            TaskType.RISK_MANAGEMENT: ["风险", "问题", "障碍", "解决", "故障"],
            TaskType.INNOVATION: ["创新", "调研", "预研", "新技术", "探索"]
        }
        
        for task_type_enum, keywords in type_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                task_type = task_type_enum
                break
        
        # 检测优先级关键词
        if any(word in text_lower for word in ["紧急", "立刻", "马上", "今天必须", "关键"]):
            priority = PriorityLevel.CRITICAL
            difficulty = 4
            impact = 4
        elif any(word in text_lower for word in ["重要", "优先", "尽快", "本周"]):
            priority = PriorityLevel.HIGH
            difficulty = 3
            impact = 3
        elif any(word in text_lower for word in ["一般", "常规", "日常"]):
            priority = PriorityLevel.MEDIUM
            difficulty = 2
            impact = 2
        
        # 检测难度关键词
        if any(word in text_lower for word in ["复杂", "困难", "挑战", "难题"]):
            difficulty = 4
        if any(word in text_lower for word in ["简单", "容易", "快速"]):
            difficulty = 2
        
        # 检测影响范围
        if any(word in text_lower for word in ["全局", "整体", "所有团队", "全项目"]):
            impact = 5
        if any(word in text_lower for word in ["局部", "部分", "个别"]):
            impact = 2
        
        # 提取预估时间
        estimated_hours = 2.0
        hour_pattern = r"(\d+)[\s\-]*(小时|h|hour)"
        match = re.search(hour_pattern, text_lower)
        if match:
            estimated_hours = float(match.group(1))
        
        # 创建任务
        task_id = str(uuid.uuid4())[:8]
        task = Task(
            id=task_id,
            title=text[:50],  # 截取前50个字符作为标题
            task_type=task_type,
            priority=priority,
            description=text,
            estimated_hours=estimated_hours,
            difficulty_level=difficulty,
            impact_level=impact,
            created_at=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        
        return task

# ==================== 主函数 ====================

def main():
    """主函数：演示系统使用"""
    print("[系统] 机器人研发团队负责人任务优先级系统")
    print("=" * 50)
    
    # 初始化规划器
    planner = DailyPlanner()
    
    # 如果还没有任务，添加一些示例任务
    if not planner.tasks:
        print("检测到无任务数据，添加示例任务...")
        
        # 示例任务
        example_tasks = [
            Task(
                id="T001",
                title="机器人运动控制算法优化",
                task_type=TaskType.ALGORITHM,
                priority=PriorityLevel.HIGH,
                description="优化四足机器人的步态控制算法，提升运动稳定性",
                estimated_hours=6.0,
                difficulty_level=4,
                impact_level=4,
                deadline="2025-03-15"
            ),
            Task(
                id="T002",
                title="项目第二阶段里程碑评审",
                task_type=TaskType.PROJECT_MILESTONE,
                priority=PriorityLevel.CRITICAL,
                description="准备第二阶段交付物，组织客户评审会议",
                estimated_hours=4.0,
                difficulty_level=3,
                impact_level=5,
                deadline="2025-03-14"
            ),
            Task(
                id="T003",
                title="硬件团队技术瓶颈攻关",
                task_type=TaskType.HARDWARE,
                priority=PriorityLevel.HIGH,
                description="解决电机驱动器过热问题，协调硬件团队技术攻关",
                estimated_hours=3.0,
                difficulty_level=4,
                impact_level=3
            ),
            Task(
                id="T004",
                title="团队周例会和技术分享",
                task_type=TaskType.TEAM_MANAGEMENT,
                priority=PriorityLevel.MEDIUM,
                description="组织团队周例会，安排技术分享内容",
                estimated_hours=2.0,
                difficulty_level=2,
                impact_level=3
            ),
            Task(
                id="T005",
                title="新型传感器技术调研",
                task_type=TaskType.INNOVATION,
                priority=PriorityLevel.LOW,
                description="调研最新的激光雷达传感器技术，评估可行性",
                estimated_hours=5.0,
                difficulty_level=3,
                impact_level=2
            )
        ]
        
        for task in example_tasks:
            planner.add_task(task)
        
        print("✅ 示例任务添加完成")
    
    # 生成今日规划
    print("\n📅 正在生成今日工作规划...")
    report = planner.generate_summary_report()
    print(report)
    
    # 显示快速录入提示
    print("\n💡 快速任务录入提示:")
    print("   直接输入任务描述，系统会自动识别类型和优先级")
    print("   示例: '今天必须解决导航算法精度问题，这个很紧急'")
    print("   示例: '安排下周与客户的进度汇报会议'")
    print("   示例: '调研新的机械臂结构设计方案，需要3小时'")

if __name__ == "__main__":
    main()