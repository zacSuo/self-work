#!/usr/bin/env python3
"""
机器人研发团队负责人每日工作规划 - 简化版
避免编码问题，专注功能实现
"""

import json
import os
import datetime
from enum import Enum
from dataclasses import dataclass, asdict

# ==================== 数据模型 ====================

class TaskType(Enum):
    """任务类型枚举"""
    HARDWARE = "硬件技术攻关"
    SOFTWARE = "软件技术攻关"
    ALGORITHM = "算法研发攻关"
    STRUCTURE = "结构设计攻关"
    PROJECT_MILESTONE = "项目关键节点"
    TEAM_MANAGEMENT = "团队管理"
    DECISION_MAKING = "关键决策"
    EXTERNAL_COMM = "外部沟通"
    RISK_MANAGEMENT = "风险管控"
    INNOVATION = "技术创新探索"

class PriorityLevel(Enum):
    """优先级级别"""
    CRITICAL = "关键紧急"
    HIGH = "高优先级"
    MEDIUM = "中等优先级"
    LOW = "低优先级"
    BACKLOG = "待办事项"

@dataclass
class Task:
    """任务数据类"""
    id: str
    title: str
    task_type: TaskType
    priority: PriorityLevel
    description: str
    estimated_hours: float = 2.0
    deadline: str = None
    status: str = "pending"
    progress_percent: int = 0
    difficulty_level: int = 3
    impact_level: int = 3
    created_at: str = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# ==================== 核心规划器 ====================

