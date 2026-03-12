#!/usr/bin/env python3
"""
记忆系统 - Memory System
用于记录用户的习惯、工作方式、决策模式和任务安排
"""

import json
import datetime
import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class HabitRecord:
    """习惯记录"""
    name: str
    description: str
    frequency: str  # daily, weekly, monthly
    priority: int  # 1-10
    created_at: str
    last_practiced: str
    success_rate: float  # 0-1


@dataclass
class WorkStyleRecord:
    """工作方式记录"""
    category: str  # 工作习惯, 沟通方式, 决策模式等
    description: str
    effectiveness: int  # 1-10
    preferred_tools: List[str]
    working_hours: Dict[str, str]
    created_at: str


@dataclass
class DecisionRecord:
    """决策记录"""
    decision_type: str  # 工作决策, 生活决策, 技术决策等
    description: str
    factors_considered: List[str]
    outcome: str  # positive, negative, neutral
    confidence_level: int  # 1-10
    timestamp: str
    lessons_learned: str


@dataclass
class TaskRecord:
    """任务安排记录"""
    title: str
    description: str
    priority: str  # low, medium, high, urgent
    status: str  # pending, in_progress, completed, cancelled
    deadline: str
    estimated_hours: float
    actual_hours: Optional[float]
    created_at: str
    completed_at: Optional[str]
    tags: List[str]


class MemorySystem:
    """记忆系统主类"""
    
    def __init__(self, storage_path: str = "private_data/data/memory_data.json"):
        self.storage_path = storage_path
        self.habits: List[HabitRecord] = []
        self.work_styles: List[WorkStyleRecord] = []
        self.decisions: List[DecisionRecord] = []
        self.tasks: List[TaskRecord] = []
        
        # 加载现有数据
        self.load_data()
    
    def _get_current_timestamp(self) -> str:
        """获取当前时间戳"""
        return datetime.datetime.now().isoformat()
    
    def load_data(self):
        """从文件加载数据"""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # 反序列化数据
                self.habits = [HabitRecord(**habit) for habit in data.get('habits', [])]
                self.work_styles = [WorkStyleRecord(**style) for style in data.get('work_styles', [])]
                self.decisions = [DecisionRecord(**decision) for decision in data.get('decisions', [])]
                self.tasks = [TaskRecord(**task) for task in data.get('tasks', [])]
                
                print(f"成功加载记忆数据: {len(self.habits)}个习惯, {len(self.work_styles)}个工作方式, "
                      f"{len(self.decisions)}个决策, {len(self.tasks)}个任务")
            
            except Exception as e:
                print(f"加载数据失败: {e}")
                # 初始化空数据结构
                self._initialize_empty_data()
        else:
            self._initialize_empty_data()
    
    def _initialize_empty_data(self):
        """初始化空数据结构"""
        self.habits = []
        self.work_styles = []
        self.decisions = []
        self.tasks = []
    
    def save_data(self):
        """保存数据到文件"""
        try:
            data = {
                'habits': [asdict(habit) for habit in self.habits],
                'work_styles': [asdict(style) for style in self.work_styles],
                'decisions': [asdict(decision) for decision in self.decisions],
                'tasks': [asdict(task) for task in self.tasks],
                'last_updated': self._get_current_timestamp()
            }
            
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print("数据保存成功")
        
        except Exception as e:
            print(f"保存数据失败: {e}")
    
    # 习惯管理方法
    def add_habit(self, name: str, description: str, frequency: str, priority: int = 5) -> bool:
        """添加新习惯"""
        try:
            habit = HabitRecord(
                name=name,
                description=description,
                frequency=frequency,
                priority=priority,
                created_at=self._get_current_timestamp(),
                last_practiced=self._get_current_timestamp(),
                success_rate=0.0
            )
            self.habits.append(habit)
            self.save_data()
            return True
        
        except Exception as e:
            print(f"添加习惯失败: {e}")
            return False
    
    def update_habit_practice(self, habit_name: str, success: bool = True) -> bool:
        """更新习惯实践记录"""
        for habit in self.habits:
            if habit.name == habit_name:
                habit.last_practiced = self._get_current_timestamp()
                # 简单计算成功率
                habit.success_rate = (habit.success_rate * 0.9) + (0.1 if success else 0)
                self.save_data()
                return True
        return False
    
    # 工作方式管理
    def add_work_style(self, category: str, description: str, effectiveness: int, 
                      preferred_tools: List[str], working_hours: Dict[str, str]) -> bool:
        """添加工作方式记录"""
        try:
            work_style = WorkStyleRecord(
                category=category,
                description=description,
                effectiveness=effectiveness,
                preferred_tools=preferred_tools,
                working_hours=working_hours,
                created_at=self._get_current_timestamp()
            )
            self.work_styles.append(work_style)
            self.save_data()
            return True
        
        except Exception as e:
            print(f"添加工作方式失败: {e}")
            return False
    
    # 决策记录管理
    def record_decision(self, decision_type: str, description: str, factors: List[str], 
                       outcome: str, confidence: int, lessons: str) -> bool:
        """记录决策"""
        try:
            decision = DecisionRecord(
                decision_type=decision_type,
                description=description,
                factors_considered=factors,
                outcome=outcome,
                confidence_level=confidence,
                timestamp=self._get_current_timestamp(),
                lessons_learned=lessons
            )
            self.decisions.append(decision)
            self.save_data()
            return True
        
        except Exception as e:
            print(f"记录决策失败: {e}")
            return False
    
    # 任务管理
    def add_task(self, title: str, description: str, priority: str, deadline: str, 
                estimated_hours: float, tags: List[str] = None) -> bool:
        """添加新任务"""
        try:
            task = TaskRecord(
                title=title,
                description=description,
                priority=priority,
                status="pending",
                deadline=deadline,
                estimated_hours=estimated_hours,
                actual_hours=None,
                created_at=self._get_current_timestamp(),
                completed_at=None,
                tags=tags or []
            )
            self.tasks.append(task)
            self.save_data()
            return True
        
        except Exception as e:
            print(f"添加任务失败: {e}")
            return False
    
    def update_task_status(self, title: str, status: str, actual_hours: float = None) -> bool:
        """更新任务状态"""
        for task in self.tasks:
            if task.title == title:
                task.status = status
                if status == "completed":
                    task.completed_at = self._get_current_timestamp()
                    if actual_hours is not None:
                        task.actual_hours = actual_hours
                self.save_data()
                return True
        return False
    
    # 查询和分析方法
    def get_habits_by_priority(self, min_priority: int = 0) -> List[HabitRecord]:
        """按优先级获取习惯"""
        return sorted([h for h in self.habits if h.priority >= min_priority], 
                     key=lambda x: x.priority, reverse=True)
    
    def get_recent_decisions(self, days: int = 7) -> List[DecisionRecord]:
        """获取最近N天的决策"""
        cutoff_date = datetime.datetime.now() - datetime.timedelta(days=days)
        return [d for d in self.decisions 
                if datetime.datetime.fromisoformat(d.timestamp) > cutoff_date]
    
    def get_pending_tasks(self) -> List[TaskRecord]:
        """获取待处理任务"""
        return [t for t in self.tasks if t.status in ["pending", "in_progress"]]
    
    def get_task_completion_rate(self) -> float:
        """计算任务完成率"""
        if not self.tasks:
            return 0.0
        completed = len([t for t in self.tasks if t.status == "completed"])
        return completed / len(self.tasks)
    
    # 统计分析
    def generate_summary(self) -> Dict[str, Any]:
        """生成系统摘要"""
        return {
            "total_habits": len(self.habits),
            "total_work_styles": len(self.work_styles),
            "total_decisions": len(self.decisions),
            "total_tasks": len(self.tasks),
            "task_completion_rate": self.get_task_completion_rate(),
            "recent_decisions": len(self.get_recent_decisions(7)),
            "pending_tasks": len(self.get_pending_tasks()),
            "high_priority_habits": len(self.get_habits_by_priority(7)),
            "last_updated": self._get_current_timestamp()
        }


