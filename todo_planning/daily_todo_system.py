#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日智能待办事项系统
基于用户工作时间和会议安排，生成每日优先级任务清单
"""

import json
import os
from datetime import datetime, date, timedelta
from typing import Dict, List, Any, Optional
import calendar

class WorkTimeConfig:
    """工作时间配置"""
    def __init__(self):
        self.work_hours = {
            "morning_start": "09:00",
            "morning_end": "12:00",
            "afternoon_start": "13:30",
            "afternoon_end": "18:00"
        }
        
        self.daily_work_hours = 7.5  # 每天工作7.5小时
        self.weekly_work_days = 5    # 每周工作5天
        self.weekend_days = ["周六", "周日"]
        
        # 晚上学习安排
        self.evening_study = {
            "monday": True,
            "tuesday": True,
            "wednesday": True,
            "thursday": True,
            "friday": False,  # 周五晚上不学习
            "saturday": False,
            "sunday": False
        }
        
        # 每日固定会议时间（从之前系统导入）
        self.load_weekly_meetings()
    
    def load_weekly_meetings(self):
        """加载每周固定会议"""
        try:
            with open("private_data/data/private_data/data/weekly_meeting_data.json", "r", encoding="utf-8") as f:
                self.weekly_meetings = json.load(f)
        except FileNotFoundError:
            # 如果文件不存在，创建默认会议数据
            self.weekly_meetings = self.create_default_meetings()
            self.save_weekly_meetings()
    
    def create_default_meetings(self):
        """创建默认会议数据"""
        return {
            "meetings": [
                # 周一
                {"day": "周一", "name": "公司管理层周例会", "time": "09:30-11:00", "duration": "1.5小时", "priority": "高"},
                {"day": "周一", "name": "机器人讨论会", "time": "11:00-12:00", "duration": "1.0小时", "priority": "高"},
                
                # 周二
                {"day": "周二", "name": "商清项目站会", "time": "09:20-09:30", "duration": "10分钟", "priority": "中"},
                {"day": "周二", "name": "晨曦项目站会", "time": "09:10-09:20", "duration": "10分钟", "priority": "中"},
                {"day": "周二", "name": "管理层站会", "time": "09:30-09:50", "duration": "20分钟", "priority": "中"},
                
                # 周三
                {"day": "周三", "name": "商清项目站会", "time": "09:20-09:30", "duration": "10分钟", "priority": "中"},
                {"day": "周三", "name": "晨曦项目站会", "time": "09:10-09:20", "duration": "10分钟", "priority": "中"},
                {"day": "周三", "name": "管理层站会", "time": "09:30-09:50", "duration": "20分钟", "priority": "中"},
                {"day": "周三", "name": "品质周例会", "time": "09:30-10:30", "duration": "1.0小时", "priority": "高"},
                
                # 周四
                {"day": "周四", "name": "商清项目站会", "time": "09:20-09:30", "duration": "10分钟", "priority": "中"},
                {"day": "周四", "name": "晨曦项目站会", "time": "09:10-09:20", "duration": "10分钟", "priority": "中"},
                {"day": "周四", "name": "管理层站会", "time": "09:30-09:50", "duration": "20分钟", "priority": "中"},
                
                # 周五
                {"day": "周五", "name": "商清项目站会", "time": "09:20-09:30", "duration": "10分钟", "priority": "中"},
                {"day": "周五", "name": "晨曦项目站会", "time": "09:10-09:20", "duration": "10分钟", "priority": "中"},
                {"day": "周五", "name": "管理层站会", "time": "09:30-09:50", "duration": "20分钟", "priority": "中"},
                {"day": "周五", "name": "商清项目Sprint评审与计划会", "time": "11:00-12:00", "duration": "1.0小时", "priority": "高"},
                {"day": "周五", "name": "晨曦项目Sprint评审与计划会", "time": "16:30-17:30", "duration": "1.0小时", "priority": "高"},
                {"day": "周五", "name": "技术团队回顾与技术分享会", "time": "17:30-18:00", "duration": "0.5小时", "priority": "中"}
            ]
        }
    
    def save_weekly_meetings(self):
        """保存会议数据"""
        with open("private_data/data/private_data/data/weekly_meeting_data.json", "w", encoding="utf-8") as f:
            json.dump(self.weekly_meetings, f, ensure_ascii=False, indent=2)
    
    def get_today_meetings(self, target_date: Optional[date] = None) -> List[Dict]:
        """获取指定日期的会议"""
        if target_date is None:
            target_date = date.today()
        
        # 将日期转换为中文星期
        weekdays = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        weekday_idx = target_date.weekday()
        chinese_weekday = weekdays[weekday_idx]
        
        # 过滤当天的会议
        today_meetings = []
        for meeting in self.weekly_meetings["meetings"]:
            if meeting["day"] == chinese_weekday:
                today_meetings.append(meeting)
        
        return sorted(today_meetings, key=lambda x: self._parse_time(x["time"].split("-")[0]))
    
    def _parse_time(self, time_str: str) -> int:
        """将时间字符串转换为分钟数用于排序"""
        if ":" in time_str:
            hours, minutes = map(int, time_str.split(":"))
            return hours * 60 + minutes
        return 0
    
    def get_today_available_hours(self, target_date: Optional[date] = None) -> float:
        """计算今天可用的工作时间"""
        if target_date is None:
            target_date = date.today()
        
        # 获取今天的会议
        today_meetings = self.get_today_meetings(target_date)
        
        # 计算会议总时长
        meeting_hours = 0
        for meeting in today_meetings:
            duration = meeting["duration"]
            if "小时" in duration:
                meeting_hours += float(duration.replace("小时", ""))
            elif "分钟" in duration:
                meeting_hours += int(duration.replace("分钟", "")) / 60
        
        # 可用工作时间 = 总工作时间 - 会议时间
        available_hours = self.daily_work_hours - meeting_hours
        return max(available_hours, 0)  # 确保不为负


class TaskPrioritySystem:
    """任务优先级系统"""
    def __init__(self):
        # 任务类别和权重
        self.task_categories = {
            "紧急重要": {"weight": 1.0, "time_estimate": 2.0},  # 最优先处理
            "重要不紧急": {"weight": 0.8, "time_estimate": 1.5},  # 计划性工作
            "紧急不重要": {"weight": 0.6, "time_estimate": 1.0},  # 临时性任务
            "不紧急不重要": {"weight": 0.3, "time_estimate": 0.5}  # 可推迟的任务
        }
        
        # 默认任务模板（可根据需要扩展）
        self.default_tasks = {
            "技术工作": [
                "代码开发和调试",
                "技术问题分析和解决",
                "算法优化和改进",
                "系统架构设计",
                "技术文档编写"
            ],
            "项目管理": [
                "项目进度跟踪和汇报",
                "资源协调和分配",
                "风险评估和管理",
                "团队沟通和协调"
            ],
            "团队管理": [
                "团队成员指导和辅导",
                "绩效评估和反馈",
                "团队建设活动",
                "知识分享和培训"
            ],
            "个人发展": [
                "技术学习和研究",
                "行业动态关注",
                "专业能力提升",
                "英语学习"
            ]
        }
    
    def categorize_task(self, task_description: str) -> str:
        """根据任务描述自动分类"""
        task_lower = task_description.lower()
        
        if any(keyword in task_lower for keyword in ["紧急", "立刻", "马上", "立即", "今天必须"]):
            if any(keyword in task_lower for keyword in ["重要", "关键", "核心", "主要"]):
                return "紧急重要"
            else:
                return "紧急不重要"
        elif any(keyword in task_lower for keyword in ["重要", "关键", "核心", "主要"]):
            return "重要不紧急"
        else:
            return "不紧急不重要"
    
    def estimate_time(self, task_description: str) -> float:
        """估算任务所需时间（小时）"""
        category = self.categorize_task(task_description)
        base_time = self.task_categories[category]["time_estimate"]
        
        # 根据任务复杂度调整
        length_factor = len(task_description) / 50  # 假设描述越长越复杂
        complexity_factor = 1.0
        
        if any(keyword in task_description for keyword in ["复杂", "困难", "挑战", "重大"]):
            complexity_factor = 1.5
        elif any(keyword in task_description for keyword in ["简单", "快速", "轻松", "小"]):
            complexity_factor = 0.7
        
        return base_time * length_factor * complexity_factor


class DailyTodoPlanner:
    """每日待办事项规划器"""
    def __init__(self):
        self.work_config = WorkTimeConfig()
        self.priority_system = TaskPrioritySystem()
        self.todo_file = "private_data/data/daily_todos.json"
        
        # 加载历史待办事项
        self.load_history_todos()
    
    def load_history_todos(self):
        """加载历史待办事项"""
        try:
            with open(self.todo_file, "r", encoding="utf-8") as f:
                self.history_todos = json.load(f)
        except FileNotFoundError:
            self.history_todos = {"daily_todos": []}
    
    def save_todo(self, todo_data: Dict):
        """保存待办事项"""
        self.history_todos["daily_todos"].append(todo_data)
        with open(self.todo_file, "w", encoding="utf-8") as f:
            json.dump(self.history_todos, f, ensure_ascii=False, indent=2)
    
    def generate_daily_todo(self, target_date: Optional[date] = None, 
                           manual_tasks: Optional[List[str]] = None) -> Dict:
        """生成每日待办事项"""
        if target_date is None:
            target_date = date.today()
        
        # 获取今天的会议和可用时间
        today_meetings = self.work_config.get_today_meetings(target_date)
        available_hours = self.work_config.get_today_available_hours(target_date)
        
        # 生成日期信息
        weekdays = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        weekday_idx = target_date.weekday()
        chinese_weekday = weekdays[weekday_idx]
        
        # 生成待办事项
        if manual_tasks:
            tasks = self._process_manual_tasks(manual_tasks, available_hours)
        else:
            tasks = self._generate_default_today_tasks(target_date, available_hours)
        
        # 构建返回数据
        todo_data = {
            "date": target_date.strftime("%Y-%m-%d"),
            "day": chinese_weekday,
            "available_hours": round(available_hours, 1),
            "meeting_hours": round(self.work_config.daily_work_hours - available_hours, 1),
            "total_work_hours": self.work_config.daily_work_hours,
            "meetings": today_meetings,
            "tasks": tasks,
            "evening_study": self.work_config.evening_study.get(chinese_weekday.lower(), False),
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # 保存待办事项
        self.save_todo(todo_data)
        
        return todo_data
    
    def _process_manual_tasks(self, manual_tasks: List[str], available_hours: float) -> List[Dict]:
        """处理手动输入的任务"""
        tasks = []
        remaining_hours = available_hours
        
        for i, task_desc in enumerate(manual_tasks, 1):
            if remaining_hours <= 0:
                break
            
            # 分类和估算时间
            category = self.priority_system.categorize_task(task_desc)
            estimated_time = self.priority_system.estimate_time(task_desc)
            
            # 如果时间不够，调整时间或标记为明天
            if estimated_time > remaining_hours:
                estimated_time = remaining_hours
                status = "部分完成"
            else:
                status = "待开始"
            
            task = {
                "id": f"task_{i:03d}",
                "description": task_desc,
                "category": category,
                "priority": self.priority_system.task_categories[category]["weight"],
                "estimated_hours": round(estimated_time, 1),
                "status": status,
                "actual_hours": 0,
                "completed": False
            }
            
            tasks.append(task)
            remaining_hours -= estimated_time
        
        # 按优先级排序
        tasks.sort(key=lambda x: x["priority"], reverse=True)
        
        return tasks
    
    def _generate_default_today_tasks(self, target_date: date, available_hours: float) -> List[Dict]:
        """生成默认的今日任务"""
        weekdays = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        weekday_idx = target_date.weekday()
        chinese_weekday = weekdays[weekday_idx]
        
        # 根据星期几生成不同的任务模板
        if chinese_weekday == "周一":
            return self._generate_monday_tasks(available_hours)
        elif chinese_weekday == "周五":
            return self._generate_friday_tasks(available_hours)
        elif chinese_weekday in ["周二", "周三", "周四"]:
            return self._generate_midweek_tasks(available_hours, chinese_weekday)
        else:
            return self._generate_weekend_tasks()
    
    def _generate_monday_tasks(self, available_hours: float) -> List[Dict]:
        """生成周一的默认任务"""
        tasks = [
            {
                "id": "task_001",
                "description": "跟进上周会议决议和行动项",
                "category": "紧急重要",
                "priority": 1.0,
                "estimated_hours": 1.0,
                "status": "待开始",
                "actual_hours": 0,
                "completed": False
            },
            {
                "id": "task_002",
                "description": "准备管理层周例会汇报材料",
                "category": "紧急重要",
                "priority": 1.0,
                "estimated_hours": 1.5,
                "status": "待开始",
                "actual_hours": 0,
                "completed": False
            },
            {
                "id": "task_003",
                "description": "机器人技术问题深度分析",
                "category": "重要不紧急",
                "priority": 0.8,
                "estimated_hours": 2.0,
                "status": "待开始",
                "actual_hours": 0,
                "completed": False
            }
        ]
        
        return self._adjust_tasks_by_time(tasks, available_hours)
    
    def _generate_friday_tasks(self, available_hours: float) -> List[Dict]:
        """生成周五的默认任务"""
        tasks = [
            {
                "id": "task_001",
                "description": "准备商清项目Sprint评审材料",
                "category": "紧急重要",
                "priority": 1.0,
                "estimated_hours": 1.0,
                "status": "待开始",
                "actual_hours": 0,
                "completed": False
            },
            {
                "id": "task_002",
                "description": "准备晨曦项目Sprint评审材料",
                "category": "紧急重要",
                "priority": 1.0,
                "estimated_hours": 1.0,
                "status": "待开始",
                "actual_hours": 0,
                "completed": False
            },
            {
                "id": "task_003",
                "description": "本周工作总结和下周计划",
                "category": "重要不紧急",
                "priority": 0.8,
                "estimated_hours": 1.5,
                "status": "待开始",
                "actual_hours": 0,
                "completed": False
            },
            {
                "id": "task_004",
                "description": "准备技术团队分享内容",
                "category": "重要不紧急",
                "priority": 0.8,
                "estimated_hours": 1.0,
                "status": "待开始",
                "actual_hours": 0,
                "completed": False
            }
        ]
        
        return self._adjust_tasks_by_time(tasks, available_hours)
    
    def _generate_midweek_tasks(self, available_hours: float, weekday: str) -> List[Dict]:
        """生成周二、三、四的默认任务"""
        # 技术工作重点
        tech_tasks = [
            "机器人底盘控制算法优化",
            "传感器数据处理和分析",
            "系统性能测试和调优",
            "技术文档整理和完善",
            "代码审查和质量改进"
        ]
        
        # 项目管理重点
        pm_tasks = [
            "项目进度跟踪和风险识别",
            "团队资源协调和分配",
            "跨部门沟通和协作",
            "客户需求分析和反馈"
        ]
        
        # 根据星期几选择不同的重点
        if weekday == "周三":
            # 周三加入品质相关工作
            base_tasks = [
                "品质问题分析和解决",
                "质量检查报告整理",
                "持续改进方案设计"
            ]
            base_tasks.extend(tech_tasks[:2])
            base_tasks.extend(pm_tasks[:1])
        else:
            # 周二、周四以技术为主
            base_tasks = tech_tasks[:3]
            base_tasks.extend(pm_tasks[:2])
        
        tasks = []
        for i, task_desc in enumerate(base_tasks, 1):
            category = self.priority_system.categorize_task(task_desc)
            estimated_time = min(2.0, available_hours / len(base_tasks))  # 平均分配时间
            
            task = {
                "id": f"task_{i:03d}",
                "description": task_desc,
                "category": category,
                "priority": self.priority_system.task_categories[category]["weight"],
                "estimated_hours": round(estimated_time, 1),
                "status": "待开始",
                "actual_hours": 0,
                "completed": False
            }
            tasks.append(task)
        
        return self._adjust_tasks_by_time(tasks, available_hours)
    
    def _generate_weekend_tasks(self) -> List[Dict]:
        """生成周末任务"""
        return [
            {
                "id": "task_001",
                "description": "休息和放松，恢复精力",
                "category": "重要不紧急",
                "priority": 0.8,
                "estimated_hours": 0,
                "status": "建议执行",
                "actual_hours": 0,
                "completed": False
            }
        ]
    
    def _adjust_tasks_by_time(self, tasks: List[Dict], available_hours: float) -> List[Dict]:
        """根据可用时间调整任务"""
        total_estimated = sum(task["estimated_hours"] for task in tasks)
        
        if total_estimated <= available_hours:
            return tasks
        
        # 按优先级调整时间
        for task in tasks:
            if available_hours <= 0:
                task["estimated_hours"] = 0
                task["status"] = "时间不足，建议调整"
            else:
                # 按优先级比例分配时间
                proportion = task["priority"] / sum(t["priority"] for t in tasks)
                task["estimated_hours"] = round(available_hours * proportion, 1)
        
        return tasks
    
    def format_todo_for_display(self, todo_data: Dict) -> str:
        """格式化待办事项用于显示"""
        lines = []
        lines.append("=" * 60)
        lines.append(f"[日历] 每日待办事项 - {todo_data['date']} ({todo_data['day']})")
        lines.append("=" * 60)
        
        # 时间概览
        lines.append(f"\n[时间] 时间分析:")
        lines.append(f"  总工作时间: {todo_data['total_work_hours']}小时")
        lines.append(f"  会议时间: {todo_data['meeting_hours']}小时")
        lines.append(f"  可用工作时间: {todo_data['available_hours']}小时")
        
        if todo_data['evening_study']:
            lines.append(f"  晚上安排: [学习] 学习时间可用")
        else:
            lines.append(f"  晚上安排: [休息] 休息时间")
        
        # 今日会议
        if todo_data['meetings']:
            lines.append(f"\n[会议] 今日会议 ({len(todo_data['meetings'])}个):")
            for meeting in todo_data['meetings']:
                priority_icon = "[高]" if meeting['priority'] == "高" else "[中]" if meeting['priority'] == "中" else "[低]"
                lines.append(f"  {priority_icon} {meeting['time']} {meeting['name']} ({meeting['duration']})")
        
        # 待办事项
        if todo_data['tasks']:
            lines.append(f"\n[任务] 待办事项 (优先级排序):")
            for i, task in enumerate(todo_data['tasks'], 1):
                # 优先级图标
                if task['priority'] >= 1.0:
                    priority_icon = "[紧急]"
                elif task['priority'] >= 0.8:
                    priority_icon = "[重要]"
                elif task['priority'] >= 0.6:
                    priority_icon = "[一般]"
                else:
                    priority_icon = "[次要]"
                
                # 类别标签
                category_map = {
                    "紧急重要": "[紧急重要]",
                    "重要不紧急": "[重要不紧急]",
                    "紧急不重要": "[紧急不重要]",
                    "不紧急不重要": "[不紧急不重要]"
                }
                
                lines.append(f"  {i}. {priority_icon} {category_map[task['category']]} {task['description']}")
                lines.append(f"     预计时间: {task['estimated_hours']}小时 | 状态: {task['status']}")
        
        # 建议安排
        lines.append(f"\n[建议] 今日安排建议:")
        
        if todo_data['day'] == "周一":
            lines.append("  1. 08:30-09:10 深度工作：跟进上周决议")
            lines.append("  2. 09:10-09:30 会议准备：管理层例会材料")
            lines.append("  3. 09:30-12:00 会议时间：管理层+机器人讨论")
            lines.append("  4. 13:30-15:30 决议跟进：会议决议落地")
            lines.append("  5. 15:30-18:00 技术工作：机器人问题分析")
        elif todo_data['day'] == "周五":
            lines.append("  1. 08:30-09:10 深度工作：Sprint材料准备")
            lines.append("  2. 09:10-09:50 站会时间：项目同步")
            lines.append("  3. 09:50-11:00 会议准备：商清项目评审")
            lines.append("  4. 11:00-12:00 会议时间：商清项目Sprint")
            lines.append("  5. 13:30-16:30 技术工作+会议准备")
            lines.append("  6. 16:30-18:00 会议时间：晨曦项目+技术分享")
        else:  # 周二、三、四
            lines.append("  1. 08:30-09:10 深度工作：关键技术攻关")
            lines.append("  2. 09:10-09:50 站会时间：项目同步")
            lines.append("  3. 10:00-12:00 技术工作：主要技术任务")
            lines.append("  4. 13:30-15:30 项目管理：进度跟踪协调")
            lines.append("  5. 15:30-18:00 技术工作：次要技术任务")
        
        if todo_data['evening_study']:
            lines.append("  晚上：19:30-21:30 学习时间：技术/管理提升")
        
        lines.append(f"\n[时间] 生成时间: {todo_data['generated_at']}")
        lines.append("=" * 60)
        
        return "\n".join(lines)
    
    def display_today_todo(self):
        """显示今天的待办事项"""
        todo_data = self.generate_daily_todo()
        print(self.format_todo_for_display(todo_data))
    
    def display_tomorrow_todo(self):
        """显示明天的待办事项"""
        tomorrow = date.today() + timedelta(days=1)
        todo_data = self.generate_daily_todo(tomorrow)
        print(self.format_todo_for_display(todo_data))


def main():
    """主函数"""
    print("[系统] 智能每日待办事项系统")
    print("=" * 50)
    
    planner = DailyTodoPlanner()
    
    # 显示今天和明天的待办事项
    print("\n[今日] 今日待办事项:")
    planner.display_today_todo()
    
    print("\n\n[明日] 明日待办事项预览:")
    planner.display_tomorrow_todo()
    
    # 保存配置
    planner.work_config.save_weekly_meetings()
    
    print("\n[完成] 系统已就绪！每天早上运行此程序获取当日待办事项。")
    print("[提示] 可以将此程序设置为每天早上自动运行。")


if __name__ == "__main__":
    main()