class RobotTeamPlanner:
    """机器人团队规划器"""
    
    def __init__(self, data_file="robot_tasks_simple.json"):
        self.data_file = data_file
        self.tasks = self.load_tasks()
    
    def load_tasks(self):
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
                            estimated_hours=task_data.get("estimated_hours", 2.0),
                            deadline=task_data.get("deadline"),
                            status=task_data.get("status", "pending"),
                            progress_percent=task_data.get("progress_percent", 0),
                            difficulty_level=task_data.get("difficulty_level", 3),
                            impact_level=task_data.get("impact_level", 3),
                            created_at=task_data.get("created_at")
                        )
                        tasks.append(task)
                    except:
                        continue
                return tasks
        return self.create_sample_tasks()
    
    def create_sample_tasks(self):
        """创建示例任务"""
        sample_tasks = [
            Task(
                id="T001",
                title="机器人运动控制算法优化",
                task_type=TaskType.ALGORITHM,
                priority=PriorityLevel.HIGH,
                description="优化四足机器人的步态控制算法，提升运动稳定性",
                estimated_hours=6.0,
                difficulty_level=4,
                impact_level=4,
                deadline="2026-03-15"
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
                deadline="2026-03-14"
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
        self.save_tasks(sample_tasks)
        return sample_tasks
    
    def save_tasks(self, tasks=None):
        """保存任务数据"""
        if tasks is None:
            tasks = self.tasks
        
        data = {
            "tasks": [
                {
                    "id": task.id,
                    "title": task.title,
                    "task_type": task.task_type.value,
                    "priority": task.priority.value,
                    "description": task.description,
                    "estimated_hours": task.estimated_hours,
                    "deadline": task.deadline,
                    "status": task.status,
                    "progress_percent": task.progress_percent,
                    "difficulty_level": task.difficulty_level,
                    "impact_level": task.impact_level,
                    "created_at": task.created_at
                }
                for task in tasks
            ],
            "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def calculate_priority_score(self, task):
        """计算任务优先级分数"""
        # 基础分
        base_scores = {
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
        
        base = base_scores.get(task.task_type, 50)
        
        # 难度调整
        difficulty_adj = task.difficulty_level * 5
        
        # 影响调整
        impact_adj = task.impact_level * 8
        
        # 截止日期调整
        deadline_adj = 0
        if task.deadline:
            try:
                deadline = datetime.datetime.strptime(task.deadline, "%Y-%m-%d")
                today = datetime.datetime.now()
                days_left = (deadline - today).days
                
                if days_left < 0:
                    deadline_adj = 30
                elif days_left <= 1:
                    deadline_adj = 25
                elif days_left <= 3:
                    deadline_adj = 20
                elif days_left <= 7:
                    deadline_adj = 15
                elif days_left <= 14:
                    deadline_adj = 10
                else:
                    deadline_adj = 5
            except:
                pass
        
        total = base + difficulty_adj + impact_adj + deadline_adj
        
        # 状态调整
        if task.status == "blocked":
            total += 20
        elif task.status == "in_progress":
            total += 10
        
        return min(100, total)
    
    def generate_daily_plan(self):
        """生成每日规划"""
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        
        # 筛选待处理任务
        pending_tasks = [t for t in self.tasks if t.status != "completed"]
        
        if not pending_tasks:
            return {
                "date": today,
                "message": "恭喜！所有任务已完成！",
                "tasks": []
            }
        
        # 计算优先级分数
        for task in pending_tasks:
            task.priority_score = self.calculate_priority_score(task)
        
        # 按优先级排序
        sorted_tasks = sorted(pending_tasks, key=lambda x: x.priority_score, reverse=True)
        
        # 确定关键任务（前20%）
        critical_count = max(1, len(sorted_tasks) // 5)
        critical_tasks = sorted_tasks[:critical_count]
        
        # 确定今日可完成的任务（基于8小时工作日）
        daily_capacity = 8
        daily_tasks = []
        time_used = 0
        
        for task in sorted_tasks:
            if time_used + task.estimated_hours <= daily_capacity:
                daily_tasks.append(task)
                time_used += task.estimated_hours
            else:
                break
        
        # 按类型统计
        type_stats = {}
        for task in pending_tasks:
            task_type = task.task_type.value
            type_stats[task_type] = type_stats.get(task_type, 0) + 1
        
        # 生成规划
        plan = {
            "date": today,
            "total_pending_tasks": len(pending_tasks),
            "critical_tasks_count": len(critical_tasks),
            "daily_tasks_count": len(daily_tasks),
            "estimated_hours": round(time_used, 1),
            "critical_tasks": [
                {
                    "title": task.title,
                    "type": task.task_type.value,
                    "score": task.priority_score,
                    "hours": task.estimated_hours,
                    "status": task.status
                }
                for task in critical_tasks
            ],
            "daily_tasks": [
                {
                    "title": task.title,
                    "type": task.task_type.value,
                    "score": task.priority_score,
                    "hours": task.estimated_hours
                }
                for task in daily_tasks
            ],
            "type_distribution": type_stats
        }
        
        return plan
    
    def print_daily_plan(self):
        """打印每日规划"""
        plan = self.generate_daily_plan()
        
        print("\n" + "="*70)
        print("机器人研发团队负责人 - 每日工作规划")
        print("日期:", plan["date"])
        print("="*70)
        
        print(f"\n[概览] 待处理任务: {plan['total_pending_tasks']}个")
        print(f"      关键任务: {plan['critical_tasks_count']}个")
        print(f"      今日推荐: {plan['daily_tasks_count']}个")
        print(f"      预估时间: {plan['estimated_hours']}小时")
        
        if plan["critical_tasks"]:
            print(f"\n[关键任务] (必须优先处理):")
            for i, task in enumerate(plan["critical_tasks"], 1):
                print(f"  {i}. {task['title']}")
                print(f"     类型: {task['type']} | 优先级分: {task['score']:.1f}")
                print(f"     预估: {task['hours']}小时 | 状态: {task['status']}")
        
        if plan["daily_tasks"]:
            print(f"\n[今日推荐任务]:")
            time_slots = ["09:00-10:30", "10:30-12:00", "13:30-15:00", "15:00-16:30", "16:30-18:00"]
            for i, task in enumerate(plan["daily_tasks"]):
                time_slot = time_slots[i] if i < len(time_slots) else "灵活安排"
                print(f"  {i+1}. [{time_slot}] {task['title']}")
                print(f"     类型: {task['type']} | 优先级分: {task['score']:.1f}")
        
        if plan["type_distribution"]:
            print(f"\n[任务类型分布]:")
            for task_type, count in plan["type_distribution"].items():
                print(f"  - {task_type}: {count}个")
        
        print(f"\n[时间分配建议]:")
        print("  - 上午 (09:00-12:00): 专注技术攻关任务")
        print("  - 中午 (12:00-13:30): 午餐休息，简短复盘")
        print("  - 下午 (13:30-16:00): 会议和团队协调")
        print("  - 傍晚 (16:00-18:00): 处理突发问题，规划明日")
        
        print("\n" + "="*70)
        print("提示: 保持专注，一次只处理一个关键任务")
        print("="*70)

# ==================== 主程序 ====================

def main():
    """主程序"""
    print("[系统] 机器人研发团队负责人工作规划系统")
    print("[版本] 简化版 - 专注于每日优先级安排")
    print("[说明] 每天早上运行此系统获取当日工作规划")
    print("-" * 70)
    
    # 初始化规划器
    planner = RobotTeamPlanner()
    
    # 生成并显示今日规划
    planner.print_daily_plan()
    
    # 显示快速操作选项
    print("\n[快速操作]:")
    print("  1. 查看任务详情")
    print("  2. 添加新任务")
    print("  3. 更新任务状态")
    print("  4. 保存并退出")
    print("  5. 直接退出")
    
    while True:
        choice = input("\n请选择操作 (1-5): ").strip()
        
        if choice == "1":
            print("\n[当前任务列表]:")
            pending = [t for t in planner.tasks if t.status != "completed"]
            if pending:
                for i, task in enumerate(pending, 1):
                    status_icon = "[进行中]" if task.status == "in_progress" else "[待处理]" if task.status == "pending" else "[阻塞]"
                    print(f"  {i}. {status_icon} {task.title}")
                    print(f"     类型: {task.task_type.value} | 优先级: {task.priority.value}")
                    print(f"     进度: {task.progress_percent}% | 预估: {task.estimated_hours}小时")
                    if task.deadline:
                        print(f"     截止: {task.deadline}")
            else:
                print("  暂无待处理任务")
        
        elif choice == "2":
            print("\n[添加新任务]:")
            title = input("  任务标题: ").strip()
            if title:
                # 简化版：创建基本任务
                import uuid
                new_task = Task(
                    id=str(uuid.uuid4())[:8],
                    title=title,
                    task_type=TaskType.TEAM_MANAGEMENT,
                    priority=PriorityLevel.MEDIUM,
                    description=title,
                    estimated_hours=2.0
                )
                planner.tasks.append(new_task)
                planner.save_tasks()
                print(f"  任务已添加: {title}")
        
        elif choice == "3":
            print("\n[更新任务状态]:")
            pending = [t for t in planner.tasks if t.status != "completed"]
            if pending:
                for i, task in enumerate(pending, 1):
                    print(f"  {i}. {task.title} [{task.status}]")
                
                try:
                    task_num = int(input("\n  选择任务编号: ")) - 1
                    if 0 <= task_num < len(pending):
                        task = pending[task_num]
                        new_status = input(f"  任务: {task.title}\n  新状态 (pending/in_progress/completed): ").strip().lower()
                        if new_status in ["pending", "in_progress", "completed"]:
                            task.status = new_status
                            if new_status == "completed":
                                task.progress_percent = 100
                            planner.save_tasks()
                            print("  状态已更新")
                        else:
                            print("  无效状态")
                    else:
                        print("  无效编号")
                except:
                    print("  输入错误")
            else:
                print("  暂无任务可更新")
        
        elif choice == "4":
            planner.save_tasks()
            print("[系统] 数据已保存")
            print("[系统] 再见！祝您工作顺利！")
            break
        
        elif choice == "5":
            print("[系统] 再见！")
            break
        
        else:
            print("[系统] 无效选择，请重试")

if __name__ == "__main__":
    main()