def main():
    """主函数 - 演示使用"""
    memory = MemorySystem()
    
    # 演示添加一些示例数据
    print("=== 记忆系统演示 ===")
    
    # 添加示例习惯
    memory.add_habit("晨间阅读", "每天早晨阅读技术文章30分钟", "daily", 8)
    memory.add_habit("代码审查", "每周进行代码审查和总结", "weekly", 7)
    
    # 添加工作方式
    memory.add_work_style(
        "工作习惯", 
        "喜欢先规划再执行，使用番茄工作法", 
        8, 
        ["VS Code", "Git", "任务管理工具"],
        {"morning": "9:00-12:00", "afternoon": "14:00-18:00"}
    )
    
    # 记录决策
    memory.record_decision(
        "技术决策",
        "选择使用Python而不是Java进行新项目开发",
        ["开发效率", "团队熟悉度", "项目需求"],
        "positive",
        8,
        "Python在快速原型开发方面更有优势"
    )
    
    # 添加任务
    memory.add_task(
        "完成记忆系统开发",
        "实现记忆系统的核心功能",
        "high",
        "2024-03-15",
        4.0,
        ["开发", "Python"]
    )
    
    # 显示摘要
    summary = memory.generate_summary()
    print("\n系统摘要:")
    for key, value in summary.items():
        print(f"  {key}: {value}")
    
    print("\n演示完成!")


if __name__ == "__main__":
    main()